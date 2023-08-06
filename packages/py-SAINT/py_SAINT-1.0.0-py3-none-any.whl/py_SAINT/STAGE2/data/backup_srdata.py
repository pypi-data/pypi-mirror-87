import os
import glob
import numpy as np
from data import common
import pickle
import torch.utils.data as data
import random


class SRData(data.Dataset):
    def __init__(self, args, name='', train=True):
        self.args = args
        self.name = name
        self.train = train
        self.split = 'train' if train else 'test'
        self.do_eval = True
        self.scale = args.scale
        self.idx_scale = 0
        data_range = [r.split('-') for r in args.data_range.split('/')]
        if train:
            data_range = data_range[0]
        else:
            if args.test_only and len(data_range) == 1:
                data_range = data_range[0]
            else:
                data_range = data_range[1]
        self.begin, self.end = list(map(lambda x: int(x), data_range))
        self._set_filesystem(args.dir_data)

        path_bin = self.apath
        os.makedirs(path_bin, exist_ok=True)

        # Binary files are stored in 'bin' folder
        # If the binary file exists, load it. If not, make it.
        list_hr, list_lr = self._scan()
        # print('*********', args.input_side)
        if args.input_side == 'cor' and self.train:
            list_hr = [x for x in list_hr if 'cor' in x]
            list_lr = [x for x in list_lr if 'cor' in x]
        elif args.input_side == 'sag' and self.train:
            list_hr = [x for x in list_hr if 'sag' in x]
            list_lr = [x for x in list_lr if 'sag' in x]
        # print(list_hr)
        os.makedirs(
            self.dir_hr.replace(self.apath, path_bin),
            exist_ok=True
        )

        self.images_hr, self.images_lr = [], []
        for h in list_hr:
            b = h.replace(self.apath, path_bin)
            self.images_hr.append(b)

        for h in list_lr:
            b = h.replace(self.apath, path_bin)
            self.images_lr.append(b)

        if train:
            self.repeat = 1

    # Below functions as used to prepare images
    def _scan(self):
        names_hr = sorted(
            glob.glob(os.path.join(self.dir_hr, '*.pt'))
        )
        names_lr = sorted(
            glob.glob(os.path.join(self.dir_lr, '*.pt'))
        )
        return names_hr, names_lr

    def _set_filesystem(self, dir_data):
        self.apath = os.path.join(dir_data, self.name)
        self.dir_hr = os.path.join(self.apath, 'HR')
        self.dir_lr = os.path.join(self.apath, 'LR')
        self.ext = ('.png', '.png')

    def __getitem__(self, idx):
        lr, hr, filename = self._load_file(idx)
        # lr, hr = self.get_patch(lr, hr)
        # print('lr shape, hr shape: ', lr.shape, hr.shape)
        # lr, hr = common.set_channel(lr, hr, n_channels=self.args.n_colors)
        if self.args.model == 'MSR_RDN':
            if self.train:
                lr, hr = np.expand_dims(lr, axis=0), np.expand_dims(hr, axis=0)
            else:
                lr, hr = np.transpose(lr, (2, 0, 1)), np.transpose(hr, (2, 0, 1))
        # The problem with bad dataloader (constantly stuck) is that the data needs to be as much the same as possible
        lr_tensor, hr_tensor = common.np2Tensor(
            lr, hr, rgb_range=self.args.rgb_range
        )
        # print('lr shape, hr shape: ', lr_tensor.size(), hr_tensor.size())
        return lr_tensor, hr_tensor, filename

    def __len__(self):
        if self.train:
            return len(self.images_hr) * self.repeat
        else:
            return len(self.images_hr)

    def _get_index(self, idx):
        if self.train:
            return idx % len(self.images_hr)
        else:
            return idx

    def _load_file(self, idx):
        idx = self._get_index(idx)
        f_hr = self.images_hr[idx]
        f_lr = self.images_lr[idx]
        filename, _ = os.path.splitext(os.path.basename(f_hr))
        # print("filenameeeeeee, ", filename)
        with open(f_hr, 'rb') as _f:
            hr = pickle.load(_f).astype('int32')
        with open(f_lr, 'rb') as _f:
            lr = pickle.load(_f).astype('int32')
        # ind = random.sample(range(0, 512), 400)
        if self.train:
            if self.args.model == 'BASELINE2D_RDN':
                return lr, hr[1:4], filename
            else:
                return lr, hr, filename
        else:
            if self.args.model == 'MSR_RDN':
                if self.args.input_side == 'cor':
                    hr = np.transpose(hr, (0, 2, 1))
                    lr = np.transpose(lr, (0, 2, 1))
                elif self.args.input_side == 'sag':
                    hr = np.transpose(hr, (1, 2, 0))
                    lr = np.transpose(lr, (1, 2, 0))
                else:
                    if bool(random.getrandbits(1)):
                        hr = np.transpose(hr, (0, 2, 1))
                        lr = np.transpose(lr, (0, 2, 1))
                    else:
                        hr = np.transpose(hr, (1, 2, 0))
                        lr = np.transpose(lr, (1, 2, 0))
                return lr, hr, filename
            elif self.args.model == 'BASELINE2D_RDN':
                return lr, hr[:-3], filename
            else:
                return lr, hr, filename

    def get_patch(self, lr, hr):
        scale = self.scale[self.idx_scale]
        # note that lr should be of smaller size than hr, unless scale is 1
        if self.train:
            lr, hr = common.get_patch_y_side(
                lr,
                hr,
                patch_size=self.args.patch_size,
                scale=scale
            )
            if not self.args.no_augment:
                # print('testing1')
                lr, hr = common.augment(lr, hr)
        else:
            # print('testing2')
            ih, iw = lr.shape[:2]
            hr = hr[0:ih * scale, 0:iw * scale]

        return lr, hr

    def set_scale(self, idx_scale):
        self.idx_scale = idx_scale
        # print('idx_scale', idx_scale)

