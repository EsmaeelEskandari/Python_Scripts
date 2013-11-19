import glob, os, sys
from Aux_Functions.py import *

# User input the proper directory
# Command-line argument needs a /path/*
# Need to split sys.argv elements to get the directory they are stored in
folder_list = sys.argv[1:]
dataset_names = GetListDataset('dataset_names')
dataset_number = GetListDataset('dataset_number')

# Rename the folders properly
for index,dataset in enumerate(dataset_names):
    cmd = 'mkdir '+dataset
    os.system(cmd)
    for folder in folder_list:
       if dataset_number[index] in folder:
           cmd = 'mv '+folder+'/* '+dataset+' && rm -r '+folder
           os.system(cmd)