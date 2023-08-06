#argv[1] is input pt dir; argv[2] is output nii dir 
import pickle
import SimpleITK as sitk
import numpy as np
import glob
import sys 
import os


# def nii2pt(ori_dir_path,output_file_path):
#     if not os.path.exists(output_file_path): os.makedirs(output_file_path)
#     file_list = sorted(glob.glob(os.path.join(ori_dir_path, '*.nii.gz')))
#     for ori_f_path in file_list:
#         ori_img = sitk.ReadImage(ori_f_path)
#         ori_image = sitk.GetArrayFromImage(ori_img)
#         ori_image = np.transpose(ori_image,[1,2,0])
#         print(ori_image.shape,ori_img.GetSpacing())
#     #spacing = (ori_img.GetSpacing()[2],ori_img.GetSpacing()[0],ori_img.GetSpacing()[1])
#         pic_dic = {"image":ori_image,"spacing":ori_img.GetSpacing()}
#         ori_f_name = ori_f_path.split('/')[-1].split('.')[0]
#         with open(os.path.join(output_file_path,ori_f_name+".pt"),"wb") as f:
#             pickle.dump(pic_dic,f)
def pt2nii(ori_nii_dir_path, pt_dir_path,nii_dir_path,spacing=4):
    if not os.path.exists(nii_dir_path): os.makedirs(nii_dir_path)
    pt_dirs = sorted(glob.glob(os.path.join(pt_dir_path,'*.pt')))
    print(pt_dirs)
    #for pt_file_path in pt_dirs:
    #     pt_file_name = pt_file_path.split('/')[-1].split('.')[0]
    #     with open(pt_file_path,'rb') as f:
    #         img_np = pickle.load(f).transpose([2,0,1])
    #         save_img = sitk.GetImageFromArray(img_np)
    #         save_img.SetSpacing((1.0,1.0,5.0))
    #         sitk.WriteImage(save_img,os.path.join(nii_dir_path,pt_file_name+".nii.gz"))
    for pt_file_path in pt_dirs:
        pt_file_name = pt_file_path.split('/')[-1].split('.')[0]
        
        ori_file_path = os.path.join(ori_nii_dir_path,pt_file_name[:-6]+'.nii.gz')
        #print(ori_file_path)
        with open(pt_file_path,'rb') as f:
            ori_img = sitk.ReadImage(ori_file_path)
            img_np = pickle.load(f).transpose([2,0,1])
            save_img = sitk.GetImageFromArray(img_np)
            save_img.SetSpacing(ori_img.GetSpacing())
            sitk.WriteImage(save_img,os.path.join(nii_dir_path,pt_file_name+".nii.gz"))

# pt2nii(ori_nii_dir_path='/home1/mksun/xh_data/273data-yscl/1T2/1/002_OCor_T2_FRFSE/',pt_dir_path='/home1/mksun/SAINT/Data/out_fuse/results/raw/',nii_dir_path='/home1/mksun/SAINT/Data/final_nii/',spacing=4)