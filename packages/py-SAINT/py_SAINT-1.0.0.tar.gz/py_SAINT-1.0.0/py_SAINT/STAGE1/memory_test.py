import torch, pickle
from option import args
import utility
import model
import numpy as np

device = torch.device('cuda')
checkpoint = utility.checkpoint(args)

args.RDNconfig='D'
args.model='baseline3d_rdn'
args.n_colors=1
args.rgb_range=4000
args.pre_train='/home/cheng/CT_DSI/DSI_3DCNN/model_latest_x4.pt'

with torch.no_grad():
    test = pickle.load(open('/data/cheng/CT_DATASET/TEST/TEST/HR/colon_170.pt','rb'))['image']
    test = test.transpose(2,0,1).astype('int32')
    test = np.ascontiguousarray(test)
    test = torch.from_numpy(test).float()
    test = test.view(1,1,48,512,512).to(device)
    model = model.Model(args, checkpoint).to(device)
    x, f__1 = model(test,None,'first',4)
    del f__1
    del test
    children = list(model.modules())
    out = children[10](children[9](x))
    x, out = x.cpu(), out.cpu()
    x = torch.cat((x,out),1).to(device)
    out = children[14](children[13](x))
    x, out = x.cpu(), out.cpu()
    x = torch.cat((x,out),1).to(device)
    out = children[18](children[17](x))
    x, out = x.cpu(), out.cpu()
    x = torch.cat((x,out),1).to(device)
    out = children[22](children[21](x))