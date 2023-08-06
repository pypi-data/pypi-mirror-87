import os, random, sys, pickle
#x4

# liver = {'liver_0.pt': [50, 42, 26, 45, 35], 'liver_42.pt': [43, 55, 71, 67, 58], 'liver_75.pt': [26, 47, 30, 35, 54], 'liver_150.pt': [42, 23, 39, 35, 50], 'liver_153.pt': [54, 33, 38, 55, 25]}
#
# colon = {'colon_038.pt': [31, 6, 1, 37, 13], 'colon_170.pt': [11, 33, 41, 27, 14], 'colon_213.pt': [10, 17, 25, 2, 19], 'colon_064.pt': [34, 18, 25, 11, 31], 'colon_183.pt': [29, 13, 26, 35, 31]}
#
# vessel = {'hepaticvessel_258.pt': [9, 39, 21, 38, 22], 'hepaticvessel_322.pt': [25, 33, 5, 10, 34], 'hepaticvessel_027.pt': [23, 29, 5, 7, 35], 'hepaticvessel_043.pt': [5, 38, 7, 21, 15], 'hepaticvessel_335.pt': [38, 27, 22, 35, 34]}
#
# kidney = {'case_00098.pt': [103, 126, 113, 97, 130], 'case_00133.pt': [99, 90, 110, 94, 87], 'case_00184.pt': [67, 89, 59, 57, 55], 'case_00193.pt': [101, 110, 125, 118, 111], 'case_00207.pt': [49, 59, 55, 51, 85]}

#x6
kidney = {'case_00196.pt': [77, 92, 100, 103, 105], 'case_00111.pt': [89, 82, 83, 99, 76], 'case_00189.pt': [62, 59, 74, 52, 64], 'case_00186.pt': [50, 87, 63, 79, 58], 'case_00207.pt': [50, 51, 86, 67, 85]}

vessel = {'hepaticvessel_148.pt': [19, 35, 17, 40, 37], 'hepaticvessel_099.pt': [41, 29, 17, 15, 7], 'hepaticvessel_382.pt': [7, 31, 35, 27, 11], 'hepaticvessel_144.pt': [7, 23, 17, 38, 16], 'hepaticvessel_268.pt': [31, 23, 22, 38, 26]}

liver = {'liver_200.pt': [50, 40, 53, 67, 77], 'liver_152.pt': [59, 47, 37, 49, 34], 'liver_53.pt': [62, 50, 57, 51, 63], 'liver_41.pt': [50, 63, 40, 46, 47], 'liver_169.pt': [38, 8, 32, 25, 21]}

colon = {'colon_027.pt': [28, 22, 1, 21, 4], 'colon_177.pt': [31, 17, 25, 7, 45], 'colon_170.pt': [4, 8, 25, 10, 9], 'colon_051.pt': [3, 32, 16, 19, 14], 'colon_042.pt': [14, 19, 15, 7, 32]}

# for item in liver.keys():
#     sr = pickle.load(open(os.path.join(sys.argv[1], item.replace('.pt','_x6_SR.pt')),'rb'))
#     print(item,sr.shape)
#     # hr = pickle.load(open(os.path.join(sys.argv[2], item,'rb')))['image']
#     for i in liver[item]:
#         pickle.dump(sr[...,i], open(os.path.join(sys.argv[2], item.replace('.pt','_'+str(i)+'_SAINT.pt')),'wb'))
#     print('finish')
#
# for item in colon.keys():
#     sr = pickle.load(open(os.path.join(sys.argv[1], item.replace('.pt','_x6_SR.pt')),'rb'))
#     print(item,sr.shape)
#     # hr = pickle.load(open(os.path.join(sys.argv[2], item,'rb')))['image']
#     for i in colon[item]:
#         pickle.dump(sr[...,i], open(os.path.join(sys.argv[2], item.replace('.pt','_'+str(i)+'_SAINT.pt')),'wb'))
#     print('finish')

for item in vessel.keys():
    sr = pickle.load(open(os.path.join(sys.argv[1], item.replace('.pt','_x6_SR.pt')),'rb'))
    print(item,sr.shape)
    # hr = pickle.load(open(os.path.join(sys.argv[2], item,'rb')))['image']
    for i in vessel[item]:
        pickle.dump(sr[...,i], open(os.path.join(sys.argv[2], item.replace('.pt','_'+str(i)+'_SAINT.pt')),'wb'))
    print('finish')

# for item in kidney.keys():
#     sr = pickle.load(open(os.path.join(sys.argv[1], item.replace('.pt','_x6_SR.pt')),'rb'))
#     print(item,sr.shape)
#     # hr = pickle.load(open(os.path.join(sys.argv[2], item,'rb')))['image']
#     for i in kidney[item]:
#         pickle.dump(sr[...,i], open(os.path.join(sys.argv[2], item.replace('.pt','_'+str(i)+'_SAINT.pt')),'wb'))
#     print('finish')