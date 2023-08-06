## arg1 input folder, arg2 output pickle, arg3 scale, factor

import sys, os, pickle
import numpy as np
test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
# test_files = ['liver_42', 'liver_35', 'liver_45', 'liver_46', 'liver_44', 'liver_37', 'liver_41', 'liver_31', 'liver_36']
# test_files = ['lung_047']
# test_files = ['liver_0', 'liver_136']
# test_files = ['liver_0']
# test_files = ['LCTSC-Train-S3-002', 'LCTSC-Test-S3-101', 'LCTSC-Train-S3-004', 'LCTSC-Test-S3-102', 'LCTSC-Train-S3-001', 'LCTSC-Train-S3-008', 'LCTSC-Test-S3-203', 'LCTSC-Train-S3-003', 'LCTSC-Train-S3-012']
# test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_vessel_top100.pt','rb'))
# test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_colon.pt','rb'))
# test_files = pickle.load(open('/data/cheng/colon/files_lung.pt','rb'))
# test_files = ['003225_03_02', '003767_01_01', '003404_03_01', '002197_06_01', '003463_01_01', '001487_05_02', '003145_02_01', '004068_01_01', '001817_12_01', '004194_01_01', '000907_01_01', '003413_01_01', '001487_06_02', '004315_01_01']
# test_files = ['lung_003', 'lung_009', 'lung_015', 'lung_016', 'lung_031', 'lung_033', 'lung_036', 'lung_037',
#               'lung_038', 'lung_042', 'lung_043', 'lung_057', 'lung_058', 'lung_066', 'lung_071', 'lung_086',
#               'lung_093', 'lung_096']

# test_files = pickle.load(open('/data/cheng/kits19/kits19/file_kits.pt','rb'))
output_dir = sys.argv[2]
input_dir = sys.argv[1]
factor = int(sys.argv[4])
print(output_dir)
missing = []
scale = sys.argv[3]
for file in test_files:
    print(file)
    # if file == 'case_00132':
    #     continue
    # if not os.path.isfile(input_dir + file + '_cor_slice_' + str(0) + '_x'+scale+'_SR.pt'):
    #     missing.append(file)
    #     print('missing: ', file)
    #     continue
    lr = pickle.load(open(input_dir + file + '_cor_slice_' + str(0) + '_x'+scale+'_SR.pt', 'rb'))
    print(lr.shape)
    volume_sr = np.zeros((512, 512, lr.shape[1]*4))
    for i in range(512):
        # part_0_hr = pickle.load(open(input_dir+file+'_cor_' + str(i) + '_part_0_x1_HR.pt', 'rb'))[0]['image'][...,0]
        # part_1_hr = pickle.load(open(input_dir+file+'_cor_' + str(i) + '_part_1_x1_HR.pt', 'rb'))[0]['image'][...,0]
        # part_2_hr = pickle.load(open(input_dir+file+'_cor_' + str(i) + '_part_2_x1_HR.pt', 'rb'))[0]['image'][...,0]
        # lr = pickle.load(open(input_dir+file+'_cor_slice_' + str(i) + '_x'+scale+'_LR.pt', 'rb'))[0]['image'][...,0]
        sr = pickle.load(open(input_dir+file+'_cor_slice_' + str(i) + '_x'+scale+'_SR.pt', 'rb'))
        # print(sr.shape)
        for j in range(factor):
            # print(factor, i)
            volume_sr[:,i,j:][:, ::factor] = sr[...,j]
    pickle.dump(np.clip(volume_sr,0,4000).round().astype('uint16'), open(os.path.join(output_dir, file+'_cor_sr.pt'),'wb'))
    print('finished ', file)

print('missing: ', missing)