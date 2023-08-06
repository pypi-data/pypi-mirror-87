## arg1 input folder, arg2 output pickle, arg3 scale, arg4 type

import sys, os, pickle
import numpy as np
if sys.argv[4] == 'liver':
    test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
# test_files = ['liver_0', 'liver_136','liver_45', 'liver_46','colon_083','hepaticvessel_351','hepaticvessel_442']
# test_files = ['lung_047']
# test_files = ['LCTSC-Train-S3-002', 'LCTSC-Test-S3-101', 'LCTSC-Train-S3-004', 'LCTSC-Test-S3-102', 'LCTSC-Train-S3-001', 'LCTSC-Train-S3-008', 'LCTSC-Test-S3-203', 'LCTSC-Train-S3-003', 'LCTSC-Train-S3-012']
if sys.argv[4] == 'lung':
    test_files = ['lung_003', 'lung_009', 'lung_015', 'lung_016', 'lung_031', 'lung_033', 'lung_036', 'lung_037',
                  'lung_038', 'lung_042', 'lung_043', 'lung_057', 'lung_058', 'lung_066', 'lung_071', 'lung_086',
                  'lung_093', 'lung_096']
if sys.argv[4] == 'vessel':
    test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_vessel_top100.pt','rb'))
# test_files = pickle.load(open('/data/cheng/kits19/kits19/file_kits.pt','rb'))
if sys.argv[4] == 'colon':
    test_files = pickle.load(open('/data/cheng/colon/output_vessel/file_colon.pt','rb'))
if sys.argv[4] == 'kidney':
    test_files = ['case_00186', 'case_00111', 'case_00144', 'case_00029', 'case_00019', 'case_00171', 'case_00047',
                  'case_00046', 'case_00133', 'case_00032', 'case_00193', 'case_00105', 'case_00128', 'case_00086',
                  'case_00082', 'case_00207', 'case_00183', 'case_00131', 'case_00081', 'case_00180', 'case_00098',
                  'case_00040', 'case_00184', 'case_00072', 'case_00196', 'case_00189', 'case_00185', 'case_00043',
                  'case_00060', 'case_00036', 'case_00190', 'case_00016']
# test_files = pickle.load(open('/data/cheng/colon/files_lung.pt','rb'))
# test_files = ['003225_03_02', '003767_01_01', '003404_03_01', '002197_06_01', '003463_01_01', '001487_05_02', '003145_02_01', '004068_01_01', '001817_12_01', '004194_01_01', '000907_01_01', '003413_01_01', '001487_06_02', '004315_01_01', '000331_11_01', '002197_05_01', '004168_02_02', '000282_03_01', '003991_01_03']
output_dir = sys.argv[2]

input_dir = sys.argv[1]
print(output_dir)
scale = sys.argv[3]
missing = []
for file in test_files:
    # if not os.path.isfile(input_dir + file + '_cor_slice_' + str(0) + '_x'+scale+'_SR.pt'):
    #     missing.append(file)
    #     print('missing: ', file)
    #     continue
    lr = pickle.load(open(input_dir + file + '_cor_slice_' + str(0) + '_x'+scale+'_SR.pt', 'rb'))[..., 0]
    print(lr.shape)
    if int(scale) == 6 and ('MSR' in sys.argv[1] or 'MDSR' in sys.argv[1]):
        volume_sr = np.zeros((510, 512, lr.shape[1]))
    else:
        volume_sr = np.zeros((512, 512, lr.shape[1]))

    for i in range(512):
        # part_0_hr = pickle.load(open(input_dir+file+'_cor_' + str(i) + '_part_0_x1_HR.pt', 'rb'))[0]['image'][...,0]
        # part_1_hr = pickle.load(open(input_dir+file+'_cor_' + str(i) + '_part_1_x1_HR.pt', 'rb'))[0]['image'][...,0]
        # part_2_hr = pickle.load(open(input_dir+file+'_cor_' + str(i) + '_part_2_x1_HR.pt', 'rb'))[0]['image'][...,0]
        # lr = pickle.load(open(input_dir+file+'_cor_slice_' + str(i) + '_x'+scale+'_LR.pt', 'rb'))[0]['image'][...,0]
        sr = pickle.load(open(input_dir+file+'_cor_slice_' + str(i) + '_x'+scale+'_SR.pt', 'rb'))
        volume_sr[:,i,:] = sr[...,0]
    print('finished ', file, volume_sr.shape)
    pickle.dump(np.clip(volume_sr,0,4000).round().astype('uint16'), open(os.path.join(output_dir, file+'_cor_sr.pt'),'wb'))

print('missing: ', missing)