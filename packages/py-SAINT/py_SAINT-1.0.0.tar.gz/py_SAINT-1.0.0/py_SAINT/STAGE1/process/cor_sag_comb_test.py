
# arg1 is input HR, arg2 is input cor\sag dir, arg3 is output dir argv[4] is scale
import sys, os, pickle
import numpy as np

def comb_cor_sag(files_dir,input_sag_cor_dir,out_dir, scale):
    files_temp = os.listdir(files_dir)
    files = []
    for file in files_temp:
        files.append(file)
        #if 'case' in file:
        #   files.append(file)
    output_HR = os.path.join(out_dir, 'HR')
    output_LR = os.path.join(out_dir, 'LR')
    if not os.path.exists(output_LR): os.makedirs(output_LR)
    if not os.path.exists(output_HR): os.makedirs(output_HR)
    # scale = sys.argv[4]
    for file in files:
        hr = pickle.load(open(os.path.join(files_dir, file),'rb'))['image']
        sr_cor = pickle.load(open(os.path.join(input_sag_cor_dir, file.replace('.pt','_cor_x{}_SR.pt'.format(scale))),'rb'))
        sr_sag = pickle.load(open(os.path.join(input_sag_cor_dir, file.replace('.pt','_sag_x{}_SR.pt'.format(scale))),'rb'))
        print("sr_cor min max",sr_cor.min(),sr_cor.max())
        #sr_cor = np.clip(sr_cor, 0, 4000).round().astype('uint16')
        #sr_sag = np.clip(sr_sag, 0, 4000).round().astype('uint16')
        print(sr_cor.shape, sr_sag.shape)
        pickle.dump(hr, open(os.path.join(output_HR, file), 'wb'))
        holder = np.zeros((2, sr_cor.shape[0], sr_cor.shape[1], sr_cor.shape[2])).astype('int16')
        holder[0] = np.transpose(sr_cor, (0,1, 2))
        holder[1] = np.transpose(sr_sag, (0,1, 2))
        pickle.dump(holder, open(os.path.join(output_LR, file), 'wb'))
        print("holder min max",holder.min(),holder.max())
        # print(file, hr.shape, holder.shape)
        #with open(os.path.join(output_LR, file),"rb") as f:
        #    img = pickle.load(f)
        #    print("mk---!!!!!!!",img.min(),img.max())
    print('complete')
#comb_cor_sag(files_dir='/home1/mksun/SAINT/Data/Stage1_Input/TEST/HR/',input_sag_cor_dir='/home1/mksun/SAINT/Data/Stage1_output_sag_cor/results/raw/',out_dir='/home1/mksun/SAINT/Data/combine_cor_sag_out/TEST/', scale=4)