## arg1 new method volumes dir, arg2 3dcnn comparison vlumes dir, thickness threshold
import os, sys, pickle
from skimage.measure import compare_psnr, compare_ssim
import numpy as np


# test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
# test_files = ['liver_0', 'liver_136']
# test_files = ['LCTSC-Train-S3-002', 'LCTSC-Test-S3-101', 'LCTSC-Train-S3-004', 'LCTSC-Test-S3-102', 'LCTSC-Train-S3-001', 'LCTSC-Train-S3-008', 'LCTSC-Test-S3-203', 'LCTSC-Train-S3-003', 'LCTSC-Train-S3-012']
# test_files = ['lung_003', 'lung_009', 'lung_015', 'lung_016', 'lung_031', 'lung_033', 'lung_036', 'lung_037',
#               'lung_038', 'lung_042', 'lung_043', 'lung_057', 'lung_058', 'lung_066', 'lung_071', 'lung_086',
#               'lung_093', 'lung_096']
test_files=['lung_086']
# spacing_info = pickle.load(open('/data/cheng/CT/spacing.pt','rb'))
# test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_vessel_top100.pt','rb'))
# test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_colon.pt','rb'))
# spacing_info = pickle.load(open('/data/cheng/colon/output_vessel/spacing_extra.pt','rb'))
spacing_info = pickle.load(open('/data/cheng/colon/spacing_lung.pt','rb'))
# spacing_info = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
# test_files = pickle.load(open('/data/cheng/colon/files_lung.pt','rb'))
# test_files = ['003225_03_02', '003767_01_01', '003404_03_01', '002197_06_01', '003463_01_01', '001487_05_02', '003145_02_01', '004068_01_01', '001817_12_01', '004194_01_01', '000907_01_01', '003413_01_01', '001487_06_02', '004315_01_01']
# test_files = pickle.load(open('/data/cheng/kits19/kits19/file_kits.pt','rb'))
# spacing_info = pickle.load(open('/data/cheng/kits19/kits19/file_kits.pt','rb'))

# file3 = '/data/cheng/fuse_data/TEST_NEW/'
psnr_saint = []
psnr_msr = []
psnr_meta = []
total_slice = []
output = []
threshold = 0
path_saint = '/home/cheng/CT_DSI/experiment/3slice_meta_multi_extra_lung_tumor_x4/results'
path_msr = '/home/cheng/CT_OLD_RDN/experiment/MSR_RDN_augment_lung_tumor_x4/results'
path_meta = '/home/cheng/CT_DSI/experiment/META_SR_TEST_BEST/results/x4'
path_hr = '/home/cheng/output_lung/TRAIN/'
upper = 5
factor = 4
for file in test_files:
   if spacing_info[file][2] >= threshold and spacing_info[file][2] <= upper:
        print(file)
        # if 'MSR' in sys.argv[1] and factor == 6:
        # print('MODIFYING LOCATION')
        if factor == 6:
            msr_cor = np.transpose(pickle.load(open(os.path.join(path_msr, file+'_cor_sr.pt'),'rb'))[62:446,64:448], (1,0,2)).round().astype(float)/4000
        else:
            msr_cor = np.transpose(pickle.load(open(os.path.join(path_msr, file+'_cor_sr.pt'),'rb'))[64:448,64:448], (1,0,2)).round().astype(float)/4000

        meta_cor = np.transpose(pickle.load(open(os.path.join(path_meta, file+'_cor_sr.pt'),'rb'))[64:448,64:448], (1,0,2)).round().astype(float)/4000
        saint_cor = np.transpose(pickle.load(open(os.path.join(path_saint, file + '_cor_sr.pt'), 'rb'))[64:448, 64:448],
                                (1, 0, 2)).round().astype(float) / 4000
        hr = pickle.load(open(os.path.join(path_hr, file+'.pt') ,'rb'))
        # if 'kits' in sys.argv[2]:
        #     # dwn = int(5/spacing_info[file][2])
        #     # hr = data[128:384,128:384, ::dwn].astype(float)/4000
        #     hr = data[128:384,128:384].astype(float)/4000
        # else:
        hr = hr['image'][64:448,64:448].astype(float)/4000
        hr = hr[...,hr.shape[2]%factor:]
        spacing = spacing_info[file]
        meta_cor = np.delete(np.clip(meta_cor, 0, 1), np.s_[::factor], axis=2)
        saint_cor = np.delete(np.clip(saint_cor, 0, 1), np.s_[::factor], axis=2)
        msr_cor = np.delete(np.clip(msr_cor, 0, 1), np.s_[::factor], axis=2)
        hr = np.delete(np.clip(hr, 0, 1), np.s_[::factor], axis=2)
        for i in range(hr.shape[0]):
            psnr_saint_cor = compare_psnr(hr[i], saint_cor[i])
            psnr_msr_cor = compare_psnr(hr[i], msr_cor[i])
            psnr_meta_cor = compare_psnr(hr[i], meta_cor[i])
            print(file, 'thickness: ',  spacing[2], ' saint: ', np.around(psnr_saint_cor,2), ' meta: ', np.around(psnr_meta_cor,2), ' msr: ', np.around(psnr_msr_cor,2))
            psnr_saint.append(psnr_saint_cor)
            psnr_meta.append(psnr_meta_cor)
            psnr_msr.append(psnr_msr_cor)

psnr_saint = np.asarray(psnr_saint)
psnr_meta = np.asarray(psnr_meta)
psnr_msr = np.asarray(psnr_msr)
meta_diff = psnr_saint - psnr_meta
msr_diff = psnr_saint - psnr_msr
# print('overall', 'new one psnr: ', np.around(np.asarray(new_one).sum()/total_slice,2))
# pickle.dump(output, open(sys.argv[4], 'wb'))