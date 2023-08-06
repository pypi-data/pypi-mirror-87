import torch
import pickle
import sys
import os

cor_file = sys.argv[1]
sag_file = sys.argv[2]
out_dir = sys.argv[3]

with open(cor_file,'rb') as f:
    cor = torch.from_numpy(pickle.load(f))

with open(sag_file,'rb') as f:
    sag = torch.from_numpy(pickle.load(f))

#combine
comb = torch.cat([cor,sag],dim=0)

#with open(os.path.join(out_dir,"comb.pt"),'wb') as f:
#    pickle.dump(comb,f)
print("cor.shape={} sag.shape={} comb.shape={}".format(cor.shape,sag.shape,comb.shape))