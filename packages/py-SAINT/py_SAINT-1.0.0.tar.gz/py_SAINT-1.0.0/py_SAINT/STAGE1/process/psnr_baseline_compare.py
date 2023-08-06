## arg1 new method volumes dir, arg2 3dcnn comparison vlumes dir, thickness threshold, factor
import os, sys, pickle
from skimage.measure import compare_psnr, compare_ssim
import numpy as np

test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
# test_files = ['liver_42', 'liver_35', 'liver_45', 'liver_46', 'liver_44', 'liver_37', 'liver_41', 'liver_31', 'liver_36',
#          'liver_40']
# test_files = ['liver_0', 'liver_136']
# test_files = ['LCTSC-Train-S3-002', 'LCTSC-Test-S3-101', 'LCTSC-Train-S3-004', 'LCTSC-Test-S3-102', 'LCTSC-Train-S3-001', 'LCTSC-Train-S3-008', 'LCTSC-Test-S3-203', 'LCTSC-Train-S3-003', 'LCTSC-Train-S3-012']
spacing = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
# test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_vessel_top100.pt','rb'))
# spacing = pickle.load(open('/data/cheng/colon/output_vessel/spacing_extra.pt','rb'))
# file3 = '/data/cheng/fuse_data/TEST_NEW/'
new_one = []
new_two = []
old_one = []
old_two = []
total_slice = 0
output = []
threshold = float(sys.argv[3])
upper = float(sys.argv[4])
factor = int(sys.argv[5])
for file in test_files:
   if spacing[file][2] >= threshold and spacing[file][2] <= upper:
        print(file)
        meta_cor = np.transpose(pickle.load(open(os.path.join(sys.argv[1], file+'_recon.pt') ,'rb'))[128:384,128:384], (0,1,2)).round().astype(float)/4000
        # if meta_cor.shape[2]>124:
        #     meta_cor = meta_cor[...,meta_cor.shape[2]//2-62:meta_cor.shape[2]//2+62]
        # print(meta_cor.shape)
        hr = pickle.load(open(os.path.join(sys.argv[2], file+'_x4_HR.pt') ,'rb')).astype(float)/4000
        # print(hr.shape)
        old = pickle.load(open(os.path.join(sys.argv[2], file+'_x4_SR.pt') ,'rb')).round().astype(float)/4000
        meta_cor = np.delete(np.clip(meta_cor, 0, 1), np.s_[::factor], axis=2)
        slice_num = hr.shape[2]
        # meta_sag = np.clip(meta_sag, 0, 1)
        hr = np.delete(np.clip(hr, 0, 1), np.s_[::factor], axis=2)
        old = np.delete(np.clip(old, 0, 1), np.s_[::factor], axis=2)

        psnr_new_cor = compare_ssim(hr, meta_cor)
        psnr_old = compare_ssim(hr, old)
        print(file, 'thickness: ',  spacing[file][2], ' new cor psnr: ', np.around(psnr_new_cor,2), 'old psnr: ', np.around(psnr_old,2))
        new_one.append(psnr_new_cor*slice_num)
        old_one.append(psnr_old*slice_num)
        total_slice = total_slice+slice_num
        output.append(file)
print(output)
print('overall', 'new one psnr: ', np.around(np.asarray(new_one).sum()/total_slice,2), 'old one psnr: ', np.around(np.asarray(old_one).sum()/total_slice,2))
