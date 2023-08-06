import pickle, os
import numpy as np
path = '/home/cheng/kits19/KIDNEY_dirty/TEST/HR/'
out_dir = '/home/cheng/kits19/KIDNEY_dirty_2D/'
files = os.listdir(path)
for file in files:
    if 'case' in file:
        print(file)
        name = file.replace('.pt','')
        data = pickle.load(open(path+file,'rb'))
        data['image'] = data['image'][...,data['image'].shape[-1]%4:]

        print(data['image'].shape, data['spacing'])

        for i in range(512):
            holder = {}
            holder['spacing'] = data['spacing']
            if i == 0:
                temp = np.zeros((3,512,data['image'].shape[-1])).astype('uint16')
                temp[1:] = data['image'][:2]
                holder['image'] = temp
            elif i == 511:
                temp = np.zeros((3, 512, data['image'].shape[-1])).astype('uint16')
                temp[:2] = data['image'][i-1:]
                holder['image'] = temp
            else:
                holder['image'] = data['image'][i-1:i+2]
            pickle.dump(holder, open(out_dir+'TEST/HR/'+name+'_cor_'+str(i)+'.pt','wb'))


        for i in range(512):
            holder = {}
            holder['spacing'] = data['spacing']
            if i == 0:
                temp = np.zeros((3,512,data['image'].shape[-1])).astype('uint16')
                temp[1:] = data['image'][:,:2].transpose(1,0,2)
                holder['image'] = temp
            elif i == 511:
                temp = np.zeros((3, 512, data['image'].shape[-1])).astype('uint16')
                temp[:2] = data['image'][:,i-1:].transpose(1,0,2)
                holder['image'] = temp
            else:
                holder['image'] = data['image'][:,i-1:i+2].transpose(1,0,2)
            pickle.dump(holder, open(out_dir+'/TEST/HR/'+name+'_sag_'+str(i)+'.pt','wb'))


        data['image'] = data['image'][...,::2]
        data['spacing'] = list(data['spacing'])
        data['spacing'][2] = data['spacing'][2]*2
    
        print(data['image'].shape, data['spacing'])

        for i in range(512):
            holder = {}
            holder['spacing'] = data['spacing']
            if i == 0:
                temp = np.zeros((3,512,data['image'].shape[-1])).astype('uint16')
                temp[1:] = data['image'][:2]
                holder['image'] = temp
            elif i == 511:
                temp = np.zeros((3, 512, data['image'].shape[-1])).astype('uint16')
                temp[:2] = data['image'][i-1:]
                holder['image'] = temp
            else:
                holder['image'] = data['image'][i-1:i+2]
            pickle.dump(holder, open(out_dir+'/TRAIN/HR/'+name+'_cor_'+str(i)+'.pt','wb'))


        for i in range(512):
            holder = {}
            holder['spacing'] = data['spacing']
            if i == 0:
                temp = np.zeros((3,512,data['image'].shape[-1])).astype('uint16')
                temp[1:] = data['image'][:,:2].transpose(1,0,2)
                holder['image'] = temp
            elif i == 511:
                temp = np.zeros((3, 512, data['image'].shape[-1])).astype('uint16')
                temp[:2] = data['image'][:,i-1:].transpose(1,0,2)
                holder['image'] = temp
            else:
                holder['image'] = data['image'][:,i-1:i+2].transpose(1,0,2)
            pickle.dump(holder, open(out_dir+'/TRAIN/HR/'+name+'_sag_'+str(i)+'.pt','wb'))
        print('finished')