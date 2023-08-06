import torch
import pickle
import torch.nn.functional as F
import numpy as np
img = pickle.load(open('/data/cheng/CT_DATASET/TEST/TEST/HR/hepaticvessel_322.pt','rb'))['image']
img = img.transpose(2,0,1)
img = torch.from_numpy(img.astype(float)).float()
img = img.view(1,1,52,512,512)
weights = torch.zeros(1,1,3,3,3)
sobel = np.asarray([[1,0,-1],[2,0,-2],[1,0,-1]])
sobel = torch.from_numpy(sobel.astype(float)).float()
weights[...,1,:,:] = sobel

out3D = F.conv3d(img, weights,padding=1)
out2D = F.conv2d(img[...,0,:,:], weights[...,1,:,:],padding=1)

