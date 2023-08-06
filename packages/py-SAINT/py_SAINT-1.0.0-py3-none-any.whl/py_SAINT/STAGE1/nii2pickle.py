# arg1 is input_dir, arg2 is output_file_path
import pickle
import SimpleITK as sitk
import sys
import numpy as np
import glob
import os


def nii2pt(ori_dir_path,output_file_path):
    if not os.path.exists(output_file_path): os.makedirs(output_file_path)
    file_list = sorted(glob.glob(os.path.join(ori_dir_path, '*.nii.gz')))
    for ori_f_path in file_list:
        ori_img = sitk.ReadImage(ori_f_path)
        ori_image = sitk.GetArrayFromImage(ori_img)
        ori_image = np.transpose(ori_image,[1,2,0])
        print(ori_image.shape,ori_img.GetSpacing())
    #spacing = (ori_img.GetSpacing()[2],ori_img.GetSpacing()[0],ori_img.GetSpacing()[1])
        pic_dic = {"image":ori_image,"spacing":ori_img.GetSpacing()}
        ori_f_name = ori_f_path.split('/')[-1].split('.')[0]
        with open(os.path.join(output_file_path,ori_f_name+".pt"),"wb") as f:
            pickle.dump(pic_dic,f)