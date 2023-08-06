# arg1 old test dir, arg2 new test dir HR

import sys, os, pickle
import numpy as np
test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
output_dir = sys.argv[2]
input_dir_lr = os.path.join(sys.argv[1], 'LR')+'/'
input_dir_hr = os.path.join(sys.argv[1], 'HR')+'/'
for file in test_files:
    for i in range(512):
        lr = pickle.load(open(input_dir_lr + file + '_cor_' + str(i) + '_part_0.pt', 'rb'))
        hr = np.zeros((512, lr.shape[1] * 4)).astype('uint16')
        hr[:, ::4] = lr
        part_0_hr = pickle.load(open(input_dir_hr+file+'_cor_' + str(i) + '_part_0.pt', 'rb'))
        part_1_hr = pickle.load(open(input_dir_hr+file+'_cor_' + str(i) + '_part_1.pt', 'rb'))
        part_2_hr = pickle.load(open(input_dir_hr+file+'_cor_' + str(i) + '_part_2.pt', 'rb'))
        hr[:, 1:][:, ::4] = part_0_hr['image']
        hr[:, 2:][:, ::4] = part_1_hr['image']
        hr[:, 3:][:, ::4] = part_2_hr['image']
        data = {}
        data['image'] = hr
        data['spacing'] = part_0_hr['spacing']
        pickle.dump(data, open(os.path.join(output_dir, file+'_cor_' + str(i)+'.pt'),'wb'))
        print('finished ', file+'_cor_' + str(i) + '_part_0.pt')

