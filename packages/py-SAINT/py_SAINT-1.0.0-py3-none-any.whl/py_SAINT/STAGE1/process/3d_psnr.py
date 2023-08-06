## 1st arg LR path, 2nd arg factor, 3rd arg range low, 4th arg range high

import pickle, sys, os
import numpy as np
from skimage.measure import compare_psnr, compare_ssim

HR_path = '/data/cheng/CT_DATASET/TEST_orig/TEST/HR/'
files = os.listdir(HR_path)
liver = []
vessel = []
colon = []
kidney = []
factor = int(sys.argv[2])
for file in files:
    #     lr = np.transpose(pickle.load(open(os.path.join(sys.argv[1], file.replace('.pt','_x'+sys.argv[2]+'_SR.pt')),'rb')),(2,0,1))
        # lr = np.transpose(
        # if 'case' in file:
        lr = pickle.load(open(os.path.join(sys.argv[1], file.replace('.pt', '_x4_SR.pt')), 'rb'))#.transpose(1,2,0)\
        # else:
        #     lr = pickle.load(open(os.path.join(sys.argv[1], file.replace('.pt', '_x6_x4_SR.pt')), 'rb'))#.transpose(1,2,0)\
        #     pickle.load(open(os.path.join(sys.argv[1], file), 'rb'))[1],
        #     (2, 0, 1))

        print(file, lr.shape)
        hr = pickle.load(open(os.path.join(HR_path, file),'rb'))['image']
        hr = hr[...,hr.shape[2]%factor:]
        lr, hr = lr.astype(float)/4000, hr.astype(float)/4000
        lr, hr = np.delete(lr, np.s_[::factor], axis=2)[128:384,128:384], np.delete(hr, np.s_[::factor], axis=2)[128:384,128:384]
        print(file, lr.shape, hr.shape)
        slice_num = hr.shape[0]
        psnr = compare_psnr(hr, lr)
        ssim = compare_ssim(hr, lr)
        print(psnr, ssim)
        if 'liver' in file:
            liver.append([psnr, ssim, slice_num])
        elif 'colon' in file:
            colon.append([psnr, ssim, slice_num])
        elif 'vessel' in file:
            vessel.append([psnr, ssim, slice_num])
        elif 'case' in file:
            kidney.append([psnr, ssim, slice_num])

liver_val = [0,0]
vessel_val = [0,0]
colon_val = [0,0]
kidney_val = [0,0]
liver_count = 0
colon_count = 0
vessel_count = 0
kidney_count = 0
for psnr, ssim, num in liver:
    liver_val[0] = psnr*num + liver_val[0]
    liver_val[1] = ssim*num + liver_val[1]
    liver_count = liver_count + num
liver_val[0], liver_val[1] = liver_val[0]/liver_count, liver_val[1]/liver_count

for psnr, ssim, num in vessel:
    vessel_val[0] = psnr*num + vessel_val[0]
    vessel_val[1] = ssim*num + vessel_val[1]
    vessel_count = vessel_count + num
vessel_val[0], vessel_val[1] = vessel_val[0]/vessel_count, vessel_val[1]/vessel_count

for psnr, ssim, num in colon:
    colon_val[0] = psnr*num + colon_val[0]
    colon_val[1] = ssim*num + colon_val[1]
    colon_count = colon_count + num
colon_val[0], colon_val[1] = colon_val[0]/colon_count, colon_val[1]/colon_count

for psnr, ssim, num in kidney:
    kidney_val[0] = psnr*num + kidney_val[0]
    kidney_val[1] = ssim*num + kidney_val[1]
    kidney_count = kidney_count + num
kidney_val[0], kidney_val[1] = kidney_val[0]/kidney_count, kidney_val[1]/kidney_count

total_count = liver_count+colon_count+vessel_count
print(liver_val, liver_count)
print(colon_val, colon_count)
print(vessel_val, vessel_count)
print(kidney_val, kidney_count)
# print((liver_psnr*liver_count+colon_psnr*colon_count+vessel_psnr*vessel_count)/total_count)