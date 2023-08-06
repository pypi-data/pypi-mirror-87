import glob
import os
import sys
import shutil

#argv[1]=ori_path  argv[2]=chazhi_patch argv[3]=mkdir_path

ori_path = sys.argv[1]
chazhi_path = sys.argv[2]
mkdir_path = sys.argv[3]

ori_list = glob.glob(os.path.join(ori_path,'*.nii.gz'))
chazhi_list = glob.glob(os.path.join(chazhi_path,'*.nii.gz'))
#print(chazhi_list)
for ori in ori_list:
    for chazhi in chazhi_list:
        ori_full_name = ori.split('/')[-1]
        ori_name = ori_full_name.split('.')[0]
        chazhi_full_name = chazhi.split('/')[-1]
        chazhi_name = chazhi_full_name.split('_')[0]
        if ori_name ==chazhi_name:
            dir_name =os.path.join(mkdir_path,ori_name)
            if not os.path.exists(dir_name):
                os.mkdir(dir_name) 
            ori_new_name = os.path.join(dir_name,ori_full_name)
            chazhi_new_name = os.path.join(dir_name,chazhi_full_name)
            shutil.copyfile(ori, ori_new_name)
            shutil.copyfile(chazhi, chazhi_new_name)