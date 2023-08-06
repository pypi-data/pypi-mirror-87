#arg 1 is the directory for processed lung data folder, arg2 is the directory for original data
import pydicom
import pickle, os, sys

files = os.listdir(sys.argv[1])
output = {}
for file in files:
    name = file.replace('.pt','')
    folder = os.path.join(sys.argv[2], name)
    folder = os.path.join(folder, os.listdir(folder)[0])
    folder1 = os.path.join(folder, os.listdir(folder)[0])
    folder2 = os.path.join(folder, os.listdir(folder)[1])
    if len(os.listdir(folder1)) != 1:
        # print(os.listdir(folder1))
        path = folder1
    else:
        path = folder2
    # print(path)
    dicoms = os.listdir(path)
    dm = pydicom.dcmread(os.path.join(path,dicoms[len(dicoms)//2]))
    spacing = dm.PixelSpacing
    spacing.append(dm.SliceThickness)
    output[name] = spacing
pickle.dump(output, open('/data/cheng/CT/spacing.pt','wb'))




