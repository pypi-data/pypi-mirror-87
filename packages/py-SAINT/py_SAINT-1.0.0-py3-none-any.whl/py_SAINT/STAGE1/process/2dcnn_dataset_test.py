# arg 1 is the HR/orig volume dir, arg 2 is the output dir, arg 3 is factor
import os, sys, pickle
import numpy as np
files = os.listdir(sys.argv[1])
hr_dir = os.path.join(sys.argv[2], 'HR')
lr_dir = os.path.join(sys.argv[2], 'LR')

for file in files:
    data = pickle.load(open(os.path.join(sys.argv[1], file),'rb'))
    data = np.transpose(data, (2, 1, 0))
    lr = np.zeros((data.shape[0]//4, data.shape[1], data.shape[2])).astype('uint16')
    for i in range(data.shape[0]//4):
        lr[i] = data[i*4]
    pickle.dump(data, open(os.path.join(hr_dir, file), 'wb'))
    pickle.dump(lr, open(os.path.join(lr_dir, file), 'wb'))