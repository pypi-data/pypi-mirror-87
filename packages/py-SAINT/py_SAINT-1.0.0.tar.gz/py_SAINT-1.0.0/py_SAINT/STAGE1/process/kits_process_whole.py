from starter_code.utils import load_case
import pickle, os, json, sys
import numpy as np
view = sys.argv[1]
quartile = int(sys.argv[2])
os.chdir('/data/cheng/kits19/kits19/')
# readfile = open('/data/cheng/kits19/kits19/data/kits.json')
outfile = open('data/kits.json','r')
kits = json.load(outfile)
output_dir = '/data/cheng/kits19/TEST/HR/'
length = len(kits)
test_files = ['case_00186', 'case_00111', 'case_00144', 'case_00029', 'case_00019', 'case_00171', 'case_00047', 'case_00046', 'case_00133', 'case_00032', 'case_00193', 'case_00105', 'case_00128', 'case_00160', 'case_00086', 'case_00082', 'case_00207', 'case_00183', 'case_00131', 'case_00081', 'case_00180', 'case_00098', 'case_00040', 'case_00184', 'case_00072', 'case_00196', 'case_00189', 'case_00185', 'case_00043', 'case_00060', 'case_00036', 'case_00190', 'case_00016']
# test_files = ['case_00091', 'case_00000', 'case_00071', 'case_00001', 'case_00111', 'case_00019', 'case_00053', 'case_00123', 'case_00022', 'case_00032', 'case_00128', 'case_00154', 'case_00086', 'case_00049', 'case_00135', 'case_00027', 'case_00052', 'case_00066', 'case_00084', 'case_00095', 'case_00006', 'case_00141', 'case_00118', 'case_00060', 'case_00101', 'case_00016']
# test_files = ['case_00091']
for file in kits:
    if file['case_id'] in test_files:
        print(file['case_id'])
        volume, seg = load_case(file['case_id'])
        try:
            volume, seg = volume.get_data(), seg.get_data()
        except:
            print('ERROR!')
            continue
        if volume.min() == -2048:
            print('ehhh different')
            volume = np.clip(volume, -1024, volume.max())
        volume = volume - volume.min()
        spacing = [file['captured_pixel_width'], file['captured_pixel_width'], file['captured_slice_thickness']]
        if volume.max() > 9000:
            print('metal artifact')
            continue
        # print('max: ', volume.max())
        # print('mid: ', volume[...,220][20][volume.shape[2]//2])
        # if view == 'sag':
        #     volume = np.transpose(np.clip(volume, 0, 4000).astype("uint16"), (1,2,0))
        # elif view == 'cor':
        volume = np.transpose(np.clip(volume, 0, 4000).astype("uint16"), (2,1,0))
        # output = {}
        # output['spacing'] = spacing
        # spacing = [file['captured_pixel_width'], file['captured_pixel_width'], file['captured_slice_thickness']]
        output = {}
        output['image'] = volume
        output['spacing'] = spacing
        pickle.dump(output, open(os.path.join(output_dir, file['case_id']+'.pt'),'wb'))
        # #sag is 1st, cor is 2nd, note that cor and sag is actually reversed from the real ones......
        # for j in range(512):
        #     name = os.path.join(output_dir, file['case_id'] + '_' + view + '_slice_' + str(j) + '.pt')
        #     hr = np.zeros((3, volume.shape[1], volume.shape[2])).astype('uint16')
        #     if j == 0:
        #         hr[1] = volume[0]
        #         hr[2] = volume[1]
        #     elif j == 511:
        #         hr[0] = volume[510]
        #         hr[1] = volume[511]
        #     else:
        #         hr[0] = volume[j - 1]
        #         hr[1] = volume[j]
        #         hr[2] = volume[j + 1]
        #     output['image'] = hr
        #     pickle.dump(output, open(name, 'wb'))
        print('finish: ', file)