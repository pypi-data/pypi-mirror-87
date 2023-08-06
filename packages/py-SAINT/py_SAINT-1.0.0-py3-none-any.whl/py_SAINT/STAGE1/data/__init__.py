from importlib import import_module

from ..dataloader import MSDataLoader
from torch.utils.data.dataloader import default_collate
from ..import data
from ..data import test
class Data:
    def __init__(self, args):
        self.loader_train = None
        if not args.test_only:
            print("not_test_only")
            module_train = import_module('data.' + args.data_train.lower())
            trainset = getattr(module_train, args.data_train)(args)
            print('---', trainset)
            self.loader_train = MSDataLoader(
                args,
                trainset,
                batch_size=args.batch_size,
                shuffle=True,
                pin_memory=not args.cpu
            )

        if args.data_test in ['Set5', 'Set14', 'B100', 'Urban100']:
            print("data_test in set5...")
            module_test = import_module('data.benchmark')
            testset = getattr(module_test, 'Benchmark')(args, train=False)
        else:
            print("data_test not in set5....")
            #module_test = import_module('data.' +  args.data_test.lower())
            #module_test = import_module('.data.' + args.data_test.lower(),'data.subpkg')
            #print("module_test---",module_test)
            #testset = getattr(module_test, args.data_test)(args, train=False)
            testset =  getattr(test, args.data_test)(args, train=False)
        #print("module_test---",module_test)
        print("testset---",testset)
        self.loader_test = MSDataLoader(
            args,
            testset,
            batch_size=1,
            shuffle=False,
            pin_memory=not args.cpu
        )

