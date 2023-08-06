import os
import math
from decimal import Decimal

import utility
import scipy.misc
import torch
from torch.autograd import Variable
from tqdm import tqdm


class Trainer():
    def __init__(self, args, loader, my_model, my_loss, ckp):
        self.args = args
        self.scale = args.scale

        self.ckp = ckp
        self.loader_train = loader.loader_train
        self.loader_test = loader.loader_test
        # print('***',len(self.loader_train.dataset))
        self.model = my_model
        self.loss = my_loss
        self.optimizer = utility.make_optimizer(args, self.model)
        self.scheduler = utility.make_scheduler(args, self.optimizer)

        if self.args.load != '.':
            self.optimizer.load_state_dict(
                torch.load(os.path.join(ckp.dir, 'optimizer.pt'))
            )
            for _ in range(len(ckp.log)): self.scheduler.step()

        self.error_last = 1e8

    def train(self):
        self.scheduler.step()
        self.loss.step()
        epoch = self.scheduler.last_epoch + 1
        lr = self.scheduler.get_lr()[0]

        self.ckp.write_log(
            '[Epoch {}]\tLearning rate: {:.2e}'.format(epoch, Decimal(lr))
        )
        self.loss.start_log()
        self.model.train()

        timer_data, timer_model = utility.timer(), utility.timer()
        for batch, (lr, hr, _, idx_scale) in enumerate(self.loader_train):
            lr, hr = self.prepare(lr, hr)
            timer_data.hold()
            timer_model.tic()

            self.optimizer.zero_grad()
            sr = self.model(lr, idx_scale)
            # print("*********** sr size", sr.size())
            loss = self.loss(sr, hr)
            if loss.item() < self.args.skip_threshold * self.error_last:
                loss.backward()
                self.optimizer.step()
            else:
                print('Skip this batch {}! (Loss: {})'.format(
                    batch + 1, loss.item()
                ))

            timer_model.hold()

            if (batch + 1) % self.args.print_every == 0:
                self.ckp.write_log('[{}/{}]\t{}\t{:.1f}+{:.1f}s'.format(
                    (batch + 1) * self.args.batch_size,
                    len(self.loader_train.dataset),
                    self.loss.display_loss(batch),
                    timer_model.release(),
                    timer_data.release()))

            timer_data.tic()

        self.loss.end_log(len(self.loader_train))
        self.error_last = self.loss.log[-1, -1]

    def test(self):
        epoch = self.scheduler.last_epoch + 1
        self.ckp.write_log('\nEvaluation:')
        self.ckp.add_log(torch.zeros(1, len(self.scale)))
        self.model.eval()

        timer_test = utility.timer()
        with torch.no_grad():
            for idx_scale, scale in enumerate(self.scale):
                eval_acc = 0
                # eval_acc_orig = 0
                self.loader_test.dataset.set_scale(idx_scale)
                tqdm_test = tqdm(self.loader_test, ncols=80)
                for idx_img, (lr, hr, filename, _) in enumerate(tqdm_test):

                    filename = filename[0]
                    no_eval = (hr.nelement() == 1)
                    if not no_eval:
                        lr, hr = self.prepare(lr, hr)
                    else:
                        lr, = self.prepare(lr)
                    if self.args.model == 'MSR_RDN':
                        C, B, W, H = lr.size()
                        lr, hr = lr.view((B * C, 1, W, H)), hr.view((B * C, 1, W, H * 4))
                        for i in range(32):
                            sub_lr, sub_hr = lr[int(16 * i):int(16 * (i + 1))], hr[int(16 * i):int(16 * (i + 1))]
                            sr = self.model(sub_lr, idx_scale)
                            if i == 0:
                                # output_lr = sub_lr[:, 0, :, :]
                                # output_hr = sub_hr[:, 0, :, :]
                                output_sr = sr[:, 0, :, :]
                            else:
                                # output_lr = torch.cat((output_lr, sub_lr[:,0,:,:]))
                                # output_hr = torch.cat((output_hr, sub_hr[:,0,:,:]))
                                output_sr = torch.cat((output_sr, sr[:, 0, :, :]))
                    elif self.args.model == 'FUSE_RDN':
                        B, C, S, W, H = lr.size()
                        print('****', lr.size(), hr.size())
                        for i in range(S):
                            if i % 4 != 0:
                                sub_lr, sub_hr = lr[[0], :, i, :, :], hr[[0], i, :, :]
                                sr = self.model(sub_lr, idx_scale)
                                output_sr = torch.cat((output_sr, sr[:, [0], :, :]), 1)
                            elif i == 0:
                                output_sr = hr[:, [0], :, :]
                            else:
                                output_sr = torch.cat((output_sr, hr[:, [i], :, :]), 1)
                        print(output_sr.size())
                    elif self.args.model == 'BASELINE2D_RDN':
                        B, S, W, H = lr.size()
                        print('####', lr.size(), hr.size())
                        for i in range(S - 1):
                            sub_lr = lr[:, i:i + 2, :, :]
                            sr = self.model(sub_lr, idx_scale)
                            if i == 0:
                                output_sr = sub_lr[:, [0], :, :]
                                output_sr = torch.cat((output_sr, sr), 1)
                                output_sr = torch.cat((output_sr, sub_lr[:, [1], :, :]), 1)
                            else:
                                # output_sr = torch.cat((output_sr, sub_lr[:, [0], :, :]), 1)
                                output_sr = torch.cat((output_sr, sr), 1)
                                output_sr = torch.cat((output_sr, sub_lr[:, [1], :, :]), 1)
                        print(output_sr.size())
                    else:
                        output_sr = self.model(lr, idx_scale)
                        # output_hr = hr
                        # output_lr = lr
                    save_list = [output_sr]
                    if not no_eval:
                        eval_acc += utility.calc_psnr(
                            self.args, output_sr, hr, scale
                        )
                        save_list.extend([lr, hr])

                    if self.args.save_results:
                       
                        self.ckp.save_results(filename, save_list, scale)

                self.ckp.log[-1, idx_scale] = eval_acc / len(self.loader_test)
                # orig_psnr = eval_acc_orig / len(self.loader_test)
                best = self.ckp.log.max(0)
                self.ckp.write_log(
                    '[{} x{}]\tPSNR: {:.3f} (Best: {:.3f} @epoch {})'.format(
                        self.args.data_test,
                        scale,
                        self.ckp.log[-1, idx_scale],
                        # orig_psnr,
                        best[0][idx_scale],
                        best[1][idx_scale] + 1
                    )
                )

        self.ckp.write_log(
            'Total time: {:.2f}s\n'.format(timer_test.toc()), refresh=True
        )
        if not self.args.test_only:
            self.ckp.save(self, epoch, is_best=(best[1][0] + 1 == epoch))

    def prepare(self, *args):
        device = torch.device('cpu' if self.args.cpu else 'cuda')

        def _prepare(tensor):
            if self.args.precision == 'half': tensor = tensor.half()
            return tensor.to(device)

        return [_prepare(a) for a in args]

    def terminate(self):
        if self.args.test_only:
            self.test()
            return True
        else:
            epoch = self.scheduler.last_epoch + 1
            return epoch >= self.args.epochs

