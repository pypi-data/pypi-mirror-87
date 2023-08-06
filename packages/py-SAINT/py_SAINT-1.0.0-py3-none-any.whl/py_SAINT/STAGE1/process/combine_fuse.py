import pickle, os, sys
import numpy as np
input_lr_dir = '/data/cheng/FUSE_x4/TEST/orig/'
input_hr_dir = '/data/cheng/FUSE_x4/TEST/HR/'
output_lr_dir = '/data/cheng/FUSE_x4/TEST/LR/'
# output_hr_dir = '/data/cheng/FUSE_x4/TRAIN/HR/'
files = os.listdir(input_hr_dir)
factor = int(sys.argv[2])
quartile = int(sys.argv[1])
length = len(files)
slab = 64
# temp = {0: 'hepaticvessel_432.pt',1: 'hepaticvessel_304.pt',2: 'liver_90.pt', 3: 'liver_51.pt', 4: 'liver_164.pt', 5: 'liver_111.pt', 6: 'liver_160.pt', 7: 'liver_92.pt'}
flag = False
for file in files[quartile*length//4:(quartile+1)*length//4]:
    print(file)
    # if not flag:
    #     print(temp[quartile])
    #     if file == temp[quartile]:
    #         flag = True
    #     else:
    #         continue
    hr = pickle.load(open(input_hr_dir + file,'rb'))['image']
    lr_cor = np.expand_dims(pickle.load(open(input_lr_dir + file.replace('.pt','_cor_x4_SR.pt'),'rb')),axis=0)
    lr_sag = np.expand_dims(pickle.load(open(input_lr_dir + file.replace('.pt','_sag_x4_SR.pt'),'rb')),axis=0)
    lr = np.concatenate((lr_cor,lr_sag),0)
    # hr = hr[..., hr.shape[2]%factor:]
    pickle.dump(lr,open(output_lr_dir+file,'wb'))
    # pickle.dump(hr,open(output_hr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
    print(lr.shape, hr.shape)
    print('finish: ', file)
