import ROOT
import os
from Aux_Functions import *
from pyAMI.client import AMIClient
from pyAMI.auth import AMI_CONFIG, create_auth_config
from pyAMI.query import *
from pyAMI.exceptions import *

hf = ROOT.TFile("VBF_Systematics.root", "RECREATE")
#th2_hist = ROOT.TH2F( "hmj1j2_wvbf", "hmj1j2_wvbf", 10, -0.5, 9.5, 200, 0, 5000 )

datasets = GetListDataset('datasets')
dataset_names = GetListDataset('dataset_names')
exp_hist_list = GetListDataset('exp_hist_list')
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

#Folder names must be the same as in the dataset_names list in Aux_Functions.py
#I could try to get the script to just to check for run number in folder name (do this later)
#Root file needs to be named after the dataset run number
for idx,folder in enumerate(dataset_names):
#for folder, data in zip(dataset_names, datasets):
    th2_hist_30 = ROOT.TH2F( "hmj1j2_wvbf_30", "hmj1j2_wvbf_30", 10, -0.5, 9.5, 200, 0, 5000 )
    th2_hist_20 = ROOT.TH2F( "hmj1j2_wvbf_20", "hmj1j2_wvbf_20", 10, -0.5, 9.5, 200, 0, 5000 )
    if os.path.exists(folder+"/") == True:
        #First get the crossSection_mean and GenFiltEff_mean for this dataset from AMI for normalizations
        xsec = cross_sections[idx][0]
        effic = cross_sections[idx][1]
        #xsec = xsec*effic          # Do not use MjjFilt efficiencies
        # if "PowhegPythia8" in data:                       # Only necessary if using AMI
        #     effic = 1.0
        #     if ".Nominal." in data: xsec = 3539.19590298
        #     if ".MuFdown." in data: xsec = 3083.52221626
        #     if ".MuFup." in data: xsec = 3870.21108023
        #     if ".MuRdown." in data: xsec = 3464.35407038
        #     if ".MuRup." in data: xsec = 3254.18183208
        #     if ".MuRdownMuFdown." in data: xsec = 3012.39734672
        #     if ".MuRupMuFup." in data: xsec = 3552.69606084
        # else:
        #     xsec, effic = get_dataset_xsec_effic(client, data)
        #     xsec = 1000*xsec*effic #Converts nb to pb and applies GenFiltEff
        print folder, xsec, effic

        #histogram manipulation and such
        os.chdir(folder+"/")
        hf.mkdir(folder)
        hf.cd(folder)
        ROOT.gDirectory.mkdir("Normalized_XS")
        # ROOT.gDirectory.mkdir("Shape_Comparisons")
        file_name = folder.split('.')
        file_name = file_name[0]
        root_file = ROOT.TFile.Open(file_name+".root")
        root_file_add = ROOT.TFile.Open(file_name+"_add.root")
        for index, hist in enumerate(hist_list):
            if index > len(title_list)-1: index = index-len(title_list)
            # No normalization
            if root_file.GetListOfKeys().Contains(hist):
              histogram = root_file.Get(hist)
              histogram_add = root_file_add.Get(hist)
            else:
              hist1 = hist.replace("_Jet_","_Jet")
              if root_file.GetListOfKeys().Contains(hist1):
                histogram = root_file.Get(hist1)
                histogram = histogram.Clone(hist)
                histogram_add = root_file_add.Get(hist1)
                histogram_add = histogram_add.Clone(hist)
              else: continue
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
            # # Clone root histograms, normalize to area, and move to Shape_Comparisons directory
            # histogram_area = histogram.Clone(hist+"_shape")
            # histogram_area.GetYaxis().SetTitle("(1/N) "+y_axis_list_norm[index])
            # integ = histogram_area.Integral("width")
            # if integ != 0.0:
            #      histogram_area.Scale(1.0/integ)
            #      ROOT.gDirectory.cd("Shape_Comparisons")
            #      histogram_area.Write()
            #      ROOT.gDirectory.cd()
            if "Mjj_" in hist and "Jet_1" in hist:
                th2_hist_30 = CompileDijetMass(histogram_norm,th2_hist_30)
            if "Mjj_" in hist and "Jet_2" in hist:
                th2_hist_20 = CompileDijetMass(histogram_norm,th2_hist_20)
            del histogram_norm #, histogram_area
        hf.cd(folder)
        StyleTH2(th2_hist_30)
        StyleTH2(th2_hist_20)
        th2_hist_30.Write()
        th2_hist_20.Write()
        del th2_hist_30, th2_hist_20
        root_file.Close()
        hf.cd()
        os.chdir("..")
    else:
    	continue

hf.Write()
hf.Close()
print "Job Complete!!!"
