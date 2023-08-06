## arg1 data input, arg2 data output
import pickle, os, sys
spacing = pickle.load(open('/data/cheng/CT/spacing.pt','rb'))
output_path = os.path.join(sys.argv[2],'HR')
files = os.listdir(sys.argv[1])
test_files = []
for file in files:
    data = pickle.load(open(os.path.join(sys.argv[1], file),'rb'))['image'][...,::2]
    if data.shape[2] < 100:
        print('data size too small, ', file)
        continue
    if data.shape[2] % 128 != 0:
        print('discarding slices to make appropriate number of slices')
        data = data[..., (data.shape[2] % 4):]
    name = file.replace('.pt','')
    for i in range(512):
        output = {}
        output['spacing'] = [spacing[name][0], spacing[name][1], spacing[name][2]*2]
        output['image'] = data[:,i,:]
        # pickle.dump(output, open(os.path.join(output_path, file.replace('.pt', '_cor_' + str(i) + '.pt')), 'wb'))
    print('finished: ', file)
    test_files.append(file.replace('.pt',''))
print(test_files)

#files = ['LCTSC-Train-S3-002', 'LCTSC-Test-S3-101', 'LCTSC-Train-S3-004', 'LCTSC-Test-S3-102', 'LCTSC-Train-S3-001', 'LCTSC-Train-S3-008', 'LCTSC-Test-S3-203', 'LCTSC-Train-S3-003', 'LCTSC-Train-S3-012']