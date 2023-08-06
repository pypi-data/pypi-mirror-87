# arg 1 is the directory to change
import os, sys, pickle
import numpy as np

hr_dir = os.path.join(sys.argv[1], 'HR')
lr_dir = os.path.join(sys.argv[1], 'LR')

files = os.listdir(hr_dir)
for file in files[:len(files)//2]:
    hr_path = os.path.join(hr_dir, file)
    lr_path = os.path.join(lr_dir, file)
    print(hr_path)
    # pickle.dump(pickle.load(open(hr_path, 'rb')), open(hr_path, 'wb'))
    data = np.transpose(pickle.load(open(hr_path, 'rb')), (2,1,0))
    pickle.dump(data, open(hr_path, 'wb'))
    print(lr_path)
    data = np.transpose(pickle.load(open(lr_path, 'rb')), (2, 1, 0))
    
    data = np.clip(data,-1024,4000).round().astype('uint16')#mk---clip
    
    pickle.dump(data, open(lr_path, 'wb'))


