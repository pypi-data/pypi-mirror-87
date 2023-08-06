import os, sys, pickle
import numpy as np

def get_stats(path):
    data = pickle.load(open(path,'rb'))['image']
    # mean = data.mean(2).mean(1)
    std = data.std(2).std(1)
    return std

files = os.listdir(sys.argv[1])
count = 1
overall_std = get_stats(os.path.join(sys.argv[1], files[0]))
for i in range(1, len(files)):
    if i%500 == 0:
        print(overall_std/count)
    new_std = get_stats(os.path.join(sys.argv[1], files[i]))
    overall_std = overall_std+new_std
    count = count + 1

overall_std = overall_std/len(files)
print(overall_std)

