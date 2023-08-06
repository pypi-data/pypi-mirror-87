## input dir, output dir
import pickle, os, sys
import numpy as np
margin = 3
files = os.listdir(sys.argv[1])
for file in files:
        data = pickle.load(open(os.path.join(sys.argv[1], file), 'rb'))
        for i in range(512//64):
            for j in range(512//64):
                i_start = i*64 - 3
                i_end = (i+1)*64 + 3
                j_start = j*64 - 3
                j_end = (j+1)*64 + 3
                output = np.zeros((70,70,data.shape[2]))
                if i_start < 0:
                    i_ind_start = -i_start
                else:
                    i_ind_start = 0
                if j_start < 0:
                    j_ind_start = -j_start
                else:
                    j_ind_start = 0
                if i_end > 511:
                    i_ind_end = 70 - i_end + 512
                else:
                    i_ind_end = 70
                if j_end > 511:
                    j_ind_end = 70 - j_end + 512
                else:
                    j_ind_end = 70
                i_start = max(0, i_start)
                i_end = min(512, i_end)
                j_start = max(0, j_start)
                j_end = min(512, j_end)
                output[i_ind_start:i_ind_end, j_ind_start:j_ind_end] = data[i_start:i_end, j_start:j_end]
                print(i_start, i_end, j_start, j_end, i_ind_start, i_ind_end, j_ind_start, j_ind_end)
                pickle.dump(output, open(os.path.join(sys.argv[2], file.replace('.pt','_'+str(i)+'_'+str(j)+'.pt')),'wb'))
