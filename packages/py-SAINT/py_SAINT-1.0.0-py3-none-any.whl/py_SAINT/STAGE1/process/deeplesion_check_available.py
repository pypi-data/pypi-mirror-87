
import os, sys, csv, pickle
import numpy as np
import scipy.misc
home_path = '/data/cheng/deeplesion/Images_png/'
output = '/data/cheng/deeplesion/1mm/'
def get_num(input):
    if input < 10:
        return '00'+str(input) + '.png'
    elif input < 100:
        return '0' + str(input) + '.png'
    else:
        return str(input) + '.png'

def get_volume(case, slice_info):
    case_dir = os.path.join(home_path, case)
    nums = np.arange(slice_info[0], slice_info[1]+1)
    output = np.zeros((512, 512, len(nums))).astype('float')
    for i in range(len(nums)):
        output[...,i] = scipy.misc.imread(os.path.join(case_dir, get_num(nums[i])))
    output = output - output.min()
    output = np.clip(output, 0, 4000).astype('int32')
    return np.transpose(output, (1,0,2))



csvfile = open('/data/cheng/deeplesion/DL_info.csv')
readCSV = csv.reader(csvfile)
threshold = 256
total_case = 0
total_slice = 0
thickness = {}
for row in readCSV:
    if row[0] == 'File_name':
        continue
    slice_info = [int(x) for x in row[11].split(',')]
    slice_num = slice_info[1] - slice_info[0]
    slice_spacing = [float(x) for x in row[12].split(',')]
    # print(slice_spacing)
    if slice_num > threshold:
        if slice_spacing[2] in thickness:
            thickness[slice_spacing[2]] = thickness[slice_spacing[2]] + 1
        else:
            thickness[slice_spacing[2]] = 1
        if slice_spacing[2] == 1.0:
            print(slice_num)
        if slice_spacing[2] == 1.0:
            if not os.path.isfile(output+row[0][:-8]+'.pt'):
                data = get_volume(row[0][:-8], slice_info)
                output_file = {}
                output_file['image'] = data
                output_file['spacing'] = slice_spacing
                pickle.dump(output_file,open(output+row[0][:-8]+'.pt','wb'))
                print(row[0][:-8])
        total_case = total_case + 1
        total_slice = total_slice + slice_num

print(total_case, total_slice, thickness)

