## arg1 new method volumes dir, arg2 3dcnn comparison vlumes dir, thickness threshold,
import os, sys, pickle
from skimage.measure import compare_psnr, compare_ssim
import numpy as np

if sys.argv[6] == 'liver':
    test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
    spacing_info = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
# test_files = ['liver_0', 'liver_136']
# test_files = ['LCTSC-Train-S3-002', 'LCTSC-Test-S3-101', 'LCTSC-Train-S3-004', 'LCTSC-Test-S3-102', 'LCTSC-Train-S3-001', 'LCTSC-Train-S3-008', 'LCTSC-Test-S3-203', 'LCTSC-Train-S3-003', 'LCTSC-Train-S3-012']
if sys.argv[6] == 'lung':
    test_files = ['lung_003', 'lung_009', 'lung_015', 'lung_016', 'lung_031', 'lung_033', 'lung_036', 'lung_037',
              'lung_038', 'lung_042', 'lung_043', 'lung_057', 'lung_058', 'lung_066', 'lung_071', 'lung_086',
              'lung_093', 'lung_096']
    spacing_info = pickle.load(open('/data/cheng/colon/spacing_lung.pt','rb'))

# spacing_info = pickle.load(open('/data/cheng/CT/spacing.pt','rb'))
if sys.argv[6] == 'vessel':
    test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_vessel_top100.pt','rb'))
    spacing_info = pickle.load(open('/data/cheng/colon/output_vessel/spacing_extra.pt','rb'))

if sys.argv[6] == 'colon':
    test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_colon.pt','rb'))
    spacing_info = pickle.load(open('/data/cheng/colon/output_vessel/spacing_extra.pt','rb'))

if sys.argv[6] == 'kidney':
    # test_files = ['case_00186', 'case_00111', 'case_00144', 'case_00029', 'case_00019', 'case_00171', 'case_00047', 'case_00046', 'case_00133', 'case_00032', 'case_00193', 'case_00105', 'case_00128', 'case_00086', 'case_00082', 'case_00207', 'case_00183', 'case_00131', 'case_00081', 'case_00180', 'case_00098', 'case_00040', 'case_00184', 'case_00072', 'case_00196', 'case_00189', 'case_00185', 'case_00043', 'case_00060', 'case_00036', 'case_00190', 'case_00016']
    # test_files = ['case_00180']
    test_files = os.listdir(sys.argv[2])
    test_files = [x.replace('.pt','') for x in test_files]
# test_files = pickle.load(open('/data/cheng/colon/files_lung.pt','rb'))
# test_files = ['003225_03_02', '003767_01_01', '003404_03_01', '002197_06_01', '003463_01_01', '001487_05_02', '003145_02_01', '004068_01_01', '001817_12_01', '004194_01_01', '000907_01_01', '003413_01_01', '001487_06_02', '004315_01_01']
# test_files = pickle.load(open('/data/cheng/kits19/kits19/file_kits.pt','rb'))
# spacing_info = pickle.load(open('/data/cheng/kits19/kits19/file_kits.pt','rb'))

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
   # if spacing_info[file][2] >= threshold and spacing_info[file][2] <= upper:
        print(file)
        if not os.path.isfile(os.path.join(sys.argv[1], file+'_cor_x'+sys.argv[5]+'_SR.pt')):
            continue
        if ('MSR' in sys.argv[1] or 'MDSR' in sys.argv[1]) and factor == 6:
          print('MODIFYING LOCATION')
          # meta_cor = np.transpose(pickle.load(open(os.path.join(sys.argv[1], file+'_cor_x'+sys.argv[5]+'_SR.pt') ,'rb'))[62:446,64:448], (0,1,2)).round().astype(float)/4000
          # meta_cor = np.transpose(pickle.load(open(os.path.join(sys.argv[1], file+'_cor_sr.pt') ,'rb')), (1,0,2)).round().astype(float)/4000
          # meta_cor =np.transpose(pickle.load(open(os.path.join(sys.argv[1], file+'_cor_x6_SR.pt') ,'rb'))[130:386,130:386], (0,1,2)).round().astype(float)/4000
          # print(meta_cor.shape)
        else:
          meta_cor = np.transpose(pickle.load(open(os.path.join(sys.argv[1], file+'_cor_x'+sys.argv[5]+'_SR.pt') ,'rb'))[128:384,128:384], (0,1,2)).round().astype(float)/4000
          # meta_cor = meta_cor + np.transpose(pickle.load(open(os.path.join(sys.argv[1].replace('X2','X2_sag'), file+'_sag_x'+sys.argv[5]+'_SR.pt') ,'rb'))[128:384,128:384], (0,1,2)).round().astype(float)/4000
          # meta_cor = meta_cor/2
          # meta_cor = np.transpose(pickle.load(open(os.path.join(sys.argv[1], file+'_cor_sr.pt') ,'rb'))[128:384,128:384], (1,0,2)).round().astype(float)/4000
          # meta_cor = np.transpose(pickle.load(open(os.path.join(sys.argv[1], file+'_x2_SR.pt') ,'rb'))[128:384,128:384], (0,1,2)).round().astype(float)/4000
          # meta_cor = pickle.load(open(os.path.join(sys.argv[1], file+'.pt'), 'rb'))[0][128:384, 128:384].round().astype(float) / 4000

        # if meta_cor.shape[2]>124:
        #     meta_cor = meta_cor[...,meta_cor.shape[2]//2-62:meta_cor.shape[2]//2+62]
        print(meta_cor.shape)
        data = pickle.load(open(os.path.join(sys.argv[2], file+'.pt') ,'rb'))['image']
        # if 'kits' in sys.argv[2]:
            # dwn = int(5/spacing_info[file][2])
            # hr = data[128:384,128:384, ::dwn].astype(float)/4000
            # hr = data[128:384,128:384].astype(float)/4000
        # else:
        hr = data[128:384,128:384].astype(float)/4000
        hr = hr[...,hr.shape[2]%factor:]
        # meta_cor = meta_cor[..., meta_cor.shape[2] % 4:]
        # spacing = data['spacing']
        # spacing = spacing_info[file]
        print('hr', hr.shape)
        # old = pickle.load(open(os.path.join(sys.argv[2], file+'_x4_SR.pt') ,'rb'))[0]['image'].round().astype(float)/4000
        meta_cor = np.delete(np.clip(meta_cor, 0, 1), np.s_[::factor], axis=2)
        slice_num = hr.shape[2]
        # meta_sag = np.clip(meta_sag, 0, 1)
        hr = np.delete(np.clip(hr, 0, 1), np.s_[::factor], axis=2)
        # for i in range(hr.shape[0]):
        psnr_new_cor = compare_psnr(hr, meta_cor)
        new_one.append(psnr_new_cor*slice_num)
        # ssim_new_cor = compare_ssim(hr, meta_cor)
        # psnr_old = compare_psnr(hr, old)
        print(file, 'thickness: ',  ' new cor psnr: ', np.around(psnr_new_cor,2))
        # new_two.append(ssim_new_cor*slice_num)
        total_slice = total_slice+slice_num
        output.append([psnr_new_cor, file])

print('overall', 'new one psnr: ', np.asarray(new_one).sum()/total_slice)
# pickle.dump(np.asarray(new_one), open(sys.argv[7],'wb'))

# print('overall', 'new one ssim: ', np.asarray(new_two).sum()/total_slice)
# pickle.dump(output, open(sys.argv[4], 'wb'))