# arg 1 input dir, arg2 output dir, arg3, train or test
from medpy.io import load
import sys, os, pickle
import numpy as np

if 'Tr' in sys.argv[3]:
    file_dir = os.path.join(sys.argv[1], 'imagesTr')
else:
    file_dir = os.path.join(sys.argv[1], 'imagesTs')
patients = os.listdir(file_dir)
for patient in patients:
    img, _ = load(os.path.join(file_dir, patient))
    if img.max().astype(float) - img.min().astype(float) > 9000:
        print("possible metal artifact: " + patient + " , HU: range" + str(img.max().astype(float) - img.min().astype(float)))
        continue
    if 'Tr' in sys.argv[3]:
        # 0 is background, 1 is liver, 2 is tumor
        label, _ = load(os.path.join(file_dir.replace('imagesTr', 'labelsTr'), patient))
        img = img - img.min()
        img = np.clip(img, 0, 4000).astype("uint16")
        data = {'image': img, 'label': label}
        pickle.dump(data, open(os.path.join(sys.argv[2], patient.replace('.nii.gz','.pt')), 'wb'))
        print("finished, " + patient)
    else:
        img = img - img.min()
        img = np.clip(img, 0, 4000).astype("uint16")
        data = {'image': img}
        pickle.dump(data, open(os.path.join(sys.argv[2], patient.replace('.nii.gz','.pt')), 'wb'))
        print("finished, " + patient)