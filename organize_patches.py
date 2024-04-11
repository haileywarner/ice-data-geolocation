import glob
import os
import shutil
import pandas as pd
from pathlib import Path
import numpy as np

dir = r"E:\spatially_sorted_lvisf2_is2olvis1bcv"
unprocessed_folders = ['58784_to_58879','58879_to_58974','59752_to_59849','59056_to_59230','58974_to_59069','58418_to_58784','63493_to_64496','57085_to_57180','59230_to_59484','69051_to_69408',\
                       '58072_to_58328','59849_to_59985','59617_to_59713','59653_to_59752','57435_to_57540','69591_to_69925','64693_to_64794','61470_to_61717','65957_to_68185','60705_to_61356',\
                        '60059_to_60548','59881_to_60059','69408_to_69591','58227_to_58322',\
                        '65858_to_65957','58382_to_62839','64496_to_64592','65762_to_65858','64592_to_64693','60548_to_60705','68185_to_68413','61356_to_61470','59713_to_59881','58037_to_58132',\
                        '57540_to_57899','57180_to_57407','59069_to_59165','59554_to_59653','59456_to_59554','57899_to_58072','59262_to_59360','58954_to_59056','59360_to_59456','59165_to_59262',\
                        '59985_to_60212','58328_to_58954','59484_to_59617']
destination_folder = r"E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches"

def organize_patches(dir, unprocessed_folders, destination_folder):
    main_df = pd.DataFrame()
    for folder in unprocessed_folders:
        metadata = Path(os.path.join(dir,folder)+'\metadata61.csv')
        if metadata.is_file():
            text =  Path(glob.glob(os.path.join(dir,folder)+'\*.txt')[0])
            z_maxamp_list = []
            for imgfile in glob.glob(os.path.join(dir,folder)+'\patches61\*.png'):
                shutil.copy(imgfile, os.path.join(destination_folder,'patch'+str(n)+'.png'))
            df = pd.read_csv(os.path.join(dir,folder)+'\metadata61.csv')
            LVISF2 = np.genfromtxt(text, dtype=float, usecols=(8))
            for index, row in df.iterrows():
                altimetry_row = row['row_in_altimetry_file']
                z_maxamp = LVISF2[altimetry_row]
                z_maxamp_list.append(z_maxamp)
            df['z_maxamp'] = z_maxamp_list
            main_df = pd.concat((main_df,df),axis=0)
    main_df.to_csv(r'E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\metadata.csv')

organize_patches(dir, unprocessed_folders, destination_folder)