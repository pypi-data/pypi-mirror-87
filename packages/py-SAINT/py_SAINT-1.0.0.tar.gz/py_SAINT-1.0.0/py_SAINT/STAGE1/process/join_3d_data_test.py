##input dir, output dir
import pickle, os, sys
import numpy as np
# files = ['liver_75', 'liver_72', 'liver_42', 'liver_199', 'liver_147', 'liver_53', 'liver_152', 'liver_143', 'liver_137', 'liver_35', 'liver_176', 'liver_73', 'liver_45', 'liver_46', 'liver_44', 'liver_170', 'liver_63', 'liver_54', 'liver_37', 'liver_140', 'liver_200', 'liver_66', 'liver_149', 'liver_71', 'liver_150', 'liver_148', 'liver_153', 'liver_169', 'liver_0', 'liver_41', 'liver_31', 'liver_36', 'liver_1', 'liver_138', 'liver_77', 'liver_74', 'liver_136', 'liver_40']
files = ['liver_0']
for file in files:
    data = pickle.load(open(os.path.join(sys.argv[1], file+'_0_0_x1_SR.pt'),'rb'))
    output = np.zeros((512,512,data.shape[3]*4))
    print(output.shape)
    for i in range(8):
        for j in range(8):
            path = os.path.join(sys.argv[1], file+'_'+str(j)+'_'+str(i)+'_x1_SR.pt')
            data = pickle.load(open(path,'rb'))
            print(data.shape)
            new_data = np.zeros((70,70,72))
            new_data[...,::4] = data[0]
            new_data[...,1:][...,::4] = data[1]
            new_data[...,2:][...,::4] = data[2]
            new_data[...,3:][...,::4] = data[3]
            output[i*64:(i+1)*64, j*64:(j+1)*64] = new_data[3:-3,3:-3]
    pickle.dump(output, open(os.path.join(sys.argv[2], file+'_recon.pt'), 'wb'))
    print('finished: ', file)