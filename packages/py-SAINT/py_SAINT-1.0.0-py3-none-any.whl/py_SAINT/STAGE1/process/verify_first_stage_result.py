# arg 1 SR cor file path, arg 2 HR file path, arg 3 output folder
import os, sys, pickle
import numpy as np
import scipy.misc

sr_cor = pickle.load(open(sys.argv[1], 'rb'))[0]['image']
print(sr_cor.shape)
sr_sag = pickle.load(open(sys.argv[1].replace('cor','sag'), 'rb'))[0]['image']
print(sr_sag.shape)
sr_sag = np.transpose(sr_sag, (2,1,0))
sr_cor = np.clip(sr_cor, 0, 4000).round().astype('uint16')
sr_sag = np.clip(sr_sag, 0, 4000).round().astype('uint16')
hr = pickle.load(open(sys.argv[2], 'rb'))
print(hr.shape)
hr_folder = os.path.join(sys.argv[3], 'HR')
sr_sag_folder = os.path.join(sys.argv[3], 'SR_sag')
sr_cor_folder = os.path.join(sys.argv[3], 'SR_cor')

for i in range(hr.shape[2]):
    scipy.misc.imsave(os.path.join(hr_folder, str(i)+'.png'), hr[:,:,i])
    scipy.misc.imsave(os.path.join(sr_sag_folder, str(i) + '.png'), sr_sag[:, i, :])
    scipy.misc.imsave(os.path.join(sr_cor_folder, str(i) + '.png'), sr_cor[:, i, :])


