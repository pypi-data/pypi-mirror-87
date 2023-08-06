import pickle, os, sys

hr_dir = os.path.join(sys.argv[1], 'HR')
files = os.listdir(hr_dir)
for file in files:
    hr = pickle.load(open(os.path.join(hr_dir, file),'rb'))
    lr = pickle.load(open(os.path.join(hr_dir.replace('HR','LR'), file), 'rb'))
    if hr.shape[0] == lr.shape[0] and lr.shape[0] == 512 and hr.shape[1] == 128 and lr.shape[1] == 32:
        continue
    else:
        print(file)
        print(hr.shape, lr.shape)