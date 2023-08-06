# arg 1 is the HR/orig volume dir, arg 2 is the output dir, arg 3 is factor

import os, sys, pickle
import numpy as np
files = os.listdir(sys.argv[1])
hr_dir = os.path.join(sys.argv[2], 'HR')
lr_dir = os.path.join(sys.argv[2], 'LR')


def wrapper():
    for file in files[::-1]:
        name = os.path.join(hr_dir, file.replace('.pt','_0.pt'))
        if os.path.exists(name):
            break
        data = pickle.load(open(os.path.join(sys.argv[1], file),'rb'))
        print(data.shape)
        for i in range(data.shape[2]):
            if i%4 == 0 and i+4 < data.shape[2]:
                print(file, i)
                hr = np.zeros((5, data.shape[0],data.shape[1]))
                hr[0] = data[...,i]
                hr[1] = data[..., i+1]
                hr[2] = data[..., i+2]
                hr[3] = data[..., i+3]
                hr[4] = data[..., i+4]
                lr = np.zeros((2, data.shape[0],data.shape[1]))
                lr[0] = data[..., i]
                lr[1] = data[..., i+4]
                pickle.dump(hr, open(os.path.join(hr_dir, file.replace('.pt','_'+str(i)+'.pt')), 'wb'))
                pickle.dump(lr, open(os.path.join(lr_dir, file.replace('.pt', '_' + str(i) + '.pt')), 'wb'))
    return 'finished'


result = wrapper()
print(result)