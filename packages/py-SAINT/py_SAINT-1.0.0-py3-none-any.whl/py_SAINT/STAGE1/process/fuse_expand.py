import pickle, os, sys
import numpy as np
input_lr_dir_one = '/home/cheng/CT_DSI/experiment/INTERNAL_CASE_00180_TRAIN/results/raw/'
# input_lr_dir_two = '/data/temp/experiment/SLANT_VOLUME_x6/results/raw/'
input_hr_dir =  '/data/cheng/CT_DATASET/TEST/TEST/HR/'
output_lr_dir = '/home/cheng/CASE_00180/3D/TRAIN/LR/'
output_hr_dir = '/home/cheng/CASE_00180/3D/TRAIN/HR/'

# test_files_liver = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
# test_files_vessel = pickle.load(open('/data/cheng/colon/output_vessel/file_vessel_top100.pt','rb'))
# test_files_colon = pickle.load(open('/data/cheng/colon/output_vessel/file_colon.pt','rb'))
# test_files = test_files_liver+test_files_colon+test_files_vessel
files = ['case_00180.pt']
factor = 2
# quartile = int(sys.argv[1])
slab = 64
# temp = {0: 'hepaticvessel_432.pt',1: 'hepaticvessel_304.pt',2: 'liver_90.pt', 3: 'liver_120.pt'}
flag = False
# train = []
# for file in files:
#     flag = True
#     for test in test_files:
#         if test in file:
#             flag = False
#     if flag:
#         train.append(file)
#

length = len(files)
# print(len(train))
for file in files:
    print(file)
    # if not flag:
    #     print(temp[quartile])
    #     if file == temp[quartile]:
    #         flag = True
    #     else:
    #         continue
    hr = pickle.load(open(input_hr_dir + file,'rb'))['image']
    lr_cor = np.expand_dims(pickle.load(open(input_lr_dir_one + file.replace('.pt','_cor_x2_SR.pt'),'rb')),axis=0)
    lr_sag = np.expand_dims(pickle.load(open(input_lr_dir_one + file.replace('.pt','_sag_x2_SR.pt'),'rb')),axis=0)
    # lr_one = np.expand_dims(pickle.load(open(input_lr_dir_two + file.replace('.pt','_one_x6_SR.pt'),'rb')),axis=0)
    # lr_two = np.expand_dims(pickle.load(open(input_lr_dir_two + file.replace('.pt','_two_x6_SR.pt'),'rb')),axis=0)
    lr = np.concatenate((lr_cor,lr_sag),0)
    print(lr.shape)
    hr = hr[..., hr.shape[2]%factor:][...,::2]
    print(lr.shape, hr.shape)
    for i in range(hr.shape[0]//slab):
        for j in range(hr.shape[1]//slab):
            for k in range(hr.shape[2]//slab):
                if k == hr.shape[2]//slab - 1:
                    # patch_lr = lr[:,i * slab:(i + 1) * slab, j * slab:(j + 1) * slab, k * slab:]
                    # patch_hr = hr[i * slab:(i + 1) * slab, j * slab:(j + 1) * slab, k * slab:]
                    # print('patch: ', patch_hr.shape, patch_lr.shape)
                    pickle.dump(lr[:,i * slab:(i + 1) * slab, j * slab:(j + 1) * slab, k * slab:],open(output_lr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
                    pickle.dump(hr[i * slab:(i + 1) * slab, j * slab:(j + 1) * slab, k * slab:],open(output_hr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
                else:
                    # patch_lr = lr[:,i*slab:(i+1)*slab, j*slab:(j+1)*slab, k*slab:(k+1)*slab]
                    # patch_hr = hr[i*slab:(i+1)*slab, j*slab:(j+1)*slab, k*slab:(k+1)*slab]
                    # print('patch: ', patch_hr.shape, patch_lr.shape)
                    pickle.dump(lr[:,i*slab:(i+1)*slab, j*slab:(j+1)*slab, k*slab:(k+1)*slab],open(output_lr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
                    pickle.dump(hr[i*slab:(i+1)*slab, j*slab:(j+1)*slab, k*slab:(k+1)*slab],open(output_hr_dir+file.replace('.pt','_'+'_'.join([str(i),str(j),str(k)])+'.pt'),'wb'))
    print('finish: ', file)
