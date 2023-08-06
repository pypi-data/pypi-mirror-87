# arg 1 input data, arg 2 output split, arg 3 quartile data gen (0123), arg 4 view
import os, sys, pickle
import numpy as np
# spacing = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
# test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
# print(len(test_files))
# factor = int(sys.argv[3])
# folders = ['pickleTr','pickleTs']
# min_size = 32
# discard_num = 0
# test_files = ['LCTSC-Train-S3-002', 'LCTSC-Test-S3-101', 'LCTSC-Train-S3-004', 'LCTSC-Test-S3-102', 'LCTSC-Train-S3-001', 'LCTSC-Train-S3-008', 'LCTSC-Test-S3-203', 'LCTSC-Train-S3-003', 'LCTSC-Train-S3-012']
spacing_info_liver = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
spacing_info_other = pickle.load(open('/data/cheng/colon/output_vessel/spacing_extra.pt','rb'))
quartile = int(sys.argv[3])
view = sys.argv[4]
output_train_path_HR = os.path.join(sys.argv[2], 'HR')
count = 0
# for folder in folders:
#     root_path = os.path.join(sys.argv[1], folder)
#     output_train_path_HR = os.path.join(sys.argv[2], 'TEST/HR')
    # output_test_path_HR = os.path.join(sys.argv[2], 'TEST/HR')
patients = os.listdir(sys.argv[1])
# print(patients)
length = len(patients)
for patient in patients[quartile*length//8:(quartile+1)*length//8]:
    print('start on: ', patient)
    output = {}
    count = count + 1

    data = pickle.load(open(os.path.join(sys.argv[1], patient), 'rb'))
    # spacing = data['spacing']
    if 'spacing' in data:
        spacing = list(data['spacing'])
    elif patient.replace('.pt','') in spacing_info_liver:
        spacing = list(spacing_info_liver[patient.replace('.pt','')])
    elif patient.replace('.pt','') in spacing_info_other:
        spacing = list(spacing_info_other[patient.replace('.pt', '')])
    else:
        print('PROBLEM!')
        break
    data = data['image']
    spacing[0], spacing[1] = np.sqrt(2)*spacing[0],np.sqrt(2)*spacing[1]
    output['spacing'] = spacing

    if view == 'slant_forward':
        for i in range(256):
            img = np.zeros((512 - i, data.shape[2])).astype('uint16')
            for j in range(512 - i):
                for k in range(data.shape[2]):
                    img[j,k] = data[j+i,j,k]
            name = os.path.join(output_train_path_HR, patient.replace('.pt', '_' + view + '_slice_' + str(255-i) + '.pt'))
            output['image'] = img
            pickle.dump(output, open(name,'wb'))

        for i in range(1, 256):
            img = np.zeros((512 - i, data.shape[2])).astype('uint16')
            for j in range(512 - i):
                for k in range(data.shape[2]):
                    img[j,k] = data[j,j+i,k]
            name = os.path.join(output_train_path_HR, patient.replace('.pt', '_' + view + '_slice_' + str(255 + i) + '.pt'))
            output['image'] = img
            pickle.dump(output, open(name,'wb'))
    else:
        for i in range(256):
            img = np.zeros((512 - i, data.shape[2])).astype('uint16')
            for j in range(512 - i):
                for k in range(data.shape[2]):
                    img[j, k] = data[j + i, 511 - j, k]
            name = os.path.join(output_train_path_HR, patient.replace('.pt', '_' + view + '_slice_' + str(255-i) + '.pt'))
            output['image'] = img
            pickle.dump(output, open(name,'wb'))

        for i in range(1, 256):
            img = np.zeros((512 - i, data.shape[2])).astype('uint16')
            for j in range(512 - i):
                for k in range(data.shape[2]):
                    img[j, k] = data[j, 511 - j - i, k]
            name = os.path.join(output_train_path_HR, patient.replace('.pt', '_' + view + '_slice_' + str(255 + i) + '.pt'))
            output['image'] = img
            pickle.dump(output, open(name,'wb'))

    print('finished: ', patient)

    # for j in range(len(data)):
    #     name = os.path.join(output_train_path_HR, patient.replace('.pt','_'+view+'_slice_'+str(j) +'.pt'))
    #     if view != 'ax':
    #         hr = np.zeros((3, data.shape[1], data.shape[2])).astype('uint16')
    #         if j == 0:
    #             hr[1] = data[0]
    #             hr[2] = data[1]
    #         elif j == 511:
    #             hr[0] = data[510]
    #             hr[1] = data[511]
    #         else:
    #             hr[0] = data[j-1]
    #             hr[1] = data[j]
    #             hr[2] = data[j+1]
    #         output['image'] = hr
    #         pickle.dump(output, open(name,'wb'))
    #     else:
    #         pickle.dump(data[j], open(name, 'wb'))

print(count)