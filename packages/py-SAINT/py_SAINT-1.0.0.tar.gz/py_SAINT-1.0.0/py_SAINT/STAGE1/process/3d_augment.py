#inp dir, output dir, quartile
import os, sys, pickle
spacing_liver = pickle.load(open('/data/cheng/liver/spacing.pt','rb'))
factors = [2,3,4,5,6,7,8,9,10]
threshold = 60
avg_spacing = 0
avg_spacing_whole = 0
count = 0
count_whole = 0
files = os.listdir(sys.argv[1])
quartile = int(sys.argv[3])

def save(data, out_path):
    copies = data.shape[2]//threshold
    for i in range(copies):
        if i != copies - 1:
            pickle.dump(data[...,i*threshold:(i+1)*threshold],
                        open(out_path.replace('.pt', '_copy_' + str(i) + '.pt'), 'wb'))
        else:
            print(data.shape[2] - i*threshold)
            pickle.dump(data[...,i*threshold:],
                        open(out_path.replace('.pt', '_copy_' + str(i) + '.pt'), 'wb'))

length = len(files)
for file in files[quartile*length//4:(quartile+1)*length//4]:
    path = os.path.join(sys.argv[1], file)
    out_path = os.path.join(sys.argv[2], file)
    if os.path.isfile(path.replace('.pt','_sag_factor_'+str(2)+'.pt')) or 'sag' in path or 'ax' in path or 'cor' in path:
        continue
    name = file.replace('.pt','')
    data_hold = pickle.load(open(path,'rb'))
    if 'spacing' in data_hold:
        file_spacing = data_hold['spacing']
    else:
        file_spacing = spacing_liver[name]
    data = data_hold['image']
    # file_spacing = spacing[name]
    avg_spacing = avg_spacing + file_spacing[2]*data.shape[2]
    avg_spacing_whole = avg_spacing_whole + file_spacing[2]
    count = count + data.shape[2]
    count_whole = count_whole + 1
    print(out_path, data.shape[2],file_spacing[2])
    save(data, out_path)
    for factor in factors:
        if file_spacing[2]*factor <= 5.0 and data.shape[2]//factor >= threshold:
            for i in range(factor):
                # avg_spacing_whole = avg_spacing_whole + file_spacing[2]*factor
                # count_whole = count_whole + 1
                # avg_spacing = avg_spacing + file_spacing[2]*factor*data.shape[2]//factor
                # count = count + data.shape[2]//factor
                new_data = data[...,i:][...,::factor]
                print(out_path.replace('.pt','_ax_factor_'+str(factor)+'.pt'), new_data.shape[2], factor)
                # pickle.dump(new_data, open(path.replace('.pt','_ax_factor_'+str(factor)+'_copy_'+str(i)+'.pt'),'wb'))
                save(new_data, out_path.replace('.pt','_ax_factor_'+str(factor)+'.pt'))


print(avg_spacing/count)
print(avg_spacing_whole/count_whole)