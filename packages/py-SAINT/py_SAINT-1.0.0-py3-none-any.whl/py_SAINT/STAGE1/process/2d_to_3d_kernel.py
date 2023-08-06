import pickle, torch
import sys

device = torch.device('cuda')
params = torch.load('/home/cheng/CT_DSI/experiment/META_MULTI_3_CHANNEL_X234/model/model_best.pt')
params['SFENet1.weight'] = params['SFENet1.weight'].view(64, -1, 3, 3, 3)
for key in params.keys():
    if len(params[key].shape) == 4 and 'GW' not in key:
        if params[key].shape[-1] == 3:
            weights = params[key]
            new_weights = torch.zeros(params[key].shape[0], params[key].shape[1], params[key].shape[2], params[key].shape[3], params[key].shape[3]).type('torch.cuda.FloatTensor').to(device)
            new_weights[:,:,1,:,:] = weights
            params[key] = new_weights
            print('kernel size 3: ', params[key].shape[0], params[key].shape[1], params[key].shape[2], params[key].shape[3], params[key].shape[4])
        else:
            params[key] = params[key].view(params[key].shape[0], params[key].shape[1], params[key].shape[2], params[key].shape[2], params[key].shape[3])
            print('kernel size 1: ', params[key].shape[0], params[key].shape[1], params[key].shape[2], params[key].shape[3], params[key].shape[4])

for key in params.keys():
    print(params[key].shape)

torch.save(params, '/home/cheng/CT_DSI/DSI_3DCNN/3D_SAINT_X2_new.pt')





# params_x4 = torch.load('/home/cheng/CT_DSI/experiment/xxxtest/model/model_latest.pt')
# params_multi = torch.load('/home/cheng/CT_DSI/experiment/3slice_meta_multi_extra_x234/model/model_latest_x6.pt')
# meta_weights = pickle.load(open('/home/cheng/CT_DSI/DSI/weights.pt','rb'))
#
# multi_keys = list(params_multi.keys())
# x4_keys = list(params_multi.keys())
#
# for key in x4_keys:
#     if key in multi_keys:
#         print(key)
#         params_x4[key] = params_multi[key]
#
# params_x4['OutLayer1.weight'] = meta_weights[0,[0]]
# params_x4['OutLayer2.weight'] = meta_weights[0,[1]]
# params_x4['OutLayer3.weight'] = meta_weights[0,[2]]
# params_x4['OutLayer4.weight'] = meta_weights[0,[3]]

# torch.save(params_x4, '/home/cheng/CT_DSI/experiment/xxxtest/model/model_filled.pt')