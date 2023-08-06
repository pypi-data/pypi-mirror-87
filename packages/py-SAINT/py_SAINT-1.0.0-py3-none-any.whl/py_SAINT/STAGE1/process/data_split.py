# arg 1 input data, arg 2 output split, arg 3 upsampling factor
import pickle, os, sys
factor = int(sys.argv[3])
folders = ['pickleTr', 'pickleTs']
min_size = 32
discard_num = 0
for folder in folders:
    root_path = os.path.join(sys.argv[1], folder)
    output_train_path_HR = os.path.join(sys.argv[2], 'TRAIN/HR')
    # output_test_path_HR = os.path.join(sys.argv[2], 'TEST/HR')
    patients = os.listdir(root_path)
    for patient in patients[3*len(patients)//4:]:
        print('start on: ', patient)
        if patient == 'liver_187.pt':
            data = pickle.load(open(os.path.join(root_path, patient), 'rb'))['image']
            print('liver_187 shape: ', data.shape)
            continue
        data = pickle.load(open(os.path.join(root_path, patient), 'rb'))['image']
        # print('data shape, ', data.shape)
        if data.shape[2]//factor > min_size:
            # discard_num = discard_num + 1
            if data.shape[2] % 128 != 0:
                print('discarding slices to make appropriate number of slices')
                data = data[..., (data.shape[2] % 128):]
            lr_data = data[..., ::factor]
            for j in range(lr_data.shape[2]//32):
                # seems like the uneven size of input data stresses a lot on the dataloader
                for i in range(data.shape[0]):
                    # print(os.path.join(output_train_path_HR, patient.replace('.pt','_cor_'+ str(i) +'.pt')))
                    pickle.dump(data[i, :, 128*j:128*(j+1)], open(os.path.join(output_train_path_HR, patient.replace('.pt','_cor_'+ str(i) +'.pt')), 'wb'))
                    pickle.dump(lr_data[i, :, 32*j:32*(j+1)],
                                open(os.path.join(output_train_path_HR.replace('HR','LR'), patient.replace('.pt','_cor_'+ str(i) +'.pt')), 'wb'))
                    pickle.dump(data[:, i, 128*j:128*(j+1)], open(os.path.join(output_train_path_HR, patient.replace('.pt','_sag_'+ str(i) +'.pt')), 'wb'))
                    pickle.dump(lr_data[:, i, 32*j:32*(j+1)],
                                open(os.path.join(output_train_path_HR.replace('HR','LR'), patient.replace('.pt','_sag_'+ str(i) +'.pt')), 'wb'))
            print('finished: ', patient)
        else:
            print('volume too thin for training, number of LR slices: ', data.shape[2]//factor)
