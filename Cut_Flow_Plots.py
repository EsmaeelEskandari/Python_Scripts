import ROOT
import os
from Aux_Functions import *

# This script just plots a single histogram from each data set
# in datasets[]. Useful to confirm that errors are being calculated
# properly in Find_error_band.py script.

# TODO: use dataset name to find index in dataset_names list, then take cross-section
#       at that location in cross_sections list

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

Colors = ["ROOT.TAttFill.kBlack", "ROOT.TAttFill.kOrange", "ROOT.TAttFill.kRed", 
        "ROOT.TAttFill.kOrange+7", "ROOT.TAttFill.kGreen+3", "ROOT.TAttFill.kViolet-6",
        "ROOT.TAttFill.kMagenta-3", "ROOT.TAttFill.kTeal+4", "ROOT.TAttFill.kBlue"]
root_file = ROOT.TFile("VBF_Systematics.root")
c1 = ROOT.TCanvas('c1','Cut_Flow_Signal',0,0,640,640)
c2 = ROOT.TCanvas('c2','Cut_Flow_Signal_MjjFilt',0,0,640,640)
c3 = ROOT.TCanvas('c3','Cut_Flow_Signal_Powheg',0,0,640,640)
c4 = ROOT.TCanvas('c4','Cut_Flow_Background',0,0,640,640)
c5 = ROOT.TCanvas('c5','Cut_Flow_Background_MjjFilt',0,0,640,640)
c6 = ROOT.TCanvas('c6','Cut_Flow_Background_Powheg',0,0,640,640)
c1.SetLogy()
c2.SetLogy()
c3.SetLogy()
c4.SetLogy()
c5.SetLogy()
c6.SetLogy()

hist = 'CutFlow_1'

#Draw for the Signal-----------------------------------------------------
leg = ROOT.TLegend(0.2,0.2,0.5,0.4)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)

# Signal, no Mjj_Filt
c1.cd()
events_passed_sig = []
for index,folder in enumerate(datasets_sig):
    xs_index = dataset_names.index(folder)
    xsec = cross_sections[xs_index][0]
    new_histo = root_file.Get(folder+"/"+hist)
    if "129916" in folder: new_histo.Scale(0.25)
    new_histo.SetLineColor(eval(Colors[index]))
    leg.AddEntry(new_histo,folder,"l")
    new_histo.Draw("hist same")
    events_passed_sig.append(new_histo.GetBinContent(11)/new_histo.GetBinContent(2)*xsec)
    del new_histo
leg.Draw()

c1.Update()
c1.SaveAs("Cut_Flow_Sig.pdf")
c1.Clear()
leg.Clear()

# Signal, with Mjj_Filt
c2.cd()
events_passed_sig_mjj = []
for index,folder in enumerate(datasets_sig_mjjfilt):
    xs_index = dataset_names.index(folder)
    xsec = cross_sections[xs_index][0]
    new_histo = root_file.Get(folder+"/"+hist)
    new_histo.SetLineColor(eval(Colors[index]))
    leg.AddEntry(new_histo,folder,"l")
    new_histo.Draw("hist same")
    events_passed_sig_mjj.append(new_histo.GetBinContent(11)/new_histo.GetBinContent(2)*xsec)
    del new_histo
leg.Draw()

c2.Update()
c2.SaveAs("Cut_Flow_Sig_Mjj.pdf")
c2.Clear()
leg.Clear()

# POWHEG - Signal, bornsuppfact
c3.cd()
events_passed_sig_pwg = [0,0]
for index,folder in enumerate(pwhg_sig_bornsupp):
    xs_index = dataset_names.index(folder)
    xsec = cross_sections[xs_index][0]
    new_histo = root_file.Get(folder+"/"+hist)
    new_histo.SetLineColor(eval(Colors[index]))
    leg.AddEntry(new_histo,folder,"l")
    new_histo.Draw("hist same")
    events_passed_sig_pwg.append(new_histo.GetBinContent(11)/new_histo.GetBinContent(2)*xsec)
    del new_histo
leg.Draw()

c3.Update()
c3.SaveAs("Cut_Flow_Sig_PWHG.pdf")
c3.Clear()
leg.Clear()

# Background, no Mjj_Filt
c4.cd()
events_passed_back = []
for index,folder in enumerate(datasets_back):
    xs_index = dataset_names.index(folder)
    xsec = cross_sections[xs_index][0]
    new_histo = root_file.Get(folder+"/"+hist)
    if "147775" in folder: new_histo.Scale(0.5)
    leg.AddEntry(new_histo,folder,"l")
    new_histo.SetLineColor(eval(Colors[index]))
    new_histo.Draw("hist same")
    events_passed_back.append(new_histo.GetBinContent(11)/new_histo.GetBinContent(2)*xsec)
    del new_histo
leg.Draw()

c4.Update()
c4.SaveAs("Cut_Flow_Back.pdf")
c4.Clear()
leg.Clear()

# Background, with Mjj_Filt
c5.cd()
events_passed_back_mjj = []
for index,folder in enumerate(datasets_back_mjjfilt):
    xs_index = dataset_names.index(folder)
    xsec = cross_sections[xs_index][0]
    new_histo = root_file.Get(folder+"/"+hist)
    leg.AddEntry(new_histo,folder,"l")
    new_histo.SetLineColor(eval(Colors[index]))
    new_histo.Draw("hist same")
    events_passed_back_mjj.append(new_histo.GetBinContent(11)/new_histo.GetBinContent(2)*xsec)
    del new_histo
leg.Draw()

c5.Update()
c5.SaveAs("Cut_Flow_Back_Mjj.pdf")
c5.Clear()
leg.Clear()

# POWHEG - Background, bornsuppfact
c6.cd()
events_passed_back_pwg = [0,0]
for index,folder in enumerate(pwhg_back_bornsupp):
    xs_index = dataset_names.index(folder)
    xsec = cross_sections[xs_index][0]
    new_histo = root_file.Get(folder+"/"+hist)
    leg.AddEntry(new_histo,folder,"l")
    new_histo.SetLineColor(eval(Colors[index]))
    new_histo.Draw("hist same")
    events_passed_back_pwg.append(new_histo.GetBinContent(11)/new_histo.GetBinContent(2)*xsec)
    del new_histo
leg.Draw()

c6.Update()
c6.SaveAs("Cut_Flow_Back_PWHG.pdf")
c6.Clear()
leg.Clear()

# Create the histograms that show the signal acceptance per uncertainty
c7 = ROOT.TCanvas('c6','Signal_Acceptance',0,0,640,640)
c8 = ROOT.TCanvas('c7','Signal_Acceptance_MjjFilt',0,0,640,640)
c9 = ROOT.TCanvas('c9','POWHEG_Sig_Acceptance',0,0,640,640)
c10 = ROOT.TCanvas('c10','Background_Acceptance',0,0,640,640)
c11 = ROOT.TCanvas('c11','Background_Acceptance_MjjFilt',0,0,640,640)
c12 = ROOT.TCanvas('c12','POWHEG_Back_Acceptance',0,0,640,640)
accept_sig = ROOT.TH1F("accept_sig","Event Acceptance - Signal",10,0,10)
accept_sig_mjj = ROOT.TH1F("accept_sig_mjj","Event Acceptance - Signal (Dijet Mass Filter)",10,0,10)
accept_sig_pwhg = ROOT.TH1F("accept_sig_pwhg", "Event Acceptance - Signal (POWHEG, bornsuppfact)",10,0,10)
accept_back = ROOT.TH1F("accept_back","Event Acceptance - Background",10,0,10)
accept_back_mjj = ROOT.TH1F("accept_back_mjj","Event Acceptance - Background (Dijet Mass Filter)",10,0,10)
accept_back_pwhg = ROOT.TH1F("accept_back_pwhg","Event Acceptance - Background (POWHEG, bornsuppfact)",10,0,10)

for index in range(1,10):
    accept_sig.Fill(index,events_passed_sig[index-1])
    accept_sig_mjj.Fill(index,events_passed_sig_mjj[index-1])
    accept_sig_pwhg.Fill(index-2,events_passed_sig_pwg[index-1])
    accept_back.Fill(index,events_passed_back[index-1])
    accept_back_mjj.Fill(index,events_passed_back_mjj[index-1])
    accept_back_pwhg.Fill(index-2,events_passed_back_pwg[index-1])
    
StyleAcceptHist(accept_sig)
StyleAcceptHist(accept_sig_mjj)
StyleAcceptPWHG(accept_sig_pwhg)
StyleAcceptHist(accept_back)
StyleAcceptHist(accept_back_mjj)
StyleAcceptPWHG(accept_back_pwhg)
    
c7.cd()
accept_sig.Draw()
c7.Update()
c7.SaveAs("accept_sig.pdf")
c7.Clear()

c8.cd()
accept_sig_mjj.Draw()
c8.Update()
c8.SaveAs("accept_sig_mjj.pdf")
c8.Clear()

c9.cd()
accept_sig_pwhg.Draw()
c9.Update()
c9.SaveAs("accept_sig_PWHG.pdf")
c9.Clear()

c10.cd()
accept_back.Draw()
c10.Update()
c10.SaveAs("accept_back.pdf")
c10.Clear()

c11.cd()
accept_back_mjj.Draw()
c11.Update()
c11.SaveAs("accept_back_mjj.pdf")
c11.Clear()

c12.cd()
accept_back_pwhg.Draw()
c12.Update()
c12.SaveAs("accept_back_PWHG.pdf")
c12.Clear()
