## arg1 existing HR folder for old MSR_RDN, arg2 the spacing file, arg3 the output new HR
import pickle, sys, os
from medpy.io import load
import numpy as np

files = os.listdir(sys.argv[1])
spacing = pickle.load(open(sys.argv[2], 'rb'))
file_len = len(files)
for file in files[7*file_len//8:]:
    hr = pickle.load(open(os.path.join(sys.argv[1], file), 'rb'))
    lr = pickle.load(open(os.path.join(sys.argv[1].replace('HR','LR'), file), 'rb'))
    name = file.split('_')
    name = name[0]+ '_' +name[1]
    print(name, file)
    data = {}
    for i in range(3):
        data['image'] = hr[:, 1+i:][:, ::4]
        data['spacing'] = spacing[name]
        data['num'] = i+1
        output_path = os.path.join(sys.argv[3], file.replace('.pt','_part'+str(i)+'.pt'))
        pickle.dump(data, open(output_path, 'wb'))
        pickle.dump(lr, open(output_path.replace('HR','LR'), 'wb'))
    print(file, 'finished')

#python meta_dataset.py /data/cheng/CT_combine/TRAIN_GOOD/HR/ /data/cheng/liver/spacing.pt /data/cheng/CT_combine/TRAIN/HR/
