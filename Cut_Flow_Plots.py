import ROOT
import os
from Aux_Functions import *

# This script just plots a single histogram from each data set
# in datasets[]. Useful to confirm that errors are being calculated
# properly in Find_error_band.py script.

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

Colors = ["ROOT.TAttFill.kBlack", "ROOT.TAttFill.kOrange", "ROOT.TAttFill.kRed", 
        "ROOT.TAttFill.kOrange+7", "ROOT.TAttFill.kGreen+3", "ROOT.TAttFill.kViolet-6",
        "ROOT.TAttFill.kMagenta-3", "ROOT.TAttFill.kTeal+4", "ROOT.TAttFill.kBlue"]
root_file = ROOT.TFile("VBF_Systematics.root")
c1 = ROOT.TCanvas('c1','Cut_Flow_Signal',0,0,640,640)
c2 = ROOT.TCanvas('c2','Cut_Flow_Signal_MjjFilt',0,0,640,640)
c3 = ROOT.TCanvas('c3','Cut_Flow_Background',0,0,640,640)
c4 = ROOT.TCanvas('c4','Cut_Flow_Background_MjjFilt',0,0,640,640)
c1.SetLogy()
c2.SetLogy()
c3.SetLogy()
c4.SetLogy()

hist = 'CutFlow'
rebin = 1

#Draw for the Signal-----------------------------------------------------
leg = ROOT.TLegend(0.33,0.25,0.73,0.45)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)

# Signal, no Mjj_Filt
c1.cd()
for index,folder in enumerate(datasets_sig):
    new_histo = root_file.Get(folder+"/"+hist)
    new_histo.SetLineColor(eval(Colors[index]))
    leg.AddEntry(new_histo,folder,"l")
    new_histo.Draw("hist same")
leg.Draw()

c1.Update()
c1.SaveAs("Cut_Flow_Sig.pdf")
c1.Clear()
leg.Clear()

# Signal, with Mjj_Filt
c2.cd()
for index,folder in enumerate(datasets_sig_mjjfilt):
    new_histo = root_file.Get(folder+"/"+hist)
    new_histo.SetLineColor(eval(Colors[index]))
    leg.AddEntry(new_histo,folder,"l")
    new_histo.Draw("hist same")
    del new_histo
leg.Draw()

c2.Update()
c2.SaveAs("Cut_Flow_Sig_Mjj.pdf")
c2.Clear()
leg.Clear()

# Background, no Mjj_Filt
c3.cd()
for index,folder in enumerate(datasets_back):
    new_histo = root_file.Get(folder+"/"+hist)
    leg.AddEntry(new_histo,folder,"l")
    new_histo.SetLineColor(eval(Colors[index]))
    new_histo.Draw("hist same")
    del new_histo
leg.Draw()

c3.Update()
c3.SaveAs("Cut_Flow_Back.pdf")
c3.Clear()
leg.Clear()

# Background, with Mjj_Filt
c4.cd()
for index,folder in enumerate(datasets_back_mjjfilt):
    new_histo = root_file.Get(folder+"/"+hist)
    leg.AddEntry(new_histo,folder,"l")
    new_histo.SetLineColor(eval(Colors[index]))
    new_histo.Draw("hist same")
    del new_histo
leg.Draw()

c4.Update()
c4.SaveAs("Cut_Flow_Sig_Back_Mjj.pdf")
c4.Clear()
leg.Clear()