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

# https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/
# source = 'E:\spatially_sorted_lvisf2_is2olvis1bcv\empty_segments'
# destination = 'E:\spatially_sorted_lvisf2_is2olvis1bcv'
# #
# # gather all files
# allfiles = glob.glob(os.path.join(source, '*'), recursive=True)
# print("Files to move", allfiles)
 
# # iterate on all files to move them to destination folder
# for file_path in allfiles:
#     dst_path = os.path.join(destination, os.path.basename(file_path))
#     shutil.move(file_path, dst_path)
#     print(f"Moved {file_path} -> {dst_path}")