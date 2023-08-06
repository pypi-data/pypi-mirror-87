#arg1 HR, arg2 spacing file, arg3 output
#python meta_dataset_test.py /data/cheng/CT_combine/TEST_OLD/HR/ /data/cheng/liver/spacing.pt /data/cheng/CT_combine/TEST/

import sys, os, pickle
files = os.listdir(sys.argv[1])
spacing = pickle.load(open(sys.argv[2], 'rb'))

for file in files:
    print(file)
    hr = pickle.load(open(os.path.join(sys.argv[1], file),'rb'))
    data = {}
    data['spacing'] = spacing[file.replace('.pt','')]
    lr = hr[...,::4]
    for i in range(512):
        for j in range(3):
            name = os.path.join(sys.argv[3], 'LR', file.replace('.pt', '_sag_'+str(i)+'_part_'+str(j)+'.pt'))
            pickle.dump(lr[:,i,:], open(name,'wb'))
            data['num'] = j+1
            data['image'] = hr[:, i, 1+j:][:,::4]
            pickle.dump(data, open(name.replace('LR', 'HR'), 'wb'))
    print('finished')
