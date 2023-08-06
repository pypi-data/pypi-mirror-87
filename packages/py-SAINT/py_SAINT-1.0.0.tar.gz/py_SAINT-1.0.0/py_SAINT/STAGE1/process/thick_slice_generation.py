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
# spacing_info = pickle.load(open('/data/cheng/CT/spacing.pt','rb'))
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
for patient in patients[quartile*length//4:(quartile+1)*length//4]:
    # print('start on: ', patient)
    # if not patient.replace('.pt','') in test_files:
        # data = pickle.load(open(os.path.join(root_path, patient), 'rb'))['image']
        # print('NOT TEST')
        # continue
    output = {}
    count = count + 1
    if view == 'sag':
        data = pickle.load(open(os.path.join(sys.argv[1], patient), 'rb'))
        # spacing = data['spacing']
        spacing = data['spacing']
        data = np.transpose(data['image'], (0,1,2))
        output['spacing'] = spacing
    elif view == 'cor':
        data = pickle.load(open(os.path.join(sys.argv[1], patient), 'rb'))
        spacing = data['spacing']
        # spacing = spacing_info[patient.replace('.pt','')]
        data = np.transpose(data['image'], (1,0,2))
        output['spacing'] = spacing
    for j in range(len(data)):
        name = os.path.join(output_train_path_HR, patient.replace('.pt','_'+view+'_slice_'+str(j) +'.pt'))
        if view != 'ax':
            hr = np.zeros((3, data.shape[1], data.shape[2])).astype('uint16')
            if j == 0:
                hr[1] = data[0]
                hr[2] = data[1]
            elif j == len(data)-1:
                hr[0] = data[len(data)-2]
                hr[1] = data[len(data)-1]
            else:
                hr[0] = data[j-1]
                hr[1] = data[j]
                hr[2] = data[j+1]
            output['image'] = hr
            pickle.dump(output, open(name,'wb'))
        else:
            pickle.dump(data[j], open(name, 'wb'))
    print('finished ', patient)

print(count)