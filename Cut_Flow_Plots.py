import ROOT
import os
from Aux_Functions import *

# This script just plots a single histogram from each data set
# in datasets[]. Useful to confirm that errors are being calculated
# properly in Find_error_band.py script.

def StyleAcceptHist(h1):
    h1.GetYaxis().SetTitle("Cross Section [pb]")
    h1.GetXaxis().SetBinLabel(2, "Nominal")
    h1.GetXaxis().SetBinLabel(3, "CKKW30")
    h1.GetXaxis().SetBinLabel(4, "MuFdown")
    h1.GetXaxis().SetBinLabel(5, "MuFup")
    h1.GetXaxis().SetBinLabel(6, "mpi1")
    h1.GetXaxis().SetBinLabel(7, "mpi2")
    h1.GetXaxis().SetBinLabel(8, "Shower1")
    h1.GetXaxis().SetBinLabel(9, "MuRdown")
    h1.GetXaxis().SetBinLabel(10, "MuRup")
    
def StyleAcceptPWHG(h1):
    h1.GetYaxis().SetTitle("Cross Section [pb]")
    h1.GetXaxis().SetBinLabel(2, "Nominal")
    h1.GetXaxis().SetBinLabel(3, "MuFdown")
    h1.GetXaxis().SetBinLabel(4, "MuFup")
    h1.GetXaxis().SetBinLabel(5, "MuRdown")
    h1.GetXaxis().SetBinLabel(6, "MuRup")
    h1.GetXaxis().SetBinLabel(7, "MuRdownMuFdown")
    h1.GetXaxis().SetBinLabel(8, "MuRupMuFup")

#-----------------------------------------------------------------
# Global style settings go here!
# Most of these are ATLAS defaults
style = AtlasStyle()
ROOT.gROOT.SetStyle( style.GetName() )
ROOT.gROOT.ForceStyle()
#-----------------------------------------------------------------------
datasets_sig = GetListDataset('datasets_sig')
datasets_back = GetListDataset('datasets_back')
datasets_sig_mjjfilt = GetListDataset('datasets_sig_MjjFilt')
datasets_back_mjjfilt = GetListDataset('datasets_back_MjjFilt')
cross_sections = GetListDataset('cross_sections')
dataset_names = GetListDataset('dataset_names')
pwhg_back_bornsupp = GetListDataset('pwhg_back_bornsupp')
pwhg_sig_bornsupp = GetListDataset('pwhg_sig_bornsupp')
pwhg_sig_ptjgencut = GetListDataset('pwhg_sig_ptjgencut')

Colors = ["ROOT.TAttFill.kBlack", "ROOT.TAttFill.kOrange", "ROOT.TAttFill.kRed", 
        "ROOT.TAttFill.kOrange+7", "ROOT.TAttFill.kGreen+3", "ROOT.TAttFill.kViolet-6",
        "ROOT.TAttFill.kMagenta-3", "ROOT.TAttFill.kTeal+4", "ROOT.TAttFill.kBlue"]
root_file = ROOT.TFile("VBF_Systematics.root")



events_passed_sig = MakeCutFlow(datasets_sig,root_file,"Sherpa_Signal")
events_passed_sig_mjj = MakeCutFlow(datasets_sig_mjjfilt,root_file,"Sherpa_Signal_MjjFilt")
events_passed_sig_pwg = [0,0]+MakeCutFlow(pwhg_sig_bornsupp,root_file,"POWHEG_Signal_bornsuppfact")
events_passed_sig_ptj = [0,0]+MakeCutFlow(pwhg_sig_ptjgencut,root_file,"POWHEG_Signal_ptj_gencut")
events_passed_back = MakeCutFlow(datasets_back,root_file,"Sherpa_Background")
events_passed_back_mjj = MakeCutFlow(datasets_back_mjjfilt,root_file,"Sherpa_Background_MjjFilt")
events_passed_back_pwg = [0,0]+MakeCutFlow(pwhg_back_bornsupp,root_file,"POWHEG_Background_bornsuppfact")
 
# # Create the histograms that show the signal acceptance per variation
c7 = ROOT.TCanvas('c7','Signal_Acceptance',0,0,640,640)
accept_sig = ROOT.TH1F("accept_sig","Event Acceptance - Signal",10,0,10)
accept_sig_mjj = ROOT.TH1F("accept_sig_mjj","Event Acceptance - Signal (Dijet Mass Filter)",10,0,10)
accept_sig_pwhg = ROOT.TH1F("accept_sig_pwhg", "Event Acceptance - Signal (POWHEG, bornsuppfact)",10,0,10)
accept_sig_pwhg_ptj = ROOT.TH1F("accept_sig_pwhg_ptj", "Event Acceptance - Signal (POWHEG, ptj_gencut)",10,0,10)
accept_back = ROOT.TH1F("accept_back","Event Acceptance - Background",10,0,10)
accept_back_mjj = ROOT.TH1F("accept_back_mjj","Event Acceptance - Background (Dijet Mass Filter)",10,0,10)
accept_back_pwhg = ROOT.TH1F("accept_back_pwhg","Event Acceptance - Background (POWHEG, bornsuppfact)",10,0,10)

for index in range(1,10):
    accept_sig.Fill(index,events_passed_sig[index-1])
    accept_sig_mjj.Fill(index,events_passed_sig_mjj[index-1])
    accept_sig_pwhg.Fill(index-2,events_passed_sig_pwg[index-1])
    accept_sig_pwhg_ptj.Fill(index-2,events_passed_sig_ptj[index-1])
    accept_back.Fill(index,events_passed_back[index-1])
    accept_back_mjj.Fill(index,events_passed_back_mjj[index-1])
    accept_back_pwhg.Fill(index-2,events_passed_back_pwg[index-1])
    
hists_accept = [accept_sig, accept_sig_mjj, accept_sig_pwhg, accept_sig_pwhg_ptj, accept_back, accept_back_mjj, accept_back_pwhg]    
    
StyleAcceptHist(accept_sig)
StyleAcceptHist(accept_sig_mjj)
StyleAcceptPWHG(accept_sig_pwhg)
StyleAcceptPWHG(accept_sig_pwhg_ptj)
StyleAcceptHist(accept_back)
StyleAcceptHist(accept_back_mjj)
StyleAcceptPWHG(accept_back_pwhg)
  
for idx,histogram in enumerate(hists_accept):
    c7.cd()
    histogram.Draw()
    name = histogram.GetTitle()
    c7.Update()
    c7.SaveAs(name+".pdf")
    c7.Clear()
