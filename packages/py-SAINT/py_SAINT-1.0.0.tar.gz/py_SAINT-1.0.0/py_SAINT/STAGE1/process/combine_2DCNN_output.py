## arg1 input folder, arg2 output pickle, arg3 scale, factor
import sys, os, pickle
import numpy as np
test_files = ['liver_0']
output_dir = sys.argv[2]
input_dir = sys.argv[1]
factor = int(sys.argv[4])
scale = sys.argv[3]
print(output_dir)
file_num = pickle.load(open('/data/cheng/liver/output/slice_num.pt','rb'))
for file in test_files:
    slice_num = file_num[file]
    slices = int(np.floor(slice_num/4))
    output = np.zeros((512,512,int(slices)*4-3))
    for slice in range(slices-1):
        lr = pickle.load(open(input_dir+file+'_ax_slice_'+str(slice*factor)+'_x'+scale+'_LR.pt','rb'))[0]['image']
        sr = pickle.load(open(input_dir+file+'_ax_slice_'+str(slice*factor)+'_x'+scale+'_SR.pt','rb'))[0]['image']
        if slice == 0:
            output[...,0] = lr[...,0]
            output[..., factor] = lr[..., 1]
            for i in range(factor-1):
                output[...,i+1] = sr[...,i]
        else:
            for i in range(factor-1):
                output[...,slice*factor + i+1] = sr[...,i]
            output[..., (slice+1)*factor] = lr[...,1]
    print("mk---combine_2DCNN_output output.min():",output.min())
    pickle.dump(np.clip(output, -1024, 4000).round().astype('uint16'),#mk---clip
                open(os.path.join(output_dir, file + '_cor_sr.pt'), 'wb'))
    print('finished ', file)