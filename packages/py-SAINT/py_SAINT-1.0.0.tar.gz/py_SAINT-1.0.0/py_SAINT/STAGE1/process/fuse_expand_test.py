import pickle, os, sys
import numpy as np
input_lr_dir = '/home/cheng/CT_DSI/experiment/MRA_x4/results/raw/'
# input_lr_dir_sag = '/data/cheng/experiment/META_MULTI_THICKBOI_TEST_sag/results/raw/'
input_hr_dir = '/home/cheng/MRA/MRA/TEST/HR/'
# input_lr_slant_dir = '/home/cheng/CT_DSI/experiment/SAINT_X2/results/raw/'
output_lr_dir = '/home/cheng/MRA_x4/TEST/LR/'
# output_hr_dir = '/home/cheng/FUSE_x6/TEST/HR/'
# files = os.listdir(input_hr_dir)
# files = ['TOF3D-_844_5_9.pt','TOF3D-_984_3_9.pt']
files= ['TOF3D-_630_1_9.pt', 'TOF3D-_790_1_9.pt', 'TOF3D-_542_3_9.pt', 'TOF3D-678_5_10.pt', 'TOF3D-170_3_18.pt', 'TOF3D-_065_1_9.pt', 'TOF3D-_748_9_9.pt', 'TOF3D-117_1_10.pt', 'TOF3D-_747_4_8.pt', 'TOF3D-1_9_10_1.pt', 'TOF3D-_300_6_4.pt', 'TOF3D-779_4_15.pt', 'TOF3D-_209_7_9.pt', 'TOF3D-072_9_22.pt', 'TOF3D-549_8_10.pt', 'TOF3D-251_4_25.pt', 'TOF3D-_614_7_9.pt', 'TOF3D-147_8_11.pt']
length = len(files)
# temp = {0: 'hepaticvessel_432.pt',1: 'hepaticvessel_304.pt',2: 'liver_90.pt', 3: 'liver_120.pt'}
flag = False
for file in files:
    print(file)
    # if not flag:
    #     print(temp[quartile])
    #     if file == temp[quartile]:
    #         flag = True
    #     else:
    #         continue
    # hr = pickle.load(open(input_hr_dir + file,'rb'))['image']
    lr_cor = np.expand_dims(pickle.load(open(input_lr_dir + file.replace('.pt','_cor_x4_SR.pt'),'rb')),axis=0)
    lr_sag = np.expand_dims(pickle.load(open(input_lr_dir + file.replace('.pt','_sag_x4_SR.pt'),'rb')),axis=0)
    # lr_one = np.expand_dims(pickle.load(open(input_lr_slant_dir + file.replace('.pt','_one_x6_SR.pt'),'rb')),axis=0)
    # lr_two = np.expand_dims(pickle.load(open(input_lr_slant_dir + file.replace('.pt','_two_x6_SR.pt'),'rb')),axis=0)
    lr = np.concatenate((lr_cor,lr_sag),0)
    # hr = hr[..., hr.shape[2]%factor:]
    print(lr.shape)
    pickle.dump(lr,open(output_lr_dir + file, 'wb'))
    # pickle.dump(hr,open(output_hr_dir + file, 'wb'))
    print('finish: ', file)
