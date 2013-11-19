import glob, os, sys
from Aux_Functions import *

# This script will be must be run from directory in which dataset
# directories are stored. Prepare_Syst_File.sh handles this.
dir_contents = glob.glob('./*')
folder_list = [ x for x in dir_contents if os.path.isdir(x)]
print "The number of directories to in pwd is: "+str(len(folder_list))
dataset_names = GetListDataset('dataset_names')
dataset_number = GetListDataset('dataset_number')

# Adjust folder_list such that the elements know 
# pwd is the directory they should be stored in.
for idx,folder in enumerate(folder_list):
  folder_list[idx] = folder.split('/')[-1]

# Rename the folders properly
for index,dataset in enumerate(dataset_names):
  cmd = 'mkdir '+dataset
  os.system(cmd)
  for folder in folder_list:
    if dataset_number[index] in folder:
      cmd = 'mv '+folder+'/* '+dataset+' && rm -r '+folder
      os.system(cmd)
    else:
      print "Dataset Number "+dataset_number[index]+" was not found in the current directory."

