import pickle, os
import numpy as np

filename = '/data/cheng/liver/pickleTr/liver_1.pt'
file = 'liver_1'
output_path_HR = '/data/cheng/CT_combine/EXP/HR'
data = pickle.load(open(filename, 'rb'))['image']
data = np.transpose(data, (2, 0, 1))
lr_data = data[..., ::4]
for i in range(512):
    pickle.dump(data[...,i], open(os.path.join(output_path_HR, file+str(i)+'.pt'), 'wb'))
    pickle.dump(lr_data[...,i], open(os.path.join(output_path_HR.replace('HR','LR'), file + str(i) + '.pt'), 'wb'))

print('finished.')