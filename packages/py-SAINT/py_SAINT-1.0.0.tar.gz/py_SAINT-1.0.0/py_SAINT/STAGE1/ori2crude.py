import pickle
import SimpleITK as sitk
from matplotlib import pyplot as plt
import numpy as np
import glob
import os
import collections
import shutil
import sys 


def get_file_names(dir_path):
    file_names_paths = []
    for a, b, c in os.walk(dir_path):  
        for i in c:
            path = os.path.join(a,i)
            file_names_paths.append(path)
    return file_names_paths

def writeCrudeNii(ori_file_path,factor,out_dir,ori_file_name):
    ori_img = sitk.ReadImage(ori_file_path)
    ori_imgnp = sitk.GetArrayFromImage(ori_img)[::factor,...]
    crude_img = sitk.GetImageFromArray(ori_imgnp)
    crude_img.SetSpacing((ori_img.GetSpacing()[0],ori_img.GetSpacing()[1],ori_img.GetSpacing()[2]*factor))
    #print(path.split('.')[0]+'lr_'+'x'+str(factor))
    sitk.WriteImage(crude_img,os.path.join(out_dir,ori_file_name+'_lr_'+'x'+str(factor)+'.nii.gz'))
    
ori_file_path = sys.argv[1]
factor = int(sys.argv[2])
out_dir_pre = sys.argv[3]
ori_file_paths = get_file_names(ori_file_path)
for file in ori_file_paths:
    if 'SR' not in file:
        ori_file_name = file.split('/')[-1].split('.')[0]
        out_dir = os.path.join(out_dir_pre,ori_file_name)
        writeCrudeNii(file,factor,out_dir,ori_file_name)
        #print(file,factor,out_dir,ori_file_name)
