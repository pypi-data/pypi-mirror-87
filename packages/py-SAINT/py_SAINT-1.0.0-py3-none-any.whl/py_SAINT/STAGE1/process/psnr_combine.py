## arg1 meta volumes cor, arg2 meta volumes sag ,arg3 fuse directory

import os, sys, pickle
from skimage.measure import compare_psnr, compare_ssim
import numpy as np
from scipy.ndimage import zoom

test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
# test_files = ['liver_0', 'liver_136']
# test_files = ['LCTSC-Train-S3-002', 'LCTSC-Test-S3-101', 'LCTSC-Train-S3-004', 'LCTSC-Test-S3-102', 'LCTSC-Train-S3-001', 'LCTSC-Train-S3-008', 'LCTSC-Test-S3-203', 'LCTSC-Train-S3-003', 'LCTSC-Train-S3-012']
# test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
spacing = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
file1 = sys.argv[1]
# file2 = '../../experiment/meta_take2/results/volume_sag/'
file3 = '/data/cheng/fuse_data/TEST_NEW/HR/'
new_one = []
new_two = []
old_one = []
old_two = []
total_slice = 0
output = []
for file in test_files:
    # if spacing[file][2] >= 4.0:
        meta_cor = np.transpose(pickle.load(open(os.path.join(file1, file+'_cor_sr.pt') ,'rb'))[128:384,128:384], (2,0,1)).round().astype(float)/4000
        # meta_sag = np.transpose(pickle.load(open(os.path.join(file2, file + '_sag_sr.pt'), 'rb')),
        #                         (2, 1, 0)).round().astype(float) / 2000
        hr = pickle.load(open(os.path.join(file3, file+'.pt') ,'rb'))[:,128:384,128:384].astype(float)/4000
        hr = hr[...,hr.shape[2]%4:]
        # lr = zoom(hr[...,::4], (1,1,4))
        # old = pickle.load(open(os.path.join(file3, 'LR', file+'.pt') ,'rb')).round().astype(float)/4000
        meta_cor = np.clip(meta_cor, 0, 1)
        slice_num = hr.shape[0]
        # meta_sag = np.clip(meta_sag, 0, 1)
        hr = np.clip(hr, 0, 1)
        # old = np.clip(old, 0, 1)
        print(meta_cor.shape, hr.shape)
        psnr_new_cor = compare_psnr(hr, meta_cor)
        # psnr_new_sag = compare_psnr(hr, meta_sag)
        # psnr_new_sag = 0
        # psnr_old = compare_psnr(hr, lr)
        # psnr_old_two = compare_psnr(hr, old[1])
        print(file, 'thickness: ',  spacing[file][2], ' new cor psnr: ', np.around(psnr_new_cor,2)) #' lr psnr: ', np.around(psnr_old,2))
        new_one.append(psnr_new_cor*slice_num)
        # new_two.append(psnr_new_sag*slice_num)
        # old_one.append(psnr_old*slice_num)
        # old_two.append(psnr_old_two*slice_num)
        total_slice = total_slice+slice_num
        output.append([psnr_new_cor, slice_num,  spacing[file][2], file])

print('overall', 'new one psnr: ', np.around(np.asarray(new_one).sum()/total_slice,2))#, 'lr psnr: ', np.around(np.asarray(old_one).sum()/total_slice,2))