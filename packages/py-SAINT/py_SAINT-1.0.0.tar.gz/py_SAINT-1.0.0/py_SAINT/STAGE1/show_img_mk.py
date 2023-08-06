from matplotlib import pyplot as plt
import os
import sys
import SimpleITK as sitk
import pickle
import numpy as np

def showNii(img,axis):
    for i in range(img.shape[axis]):
        plt.imshow(img[i,:,:] if axis==0 else img[:,:,i],cmap='gray')
        plt.show()
            
file_tpye = sys.argv[1]    #file_tpye=1:nii  file_tpye=2:pt        
axis = int(sys.argv[2])  #axis=0:shape[0]=slicer axis=2:shape[2]=slicer
file_path = sys.argv[3]

if file_tpye=='nii':
    img = sitk.ReadImage(file_path)
    img_np = sitk.GetArrayFromImage(img)
   
elif file_tpye=='pt':
    with open(file_path,"rb") as f:
        img_np = pickle.load(f)

print(img_np.shape)
print(img_np.min(),img_np.max())
showNii(img_np,axis)
    
#itk_img = sitk.ReadImage(img)
#image = sitk.GetArrayFromImage(itk_img)

