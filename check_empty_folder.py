import os
import shutil
import glob

contains_imagery = False
num_empty = 0
num_nonempty = 0
main = r'E:\spatially_sorted_lvisf2_is2olvis1bcv'
empty = r'E:\spatially_sorted_lvisf2_is2olvis1bcv\empty_segments'

folders = os.listdir(main)#.remove('empty_segments')
print(len(folders))
for i in range(len(folders)):
    files = os.listdir(os.path.join(main,folders[i]))
    for f in files:
        if f.endswith('.tif'):
            contains_imagery = True
    if contains_imagery == True:
        #print(os.path.join(main,folders[i]))
        num_nonempty += 1
    else:
        print(os.path.join(main,folders[i]))
        num_empty += 1
        shutil.move(os.path.join(main,folders[i]), os.path.join(main,"empty_segments",folders[i]))
print(str(num_empty))
print(str(num_nonempty))