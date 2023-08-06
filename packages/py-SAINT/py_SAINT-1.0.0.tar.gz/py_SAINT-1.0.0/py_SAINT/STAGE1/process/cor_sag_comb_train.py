# arg1 is input HR, arg2 is input cor, arg3 is input sag, arg4 is output dir, arg5 is combined slices

import sys, os, pickle
import numpy as np
files = os.listdir(sys.argv[1])
output_HR = os.path.join(sys.argv[4], 'HR')
output_LR = os.path.join(sys.argv[4], 'LR')
for file in files:
    hr = pickle.load(open(os.path.join(sys.argv[1], file),'rb'))
    sr_cor = pickle.load(open(os.path.join(sys.argv[2], file.replace('.pt','_x4_SR.pt')),'rb'))[0]['image']
    sr_sag = np.transpose(pickle.load(open(os.path.join(sys.argv[3], file.replace('.pt','_x4_SR.pt')),'rb'))[0]['image'], (2,1,0))
    sr_cor = np.clip(sr_cor, 0, 4000).round().astype('uint16')
    sr_sag = np.clip(sr_sag, 0, 4000).round().astype('uint16')

    for i in range(hr.shape[2]):
        if not i%4 == 0:
            pickle.dump(np.transpose(hr[:,:,[i]], (2,1,0)), open(os.path.join(output_HR, file.replace('.pt','_'+str(i)+'.pt')),'wb'))
            holder = np.zeros((2,512,512))
            holder[0] = sr_cor[:,i,:]
            holder[1] = sr_sag[:,i,:]
            pickle.dump(holder, open(os.path.join(output_LR, file.replace('.pt', '_' + str(i) + '.pt')), 'wb'))
    print(file)
print('complete')













