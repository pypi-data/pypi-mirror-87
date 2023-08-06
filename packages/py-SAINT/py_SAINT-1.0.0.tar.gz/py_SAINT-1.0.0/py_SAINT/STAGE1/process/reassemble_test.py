import os, pickle
import scipy.misc
import numpy as np
import torch

HR = torch.from_numpy(pickle.load(open('/home/cheng/CT_ALL/TRAIN/HR/liver_173_sag_3th_copy_337.pt','rb'))['image'].astype('int32')).view(1,1,512,128).float()
LR = HR[...,::4]

# other = torch.zeros(1,3,512,32).float()
zero = HR[...,1:][...,::4]
one = HR[...,2:][...,::4]
two = HR[...,3:][...,::4]
output = torch.cat((LR,zero,one,two),3)

scipy.misc.imsave('/home/cheng/testtesttest.png', output.numpy()[0][0])