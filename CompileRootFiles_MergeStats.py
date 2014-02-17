import ROOT
import os
from Aux_Functions import *
# from pyAMI.client import AMIClient
# from pyAMI.auth import AMI_CONFIG, create_auth_config
# from pyAMI.query import *
# from pyAMI.exceptions import *

hf = ROOT.TFile("VBF_Systematics_merged_stats.root", "RECREATE")

dataset_names = GetListDataset('dataset_names')
dataset_names_1 = GetListDataset('dataset_names_1')
dataset_names_2 = GetListDataset('dataset_names_2')
datasets_to_merge = dataset_names_1+dataset_names_2
hist_list = GetListDataset('hist_list')
cross_sections = GetListDataset('cross_sections')
title_list = GetListDataset('title_list')
x_axis_list = GetListDataset('x_axis_list')
y_axis_list = GetListDataset('y_axis_list')
y_axis_list_norm = GetListDataset('y_axis_list_norm')

def StyleHistogram(index, h1):
    h1.SetTitle(title_list[index])
    h1.GetXaxis().SetTitle(x_axis_list[index])
    h1.GetYaxis().SetTitle(y_axis_list[index])
    h1.SetOption("HIST E")
    
def StyleCutFlow(h1):
    h1.GetXaxis().SetBinLabel(2,"No Cuts")
    h1.GetXaxis().SetBinLabel(3, "1#it{l} & 1#nu")
    h1.GetXaxis().SetBinLabel(4, "#slash{E}_{T} > 25GeV")
    h1.GetXaxis().SetBinLabel(5, "m_T(W) > 40GeV")
    h1.GetXaxis().SetBinLabel(6, "#geq 2jets")
    h1.GetXaxis().SetBinLabel(7, "p_{T,1} > 80GeV")
    h1.GetXaxis().SetBinLabel(8, "p_{T,2} > 60GeV")
    h1.GetXaxis().SetBinLabel(9, "M_{jj} > 500GeV")
    h1.GetXaxis().SetBinLabel(10, "CJV")
    h1.GetXaxis().SetBinLabel(11, "OJV")
    
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
    
def MergeHistograms(hist1,hist2):
    bin_cont = []
    bin_err = []
    bin_cont_mjj = []
    bin_err_mjj = []
    num_xbins = hist1.GetNbinsX()
    histo = hist1.Clone()
    histo.Reset()
    for bin in range(num_xbins+2):
        bin_cont.append(hist2.GetBinContent(bin))
        bin_err.append(hist2.GetBinError(bin))
        bin_cont_mjj.append(hist1.GetBinContent(bin))
        bin_err_mjj.append(hist1.GetBinError(bin))
        
    for bin in range(num_xbins+2):
        if bin_err[bin] == 0.0: weight_nofilt = 0.0
        else: weight_nofilt = 1.0/(bin_err[bin]**2)
        if bin_err_mjj[bin] == 0.0: weight_mjjfilt = 0.0
        else: weight_mjjfilt = 1.0/(bin_err_mjj[bin]**2)
        a = weight_nofilt*bin_cont[bin]
        b = weight_mjjfilt*bin_cont_mjj[bin]
        c = weight_nofilt+weight_mjjfilt
        if c != 0.0:
            new_bin_content = (a + b)/c
            new_bin_err = math.sqrt(1.0/c)
            
        histo.SetBinContent(bin,new_bin_content)
        histo.SetBinError(bin,new_bin_err)
    
    return histo

# Folder names must be the same as in the dataset_names list in Aux_Functions.py
# I could try to get the script to just to check for run number in folder name (do this later)
# Root file needs to be named after the dataset run number
_h_xsecs = ROOT.TH1F("Cross_Sections","Cross_Sections",len(dataset_names),0,len(dataset_names))
_h_xsecs.GetYaxis().SetTitle("Cross Section [pb]")
for idx,folder in enumerate(datasets_to_merge):
    if (idx % 2 == 0):
        folder_nofilt = folder
        continue
        
    th2_hist_30 = ROOT.TH2F( "hmj1j2_wvbf", "hmj1j2_wvbf", 10, -0.5, 9.5, 200, 0, 5000 )
    th2_hist_20 = ROOT.TH2F( "hmj1j2_wvbf_20", "hmj1j2_wvbf_20", 10, -0.5, 9.5, 200, 0, 5000 )
    if os.path.exists(folder+"/") == True:
        folder_mjjfilt = folder
        # First get the crossSection_mean and GenFiltEff_mean for this dataset from AMI for normalizations
        xs_idx_mjjfilt = dataset_names.index(folder_mjjfilt)
        xs_idx_nofilt = dataset_names.index(folder_nofilt)
        xsec = (cross_sections[xs_idx_mjjfilt][0],cross_sections[xs_idx_nofilt][0])
        effic = (cross_sections[xs_idx_mjjfilt][1],1.0) # Do not use efficiency for MjjFilt datasets
        _h_xsecs.Fill(idx,xsec[0])
        print folder_mjjfilt, xsec, folder_nofilt
        
        # histogram manipulation and such
        os.chdir(folder_mjjfilt+"/")
        file_name = folder_mjjfilt.split('.')[0]
        root_file_mjjfilt = ROOT.TFile.Open(file_name+".root")
        root_file_add_mjjfilt = ROOT.TFile.Open(file_name+"_add.root")
        os.chdir("../"+folder_nofilt+"/")
        file_name = folder_nofilt.split('.')[0]
        root_file_nofilt = ROOT.TFile.Open(file_name+".root")
        root_file_add_nofilt = ROOT.TFile.Open(file_name+"_add.root")
        _h_xsecs.GetXaxis().SetBinLabel(idx+1,file_name)
        hf.mkdir(folder_mjjfilt)
        hf.cd(folder_mjjfilt)
        ROOT.gDirectory.mkdir("Normalized_XS")
        
        for index, hist in enumerate(hist_list):
            if index > len(title_list)-1: index = index-len(title_list)
            # No normalization
            histo1 = root_file_mjjfilt.Get(hist)
            histo2 = root_file_nofilt.Get(hist)
            histo1.Scale(1.0/effic[0])
            histo1_add = root_file_add_mjjfilt.Get(hist)
            histo2_add = root_file_add_nofilt.Get(hist)
            hf.cd(folder)
            if "CutFlow" in hist:
                histogram_add = histo1_add.Clone()
                histogram_add.Add(histo2)
                StyleCutFlow(histogram_add) # Labels the Cut Flow histograms
                histogram_add.Write()
            else:
                histogram = MergeHistograms(histo1,histo2)
                StyleHistogram(index, histogram)
                histogram.Write()
            # Clone root histograms, normalize to XS, and move to Normalized_XS directory
            histogram_norm = histogram.Clone(hist+"_norm")
            histogram_norm.GetYaxis().SetTitle("(1/#sigma) "+y_axis_list_norm[index])
            histogram_norm.Scale(1.0/xsec[0])
            if "Mjj_" in hist and "Jet_1" in hist:
                th2_hist_30 = CompileDijetMass(histogram_norm,th2_hist_30)
            if "Mjj_" in hist and "Jet_2" in hist:
                th2_hist_20 = CompileDijetMass(histogram_norm,th2_hist_20)
            ROOT.gDirectory.cd("Normalized_XS")
            histogram_norm.Write()
            ROOT.gDirectory.cd()
            del histogram_norm #, histogram_add, histogram
        
        hf.cd(folder_mjjfilt)
        StyleTH2(th2_hist_30)
        StyleTH2(th2_hist_20)
        th2_hist_30.Write()
        th2_hist_20.Write()
        del th2_hist_30, th2_hist_20
        root_file_mjjfilt.Close()
        root_file_add_mjjfilt.Close()
        root_file_nofilt.Close()
        root_file_add_nofilt.Close()
        hf.cd()
        os.chdir("..")
    else:
    	continue

_h_xsecs.Write()
hf.Write()
hf.Close()
print "Job Complete!!!"
