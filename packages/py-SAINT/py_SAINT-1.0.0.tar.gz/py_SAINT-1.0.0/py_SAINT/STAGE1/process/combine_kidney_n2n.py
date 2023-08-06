## arg1 input folder, arg2 output pickle, arg3 scale, arg4 type

import sys, os, pickle
import numpy as np
import scipy.misc
test_files = ['case_00180']
output_dir = sys.argv[2]

input_dir = sys.argv[1]
view = sys.argv[3]

for file in test_files:
    if view == 'cor':
        sr = pickle.load(open(input_dir + file + '_' + str(0) + '_0_x1_SR.pt', 'rb'))[1]
    else:
        sr = pickle.load(open(input_dir + file + '_sag_' + str(0) + '_0_x1_SR.pt', 'rb'))[1]

    volume_sr = np.zeros((512, 512, sr.shape[1]))
    for i in range(512):
        if view == 'cor':
            sr = pickle.load(open(input_dir + file + '_' + str(i) + '_0_x1_SR.pt', 'rb'))
            volume_sr[i] = sr[1]
        else:
            sr = pickle.load(open(input_dir + file + '_sag_' + str(i) + '_0_x1_SR.pt', 'rb'))
            volume_sr[:,i] = sr[1]
    print('finish, ', file)
    pickle.dump(volume_sr.astype('uint16'), open(output_dir+file+'.pt','wb'))


