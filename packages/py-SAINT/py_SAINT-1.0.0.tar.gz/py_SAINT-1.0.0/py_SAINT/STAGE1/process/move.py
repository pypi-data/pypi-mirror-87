from shutil import move
import os
input_dir = '/home/cheng/FUSE_x6/TEST/HR/'
output_dir = '/home/cheng/FUSE_x4/TEST/HR/'
files = os.listdir(input_dir)
for file in files:
    move(input_dir+file, output_dir+file.replace('.pt','_x6.pt'))