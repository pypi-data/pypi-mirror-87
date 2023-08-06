import pickle, os, sys
import numpy as np
from scipy.ndimage import zoom
input_lr_dir = '/home/cheng/FUSE_x4/TRAIN/LR/'
input_hr_dir = '/home/cheng/FUSE_x4/TRAIN/HR/'
# output_lr_dir = '/home/cheng/FUSE_x4/TEST/LR/'
# output_hr_dir = '/data/cheng/FUSE_x4/TRAIN/HR/'
files = os.listdir(input_hr_dir)
factor = int(sys.argv[2])
quartile = int(sys.argv[1])
length = len(files)
print(length)
# slab = 64
# temp = {0: 'hepaticvessel_432.pt',1: 'hepaticvessel_304.pt',2: 'liver_90.pt', 3: 'liver_51.pt', 4: 'liver_164.pt', 5: 'liver_111.pt', 6: 'liver_160.pt', 7: 'liver_92.pt'}
# flag = False
for file in files[quartile*length//4:(quartile+1)*length//4]:
    print(file)
    hr = pickle.load(open(input_hr_dir + file,'rb'))
    hr = hr[...,hr.shape[2]%factor:]
    orig = pickle.load(open(input_lr_dir + file,'rb'))[...,:-3]
    # print(orig.shape[-1], hr.shape[-1] -6)
    if orig.shape[-1] == hr.shape[-1] -6:
        print('already did, pass: ', file)
        continue
    dwn = hr[...,::factor]
    lr = np.zeros((hr.shape[0], hr.shape[1], hr.shape[2] - 3))
    for i in range(dwn.shape[2] - 1):
        lr[..., i * 4] = dwn[..., i]
        lr[..., i * 4 + 1:i * 4 + 4] = zoom(dwn[..., i:i + 2], (1, 1, 2.5))[..., 1:4]
    lr[..., -1] = dwn[..., -1]
    lr = np.expand_dims(lr,axis=0)
    print(lr.shape, orig.shape, hr.shape)
    orig[0] = lr
    pickle.dump(orig,open(input_lr_dir+file,'wb'))
    # pickle.dump(hr,open(output_hr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
    print(lr.shape, hr.shape)
    print('finish: ', file)
