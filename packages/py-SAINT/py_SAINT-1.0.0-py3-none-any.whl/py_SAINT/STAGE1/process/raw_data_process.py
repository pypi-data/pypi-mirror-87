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
    if not '._' in patient:
        img, header = load(os.path.join(file_dir, patient))
        if img.max().astype(float) - img.min().astype(float) > 9000:
            print("possible metal artifact: " + patient + " , HU: range" + str(img.max().astype(float) - img.min().astype(float)))
            continue
        spacing = header.get_voxel_spacing()
        img = img - img.min()
        img = np.clip(img, 0, 4000).astype("uint16")
        data = {'image': img, 'spacing': spacing}
        if img.shape[2] >= int(sys.argv[4]):
            pickle.dump(data, open(os.path.join(sys.argv[2],'TRAIN', patient.replace('.nii.gz','.pt')), 'wb'))
            print("train finished, " + patient, img.shape)
        else:
            pickle.dump(data, open(os.path.join(sys.argv[2],'TEST', patient.replace('.nii.gz','.pt')), 'wb'))
            print("test finished, " + patient, img.shape)