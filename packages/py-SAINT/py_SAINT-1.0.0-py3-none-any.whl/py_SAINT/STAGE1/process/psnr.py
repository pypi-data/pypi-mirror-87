import pickle, sys, os, scipy.misc
from scipy.ndimage import zoom
from skimage.measure import compare_psnr
import numpy as np
files = os.listdir(sys.argv[1])
bi_psnr_all = 0
sr_psnr_all = 0
count = 0
for file in files:
    if 'HR' in file:
        count = count + 1
        print(file)
        hr = pickle.load(open(os.path.join(sys.argv[1], file), 'rb'))[0]['image']
        lr = pickle.load(open(os.path.join(sys.argv[1], file.replace('HR', 'LR')), 'rb'))[0]['image']
        sr = pickle.load(open(os.path.join(sys.argv[1], file.replace('HR', 'SR')), 'rb'))[0]['image']
        hr = np.clip(hr / 4000, 0, 1)
        lr = zoom(np.clip(lr / 4000, 0, 1), (1, 4, 1))
        sr = np.clip(sr / 4000, 0, 1)
        print('shapes: ', hr.shape, lr.shape, sr.shape)
        bi_psnr = np.round(compare_psnr(hr, lr), 2)
        sr_psnr = np.round(compare_psnr(hr, sr), 2)
        print("for case: ", file, " LR interpolate PSNR: ", bi_psnr, " SR PSNR: ", sr_psnr)
        bi_psnr_all = bi_psnr_all + bi_psnr
        sr_psnr_all = sr_psnr_all + sr_psnr

print("overall LR interpolate PSNR: ", bi_psnr_all/count, " SR PSNR: ", sr_psnr_all/count)

