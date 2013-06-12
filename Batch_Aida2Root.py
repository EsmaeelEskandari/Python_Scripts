import glob
import os
import ROOT
from Aux_Functions import *

hist_list = GetListDataset('hist_list')
dataset_names = GetListDataset('dataset_names')
				
# Get rid of all the current root files (Clean the slate!)
os.system('find . -name \*.root -exec rm -rf {} \;')
				
# Time to merge some files!
for folder in dataset_names:
	folder = folder+"/"
	root_file_list = []
	if os.path.exists(folder) == True:
		os.chdir(folder)
		Aida_Files = glob.glob("*.aida")
		
		# Run aida2root over every file in Aida_Files list.
		for aida in Aida_Files:
			cmd = 'aida2root '+aida
			os.system(cmd)
			aida = os.path.splitext(aida)
			root_file = aida[0]+".root"
			root_file_list.append(root_file)
		
		# Merge Root files (use hadd?)
		arguments = "%s" % " ".join(map(str, root_file_list))
		file_name = folder.split('.')
		cmd = "hadd -f "+file_name[0]+".root "+arguments
		os.system(cmd)
		
		# Need to divide histograms by number of merged files to make average...
		# This may not be right, considering the average should be done bin-by-bin
		# and each bin may not have same number of points...
		merged_root = ROOT.TFile(file_name[0]+".root", 'UPDATE')
		for hist in hist_list:
			histogram = merged_root.Get(hist)
			histogram.Scale(1.0/float(len(root_file_list)))
			histogram.Write('',ROOT.TObject.kOverwrite)
		#merged_root.Write()	
		merged_root.Close()
		
		
		# Prepare for next folder	
		os.chdir("..")
		Aida_Files = []
			
	else:
		continue