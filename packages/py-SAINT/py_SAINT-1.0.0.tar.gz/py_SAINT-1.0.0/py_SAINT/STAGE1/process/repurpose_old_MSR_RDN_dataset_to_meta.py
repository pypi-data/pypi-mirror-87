import pickle, os, sys

spacing = pickle.load(open('/data/cheng/liver/spacing.pt', 'rb'))

files = os.listdir(sys.argv[1])
length = len(files)
wrong_file = []
for file in files:
    try:
        data = pickle.load(open(os.path.join(sys.argv[1], file),'rb'))
    except:
        print('ERRORRRR ', file)
        wrong_file.append(file)
        continue
    if 'image' in data:
        # print(file)
        if 'image' in data['image']:
            data['image'] = data['image']['image']
            pickle.dump(data, open(os.path.join(sys.argv[1], file), 'wb'))
            print('finished: ', file)
        continue
    output = {}
    name = file.split('_')
    name = name[0] + '_' + name[1]
    output['image'] = data
    output['spacing'] = spacing[name]
    pickle.dump(output, open(os.path.join(sys.argv[1], file), 'wb'))
    print('finished: ', file)
print(wrong_file)