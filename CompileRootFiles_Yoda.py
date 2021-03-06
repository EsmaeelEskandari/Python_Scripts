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
exp_hist_list = GetListDataset('exp_hist_list')
# hist_list = GetListDataset('hist_list')
# cross_sections = GetListDataset('cross_sections')
# title_list = GetListDataset('title_list')
# x_axis_list = GetListDataset('x_axis_list')
# y_axis_list = GetListDataset('y_axis_list')
# y_axis_list_norm = GetListDataset('y_axis_list_norm')
histDict = GetListDataset('dictList')
analysis = 'VBF_W_NLO'

def StyleHistogram(h1,titles):
    h1.SetTitle(titles[0])
    h1.GetXaxis().SetTitle(titles[1])
    h1.GetYaxis().SetTitle(titles[2])
    h1.SetOption("HIST E")
    
def StyleCutFlow(h1):
    h1.GetXaxis().SetBinLabel(1, "No Cuts")
    h1.GetXaxis().SetBinLabel(2, "One W Boson")
    h1.GetXaxis().SetBinLabel(3, "N_{jets} >= 2")
    h1.GetXaxis().SetBinLabel(4, "MET > 25 GeV")
    h1.GetXaxis().SetBinLabel(5, "p_{T,1} > 80GeV")
    h1.GetXaxis().SetBinLabel(6, "p_{T,2} > 60GeV")
    h1.GetXaxis().SetBinLabel(7, "M_{jj} > 500GeV")
    h1.GetXaxis().SetBinLabel(8, "#Delta #eta > 2")
    h1.GetXaxis().SetBinLabel(9, "M_{T}(W) > 40GeV")
    h1.GetXaxis().SetBinLabel(10, "CJV")
    h1.GetXaxis().SetBinLabel(11, "OLV")
    h1.GetXaxis().SetBinLabel(12, "Signal Region")
    
def StyleRegPop(h1):
    binNames = { 1: 'AllEvents', 2: 'Inclusive', 3: 'HighMass15', 4: 'HighMass20', 5: '!LC',
                 6: '!JC', 7: '!LC!JC', 8: 'Signal', 9: 'aTGC_WpT500', 10: 'aTGC_WpT600',
                 11: 'aTGC_WpT700', 12: 'aTGC_MT10', 13: 'aTGC_MT20', 14: 'aTGC_Mjj1000',
                 15: 'HighMass10', 16: 'Signal10' }
    for bin in binNames:
        h1.GetXaxis().SetBinLabel(bin, binNames[bin])
    
def StyleTH2(th2):
    th2.SetTitle("Differential Dijet Mass and N_{jets} Distribution")
    th2.GetXaxis().SetTitle("N_{jets} in event")
    th2.GetYaxis().SetTitle("Dijet Mass [GeV]")
    th2.GetZaxis().SetTitle("(1/#sigma) d#sigma/d#m_{jj}dN_{jets}")
    th2.SetOption("LEGO2 0")
    
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

# Folder names must be the same as in the dataset_names list in Aux_Functions.py
# I could try to get the script to just to check for run number in folder name (do this later)
# Root file needs to be named after the dataset run number
_h_xsecs = ROOT.TH1F("Cross_Sections","Cross_Sections",len(dataset_names),0,len(dataset_names))
_h_xsecs.GetYaxis().SetTitle("Cross Section [pb]")
idx = 0
for folder in sorted(dataset_names):
    idx += 1
    if os.path.exists(folder+"/") == True: # and not os.listdir("./"+folder+"/"):
        th2_hist_30 = ROOT.TH2F( "hmj1j2_wvbf", "hmj1j2_wvbf", 10, -0.5, 9.5, 200, 0, 5000 )
        # First get the crossSection_mean and GenFiltEff_mean for this dataset from AMI for normalizations
        xsec = dataset_names[folder][0]
        #effic = dataset_names[folder][1] # Do not use efficiency for MjjFilt datasets
        print folder, xsec

        # histogram manipulation and such
        os.chdir(folder+"/")
        hf.mkdir(folder)
        hf.cd(folder)
        ROOT.gDirectory.mkdir("Normalized_XS")
        file_name = folder.split('.')
        file_name = file_name[0]
        _h_xsecs.GetXaxis().SetBinLabel(idx,file_name)
        _h_xsecs.Fill(idx,xsec)
        root_file = ROOT.TFile.Open(file_name+".root")
        #root_file_add = ROOT.TFile.Open(file_name+"_add.root")
        #if not(root_file) or not(root_file_add):
        if not(root_file):
          os.chdir("..")
          continue
        for hist in histDict:
          for ext in [ "", "_ewkonly" ]:
            # No normalization
            keyName = hist
            if hist[-2:] == "_1": hist = hist[:-2]
            # if "CutFlow" in hist:
            #     histo = root_file_add.Get(analysis+'/'+hist+ext)
            # elif "RegionPop" in hist:
            #     histo = root_file_add.Get(analysis+'/'+hist+ext)
            # else:
            #     histo = root_file.Get(analysis+'/'+hist+ext)
            histo = root_file.Get(analysis+'/'+hist+ext)
            root_file.Get(analysis+'/'+hist+ext)
            if not histo:
                print "No histogram for {0} found.".format(hist+ext)
                continue
            histogram = histo.Clone(hist+ext)
            hf.cd(folder)
            StyleHistogram(histogram,histDict[keyName])
            if "CutFlow" in hist: StyleCutFlow(histogram)
            if "RegionPop" in hist: StyleRegPop(histogram)
            histogram.Write()
            # Clone root histograms, normalize to XS, and move to Normalized_XS directory
            histogram_norm = histogram.Clone(hist+ext+"_norm")
            histogram_norm.GetYaxis().SetTitle("(1/#sigma) "+histDict[keyName][3])
            histogram_norm.Scale(1.0/xsec)
            ROOT.gDirectory.cd("Normalized_XS")
            histogram_norm.Write()
            ROOT.gDirectory.cd()
            if "Mjj_Excl" in hist:
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
