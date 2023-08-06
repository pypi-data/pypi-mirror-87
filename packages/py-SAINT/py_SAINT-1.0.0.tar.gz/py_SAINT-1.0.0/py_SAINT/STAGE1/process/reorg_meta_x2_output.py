## input dir, output dir
import os, sys, pickle
import numpy as np

#liver_31_cor_slice_215_x1_SR.pt
test_files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
spacing = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
input_dir = sys.argv[1]
output_dir = sys.argv[2]
for file in test_files:
    space = spacing[file]
    result = {}
    result['spacing'] = space
    for i in range(512):
        path = os.path.join(input_dir, file + '_cor_slice_' + str(i) + '_x1_SR.pt')
        data = pickle.load(open(path, 'rb'))
        # print(data.shape)
        output = np.zeros((3, data.shape[0], data.shape[1]*2))
        output[1][:,::2] = data[...,0]
        output[1,:,1:][:, ::2] = data[..., 1]
        if i != 0:
            path_prev = os.path.join(input_dir, file + '_cor_slice_' + str(i-1) + '_x1_SR.pt')
            data_prev = pickle.load(open(path_prev, 'rb'))
            output[0][:,::2] = data_prev[...,0]
            output[0,:,1:][:, ::2] = data_prev[..., 1]
        if i != 511:
            path_next = os.path.join(input_dir, file + '_cor_slice_' + str(i + 1) + '_x1_SR.pt')
            data_next = pickle.load(open(path_next, 'rb'))
            output[2][:,::2] = data_next[...,0]
            output[2,:,1:][:, ::2] = data_next[..., 1]
        result['image'] = output
        pickle.dump(result, open(os.path.join(output_dir, file + '_cor_slice_' + str(i) + '.pt'),'wb'))
        print(file + '_cor_slice_' + str(i) + '.pt')