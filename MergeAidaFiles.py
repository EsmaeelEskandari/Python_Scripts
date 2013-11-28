import glob
import os
from Aux_Functions import *

dataset_names = GetListDataset('dataset_names')

# Make a list of Aida files available in the current directory
for folder in dataset_names:
	current_dir = folder+"/"
	if os.path.exists(current_dir) == True:
		os.chdir(current_dir)
		Aida_Files = glob.glob("*.aida")
		i = len(Aida_Files)
		print "There were %i in the directory: "%i + current_dir

        if i = 0: continue
		# Run aidamerge.py over every file in the Aida_Files list.
		arguments = "%s" % " ".join(map(str, Aida_Files))
		cmd = "python ../aidamerge.py -o merged_avg.aida "+arguments
		os.system(cmd)
		cmd = "python ../aidamerge.py -s -o merged_add.aida "+arguments
		os.system(cmd)
		
		# Convert merged.aida file to merged.root file and rename to dataset
		# run number (found from the folder name).
		os.system("aida2root merged_avg.aida")
		os.system("aida2root merged_add.aida")
		file_name = folder.split('.')
		file_name = file_name[0]
		cmd = "mv merged_avg.root "+file_name+".root"
		os.system(cmd)
		cmd = "mv merged_add.root "+file_name+"_add.root"
		os.system(cmd)
		
		# Remove the merged.aida file in case the script fails.
		# This keeps you from having to delete them by hand before re-running script.
		os.system("rm merged_add.aida merged_avg.aida")
		
		# Prepare for next folder
		os.chdir("..")
		Aida_Files = []
	else:
		continue
