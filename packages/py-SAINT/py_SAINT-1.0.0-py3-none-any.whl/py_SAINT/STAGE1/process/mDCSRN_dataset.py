# existing 3D HR, output dir (LR), factor
import os, pickle
from scipy.ndimage import zoom
from skimage.measure import compare_psnr
import numpy as np
factor = int(sys.argv[3])
files = os.listdir(sys.argv[1])
for file in files:
    print('start: ', file)
    data = pickle.load(open(os.path.join(sys.argv[1], file),'rb'))
    dwn = data[...,::factor]
    dwn = np.clip(zoom(dwn, (1,1,factor)), 0,4000).round().astype('uint16')
    print(compare_psnr(data.astype(float)/4000, dwn.astype(float)/4000))
    pickle.dump(dwn, open(os.path.join(sys.argv[2], file),'wb'))
    print('finished: ', file)