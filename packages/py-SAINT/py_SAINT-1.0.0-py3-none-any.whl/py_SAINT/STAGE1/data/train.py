import os
from data import srdata


class TRAIN(srdata.SRData):
    def __init__(self, args, name='TRAIN', train=True):
        super(TRAIN, self).__init__(
            args, name=name, train=train
        )

    def _scan(self):
        names_hr, names_lr = super(TRAIN, self)._scan()
        print('@@@',len(names_hr), len(names_lr))
        names_hr = names_hr[self.begin - 1:self.end]
        names_lr = names_lr[self.begin - 1:self.end]
        return names_hr, names_lr

    def _set_filesystem(self, dir_data):
        super(TRAIN, self)._set_filesystem(dir_data)
        self.dir_hr = os.path.join(self.apath, 'HR')
        self.dir_lr = os.path.join(self.apath, 'LR')
        print('###', self.dir_hr, self.dir_lr)
