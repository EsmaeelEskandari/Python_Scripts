import ROOT
import os
from Aux_Functions import *
# from pyAMI.client import AMIClient
# from pyAMI.auth import AMI_CONFIG, create_auth_config
# from pyAMI.query import *
# from pyAMI.exceptions import *

hf = ROOT.TFile("VBF_Systematics.root", "RECREATE")

datasets = GetListDataset('datasets')
dataset_names = GetListDataset('dataset_names')
dataset_number = GetListDataset('dataset_number')
exp_hist_list = GetListDataset('exp_hist_list')
hist_list = GetListDataset('hist_list')
cross_sections = GetListDataset('cross_sections')
title_list = GetListDataset('title_list')
x_axis_list = GetListDataset('x_axis_list')
y_axis_list = GetListDataset('y_axis_list')
y_axis_list_norm = GetListDataset('y_axis_list_norm')

merged_pwhg = ['000001','000002','000003','000004','000005','000006','000007']
powheg_dict = dict(zip(dataset_number, dataset_names))

def StyleHistogram(index, h1):
    h1.SetTitle(title_list[index])
    h1.GetXaxis().SetTitle(x_axis_list[index])
    h1.GetYaxis().SetTitle(y_axis_list[index])
    h1.SetOption("HIST E")
    
def StyleCutFlow(h1):
    h1.GetXaxis().SetBinLabel(2,"No Cuts")
    h1.GetXaxis().SetBinLabel(3, "WFinder and #geq 2jets") # WFinder include MET cut
    h1.GetXaxis().SetBinLabel(4, "p_{T,1} > 80GeV")
    h1.GetXaxis().SetBinLabel(5, "p_{T,2} > 60GeV")
    h1.GetXaxis().SetBinLabel(6, "M_{jj} > 500GeV")
    h1.GetXaxis().SetBinLabel(7, "CJV")
    h1.GetXaxis().SetBinLabel(8, "OLV")
    #h1.GetXaxis().SetBinLabel(9, "")
    #h1.GetXaxis().SetBinLabel(10, "")
    #h1.GetXaxis().SetBinLabel(11, "")
    
def StyleTH2(th2):
    th2.SetTitle("Differential Dijet Mass and N_{jets} Distribution")
    th2.GetXaxis().SetTitle("N_{jets} in event")
    th2.GetYaxis().SetTitle("Dijet Mass [GeV]")
    th2.GetZaxis().SetTitle("(1/#sigma) d#sigma/d#m_{jj}dN_{jets}")
    th2.SetOption("LEGO2 0")
	
def StyleData(index, h1):
	h1.SetTitle(title_list[index])
	h1.GetXaxis().SetTitle(x_axis_list[index])
	h1.GetYaxis().SetTitle(y_axis_list[index])
	h1.SetMarkerStyle(20)
	h1.SetMarkerSize(0.9)
    
def CompileDijetMass(ExclMjj,th2_hist):
    # x-axis is the number of jets in event
    # y-axis is the Dijet mass of the event
    bin_cont = []
    bin_err = []
    jet_num = ExclMjj.GetName()
    jet_num = int(jet_num.split('_')[2])
    # Get bin content and error for given Excl_jet_Mjj
    for bin in range(202):
        bin_cont.append(ExclMjj.GetBinContent(bin))
        bin_err.append(ExclMjj.GetBinError(bin))
    
    # Set bin content and error in th2_hist for given excl_jet_#
    for bin in range(202):
        th2_hist.SetBinContent(jet_num+1,bin,bin_cont[bin])
        th2_hist.SetBinError(jet_num+1,bin,bin_err[bin])
        
    return th2_hist
    
def MergeChannels(hist,file_name):
    source_Wm = str(int(file_name) + 185695)
    source_Wp = str(int(source_Wm) + 7)
    source_Wm_dir = powheg_dict[source_Wm]
    source_Wp_dir = powheg_dict[source_Wp]
    rootFile_Wp_avg = ROOT.TFile.Open("../"+source_Wp_dir+"/"+source_Wp+".root")
    rootFile_Wm_avg = ROOT.TFile.Open("../"+source_Wm_dir+"/"+source_Wm+".root")
    rootFile_Wp_add = ROOT.TFile.Open("../"+source_Wp_dir+"/"+source_Wp+"_add.root")
    rootFile_Wm_add = ROOT.TFile.Open("../"+source_Wm_dir+"/"+source_Wm+"_add.root")
    
    histogram = rootFile_Wp_avg.Get(hist)
    hist1 = histogram.Clone()
    hist2 = rootFile_Wm_avg.Get(hist)
    hist1.Add(hist2)
    
    histogram_add = rootFile_Wp_add.Get(hist)
    hist3 = histogram_add.Clone()
    hist4 = rootFile_Wm_add.Get(hist)
    hist3.Add(hist4)
    
    rootFile_Wp_avg.Close()
    rootFile_Wm_avg.Close()
    rootFile_Wp_add.Close()
    rootFile_Wm_add.Close()
    
    del histogram, histogram_add, hist2, hist4
    # Need to check errors on new_hist (it should not be sumw2)
    return hist1, hist3

#Setup AMIClient.	
#This works only on my laptop, otherwise you need to run 'ami auth'
# client = AMIClient()
# if not os.path.exists(AMI_CONFIG):
#     create_auth_config()
# client.read_config(AMI_CONFIG)

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

# Folder names must be the same as in the dataset_names list in Aux_Functions.py
# I could try to get the script to just to check for run number in folder name (do this later)
# Root file needs to be named after the dataset run number
_h_xsecs = ROOT.TH1F("Cross_Sections","Cross_Sections",len(dataset_names),0,len(dataset_names))
_h_xsecs.GetYaxis().SetTitle("Cross Section [pb]")
for idx,folder in enumerate(dataset_names):
#for folder, data in zip(dataset_names, datasets):
    if os.path.exists(folder+"/") == True:
        th2_hist_30 = ROOT.TH2F( "hmj1j2_wvbf", "hmj1j2_wvbf", 10, -0.5, 9.5, 200, 0, 5000 )
        # First get the crossSection_mean and GenFiltEff_mean for this dataset from AMI for normalizations
        xsec = cross_sections[idx][0]
        #effic = cross_sections[idx][1] # Do not use efficiency for MjjFilt datasets
        _h_xsecs.Fill(idx,xsec)
        print folder, xsec, folder.split('.')[0]
        mergeChannels = False
        #if folder.split('.')[0] in merged_pwhg: mergeChannels = True

        # histogram manipulation and such
        os.chdir(folder+"/")
        hf.mkdir(folder)
        hf.cd(folder)
        ROOT.gDirectory.mkdir("Normalized_XS")
        file_name = folder.split('.')
        file_name = file_name[0]
        _h_xsecs.GetXaxis().SetBinLabel(idx+1,file_name)
        if not mergeChannels:
            root_file = ROOT.TFile.Open(file_name+".root")
            root_file_add = ROOT.TFile.Open(file_name+"_add.root")
        for index, hist in enumerate(hist_list):
            if index > len(title_list)-1: index = index-len(title_list)
            # No normalization
            if mergeChannels:
                histogram,histogram_add = MergeChannels(hist,file_name)
            else:
                histogram = root_file.Get(hist)
                histogram_add = root_file_add.Get(hist)
            hf.cd(folder)
            StyleHistogram(index, histogram)
            if "CutFlow" in hist:
                StyleCutFlow(histogram_add) # Labels the Cut Flow histograms
                histogram_add.Write()
            else:
                histogram.Write()
            # Clone root histograms, normalize to XS, and move to Normalized_XS directory
            histogram_norm = histogram.Clone(hist+"_norm")
            histogram_norm.GetYaxis().SetTitle("(1/#sigma) "+y_axis_list_norm[index])
            histogram_norm.Scale(1.0/xsec)
            ROOT.gDirectory.cd("Normalized_XS")
            histogram_norm.Write()
            ROOT.gDirectory.cd()
            if "Mjj_" in hist and "Jet_1" in hist:
                th2_hist_30 = CompileDijetMass(histogram_norm,th2_hist_30)
            del histogram_norm
        hf.cd(folder)
        StyleTH2(th2_hist_30)
        th2_hist_30.Write()
        del th2_hist_30
        root_file.Close()
        hf.cd()
        os.chdir("..")
    else:
    	continue

_h_xsecs.Write()
hf.Write()
hf.Close()
print "Job Complete!!!"
