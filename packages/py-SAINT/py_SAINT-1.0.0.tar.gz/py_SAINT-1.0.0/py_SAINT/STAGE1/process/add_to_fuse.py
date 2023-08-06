import pickle, os, sys
import numpy as np
input_lr_dir = '/data/cheng/experiment/SLANT_VOLUME/results/raw/'
input_hr_dir =  '/data/cheng/CT_DATASET/TEST/HR/'
output_lr_dir = '/home/cheng/FUSE_x4/TRAIN/LR/'
# output_hr_dir = '/home/cheng/FUSE_x4/TRAIN/HR/'
files = os.listdir(input_hr_dir)
factor = int(sys.argv[2])
quartile = int(sys.argv[1])
length = len(files)
slab = 64
# temp = {0: 'hepaticvessel_432.pt',1: 'hepaticvessel_304.pt',2: 'liver_90.pt', 3: 'liver_51.pt', 4: 'liver_164.pt', 5: 'liver_111.pt', 6: 'liver_160.pt', 7: 'liver_92.pt'}
flag = False
for file in files[quartile*length//4:(quartile+1)*length//4]:
    print(file)
    # hr = pickle.load(open(input_hr_dir + file,'rb'))['image']
    lr_one = np.expand_dims(pickle.load(open(input_lr_dir + file.replace('.pt','_one_x4_SR.pt'),'rb')),axis=0)
    lr_two = np.expand_dims(pickle.load(open(input_lr_dir + file.replace('.pt','_two_x4_SR.pt'),'rb')),axis=0)
    lr = np.concatenate((lr_one,lr_two),0)
    # hr = hr[..., hr.shape[2]%factor:]
    print(lr.shape)
    for i in range(lr.shape[1]//slab):
        for j in range(lr.shape[2]//slab):
            for k in range(lr.shape[3]//slab):
                if k == lr.shape[3]//slab - 1:
                    # patch_lr = lr[:,i * slab:(i + 1) * slab, j * slab:(j + 1) * slab, k * slab:]
                    # patch_hr = hr[i * slab:(i + 1) * slab, j * slab:(j + 1) * slab, k * slab:]
                    # print('patch: ', patch_hr.shape, patch_lr.shape)
                    orig = pickle.load(open(output_lr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'rb'))
                    output = np.concatenate((orig, lr[:,i * slab:(i + 1) * slab, j * slab:(j + 1) * slab, k * slab:]),0)
                    # print(output.shape)
                    pickle.dump(output,open(output_lr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
                    # pickle.dump(hr[i * slab:(i + 1) * slab, j * slab:(j + 1) * slab, k * slab:],open(output_hr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
                else:
                    # patch_lr = lr[:,i*slab:(i+1)*slab, j*slab:(j+1)*slab, k*slab:(k+1)*slab]
                    # patch_hr = hr[i*slab:(i+1)*slab, j*slab:(j+1)*slab, k*slab:(k+1)*slab]
                    # print('patch: ', patch_hr.shape, patch_lr.shape)
                    orig = pickle.load(open(output_lr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'rb'))
                    output = np.concatenate((orig, lr[:,i*slab:(i+1)*slab, j*slab:(j+1)*slab, k*slab:(k+1)*slab]),0)
                    # print(output.shape)
                    pickle.dump(output,open(output_lr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
                    # pickle.dump(hr[i*slab:(i+1)*slab, j*slab:(j+1)*slab, k*slab:(k+1)*slab],open(output_hr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
    print('finish: ', file)
