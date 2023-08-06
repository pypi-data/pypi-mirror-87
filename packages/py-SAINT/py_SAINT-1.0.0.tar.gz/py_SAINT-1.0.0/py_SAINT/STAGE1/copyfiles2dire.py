import pickle
import SimpleITK as sitk
from matplotlib import pyplot as plt
import numpy as np
import glob
import os
import collections
import sys
import shutil

#argv[1]=input dir argv[2]=output dir argv[3]=spacing

path = sys.argv[1]
new_path = sys.argv[2]
def get_file_names(path):
    file_names_paths = []
    for a, b, c in os.walk(path):  
        for i in c:
            path = os.path.join(a,i)
            file_names_paths.append(path)
    return file_names_paths

file_paths = get_file_names(path)
spacing = float(sys.argv[3])
#print(file_paths)
for file in file_paths:
    if 'seg' not in file:
        sitk_img = sitk.ReadImage(file)
        sitk_img_np = sitk.GetArrayFromImage(sitk_img)
        if(round(sitk_img.GetSpacing()[2],1)==spacing):
            #print(file)
            #spacing_1mm_list.append(file)
            new_name = os.path.join(new_path,file.split('/')[-1])
            shutil.copyfile(file, new_name)


