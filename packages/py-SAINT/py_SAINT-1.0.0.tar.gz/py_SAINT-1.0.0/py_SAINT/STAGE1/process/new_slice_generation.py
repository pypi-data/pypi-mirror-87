# arg 1 input data, arg 2 output split
import os, sys, pickle
import numpy as np
spacing = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
# factor = int(sys.argv[3])
folders = ['pickleTr','pickleTs']
output_train_path_HR = os.path.join(sys.argv[2], 'TRAIN/HR')
for folder in folders:
    root_path = os.path.join(sys.argv[1], folder)
    output_train_path_HR = os.path.join(sys.argv[2], 'TRAIN/HR')
    # output_test_path_HR = os.path.join(sys.argv[2], 'TEST/HR')
    patients = os.listdir(root_path)
    length = len(patients)
    for patient in patients[length//4:length//2]:
        print('start on: ', patient)
        if patient == 'liver_187.pt':
            # data = pickle.load(open(os.path.join(root_path, patient), 'rb'))['image']
            print('pass liver_187 shape')
            continue
        if not patient.replace('.pt','') in test_files:
            output = {}
            data = np.transpose(pickle.load(open(os.path.join(root_path, patient), 'rb'))['image'], (1,0,2))
            # data = pickle.load(open(os.path.join(root_path, patient), 'rb'))['image']
            data_spacing = spacing[patient.replace('.pt', '')][2]
            # print('data shape, ', data.shape)
            # downsample_factor = int(5/data_spacing)
            # if downsample_factor < 1:
            #     downsample_factor = 1
            # print(downsample_factor)
            # downsample_spacing = downsample_factor*data_spacing
            output['spacing'] = [spacing[patient.replace('.pt', '')][0], spacing[patient.replace('.pt', '')][1], data_spacing]
            # for i in range(factor):
            #     copy = data[...,i:][:,:,::downsample_factor]
            copy = data.reshape((512,data.shape[1]*data.shape[2]))
            for j in range(int(copy.shape[1]//512)):
                name = os.path.join(output_train_path_HR, patient.replace('.pt','_sag_part_'+str(j) +'.pt'))
                hr = copy[:,512*j:512*(j+1)]
                output['image'] = hr
                pickle.dump(output, open(name,'wb'))
            print('finished: ', patient)

