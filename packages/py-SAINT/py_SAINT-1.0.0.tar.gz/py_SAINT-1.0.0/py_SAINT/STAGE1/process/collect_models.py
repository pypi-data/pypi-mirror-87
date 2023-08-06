import sys, os
from shutil import move, rmtree

input_dir = sys.argv[1]
exps = os.listdir(input_dir)
for exp in exps:
    model_dir = os.path.join(input_dir, exp,'model')
    if len(os.listdir(model_dir)) == 0:
        print('test folder')
        print(os.path.join(input_dir, exp))
        rmtree(os.path.join(input_dir, exp))
    else:
        print('model folder')
        print(os.path.join(input_dir, exp,'results'))
        rmtree(os.path.join(input_dir, exp,'results'))