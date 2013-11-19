import ROOT
import os
from Aux_Functions import *
from pyAMI.client import AMIClient
from pyAMI.auth import AMI_CONFIG, create_auth_config
from pyAMI.query import *
from pyAMI.exceptions import *

hf = ROOT.TFile("VBF_Systematics.root", "RECREATE")

datasets = GetListDataset('datasets')
dataset_names = GetListDataset('dataset_names')
exp_hist_list = GetListDataset('exp_hist_list')
hist_list = GetListDataset('hist_list')
title_list = GetListDataset('title_list')
x_axis_list = GetListDataset('x_axis_list')
y_axis_list = GetListDataset('y_axis_list')
y_axis_list_norm = GetListDataset('y_axis_list_norm')

def StyleHistogram(index, h1):
	index = int(index/2)
	h1.SetTitle(title_list[index])
	h1.GetXaxis().SetTitle(x_axis_list[index])
	h1.GetYaxis().SetTitle(y_axis_list[index])
	h1.SetOption("HIST E")
	
def StyleData(index, h1):
	index = int(index/2)
	h1.SetTitle(title_list[index])
	h1.GetXaxis().SetTitle(x_axis_list[index])
	h1.GetYaxis().SetTitle(y_axis_list[index])
	h1.SetMarkerStyle(20)
	h1.SetMarkerSize(0.9)

#Setup AMIClient.	
#This works only on my laptop, otherwise you need to run 'ami auth'
client = AMIClient()
if not os.path.exists(AMI_CONFIG):
	create_auth_config()
client.read_config(AMI_CONFIG)

if os.path.exists("Exp_Data_arXiv12011276.root") == True:
	hf.mkdir("Exp_Data_2012")
	hf.cd("Exp_Data_2012")
	exp_data = ROOT.TFile.Open("Exp_Data_arXiv12011276.root")
	for index, hist in enumerate(exp_hist_list):
		histogram = exp_data.Get(hist)
		hf.cd("Exp_Data_2012")
		StyleData(index, histogram)
		histogram.Write()
		del histogram
	exp_data.Close()
	hf.cd()

#Folder names must be the same as in the dataset_names list in Aux_Functions.py
#I could try to get the script to just to check for run number in folder name (do this later)
#Root file needs to be named after the dataset run number
#for folder in dataset_names:
for folder, data in zip(dataset_names, datasets):
	if os.path.exists(folder+"/") == True:
		#First get the crossSection_mean and GenFiltEff_mean for this dataset from AMI for normalizations
		xsec, effic = get_dataset_xsec_effic(client, data)
		print folder, xsec, effic
		xsec = 1000*xsec*effic #Converts nb to pb and applies GenFiltEff
		
		#histogram manipulation and such
		os.chdir(folder+"/")
		hf.mkdir(folder)
		hf.cd(folder)
		ROOT.gDirectory.mkdir("Normalized_XS")
		ROOT.gDirectory.mkdir("Shape_Comparisons")
		file_name = folder.split('.')
		file_name = file_name[0]
		root_file = ROOT.TFile.Open(file_name+".root")
		for index, hist in enumerate(hist_list):
			histogram = root_file.Get(hist)
			hf.cd(folder)
			StyleHistogram(index, histogram)
			histogram.Write()
			# Clone root histograms, normalize to XS, and move to Normalized_XS directory
			histogram_norm = histogram.Clone(hist+"_norm")
			histogram_norm.GetYaxis().SetTitle("(1/#sigma) "+y_axis_list_norm[int(index/2)])
			histogram_norm.Scale(1.0/xsec)
			ROOT.gDirectory.cd("Normalized_XS")
			histogram_norm.Write()
			ROOT.gDirectory.cd()
			# Clone root histograms, normalize to area, and move to Shape_Comparisons directory
			histogram_area = histogram.Clone(hist+"_shape")
			histogram_area.GetYaxis().SetTitle("(1/N) "+y_axis_list_norm[int(index/2)])
			integ = histogram_area.Integral("width")
			# if integ != 0.0:
			# 	histogram_area.Scale(1.0/integ)
			# 	ROOT.gDirectory.cd("Shape_Comparisons")
			# 	histogram_area.Write()
			# 	ROOT.gDirectory.cd()
			del histogram_norm, histogram_area
		root_file.Close()
		hf.cd()
		os.chdir("..")
	else:
		continue

hf.Write()
hf.Close()
print "Job Complete!!!"