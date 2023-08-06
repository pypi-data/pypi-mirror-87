# user input the directory for Lung dataset ("LCTSC/") on first argument
import pydicom
from skimage.draw import polygon
import matplotlib.pyplot as plt
import sys, os, glob
import numpy as np
import pickle

def read_structure(structure):
    # print("hello,sdsd")
    contours = []
    for i in range(len(structure.ROIContourSequence)):
        # print("hello,"+structure.ROIContourSequence[i].ROINumber)
        contour = {}
        contour['color'] = structure.ROIContourSequence[i].ROIDisplayColor
        contour['number'] = i+1
        contour['name'] = structure.StructureSetROISequence[i].ROIName
        # assert contour['number'] == structure.StructureSetROISequence[i].ROINumber
        contour['contours'] = [s.ContourData for s in structure.ROIContourSequence[i].ContourSequence]
        contours.append(contour)
    return contours


def get_mask(contours, slices):
    z = [s.ImagePositionPatient[2] for s in slices]
    zNew = [round(elem, 1) for elem in z]
    pos_r = slices[0].ImagePositionPatient[1]
    spacing_r = slices[0].PixelSpacing[1]
    pos_c = slices[0].ImagePositionPatient[0]
    spacing_c = slices[0].PixelSpacing[0]
    label = np.zeros_like(image, dtype=np.uint8)
    for con in contours:
        num = int(con['number'])
        for c in con['contours']:
            nodes = np.array(c).reshape((-1, 3))
            assert np.amax(np.abs(np.diff(nodes[:, 2]))) == 0
            try:
                z_index = z.index(nodes[0, 2])
            except ValueError:
                z_index = zNew.index(np.around(nodes[0, 2], 1))
            r = (nodes[:, 1] - pos_r) / spacing_r
            c = (nodes[:, 0] - pos_c) / spacing_c
            rr, cc = polygon(r, c)
            label[rr, cc, z_index] = num
    colors = tuple(np.array([con['color'] for con in contours]) / 255.0)
    return label, colors


train_data_path = sys.argv[1]
print(train_data_path)
train_patients = [os.path.join(train_data_path, name) for name in os.listdir(train_data_path) if os.path.isdir(
    os.path.join(train_data_path, name))]

for patient in train_patients:
    print(patient)
    flag = 0
    for subdir, dirs, files in os.walk(patient):
        dcms = glob.glob(os.path.join(subdir, "*.dcm"))
        if len(dcms) == 1:
            structure = pydicom.read_file(os.path.join(subdir, files[0]))
            contours = read_structure(structure)
        elif len(dcms) > 1:
            slices = [pydicom.read_file(dcm) for dcm in dcms]
            slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
            # image is uint16, not considering overflow here
            image = np.stack([s.pixel_array for s in slices], axis=-1)
            print(image.max().astype(float) - image.min().astype(float), patient)
            if image.max().astype(float) - image.min().astype(float) > 9000:
                print("possible metal artifact: "+patient+" , HU range: "+str(image.max().astype(float) - image.min()))
                flag = 1
    label, _ = get_mask(contours, slices)
    if image.min() == -2048:
        image = np.clip(image, -1024,image.max())
    image = image - image.min()
    image = np.clip(image, 0, 4000)
    if flag == 0:
        data = {'image': image, 'label': label}
        # pickle.dump(data, open(os.path.join(sys.argv[2], patient.split('/')[-1]+'.pt'), 'wb'))
        print("finished, "+patient)
