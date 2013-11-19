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

Max_Vals = []
root_file = ROOT.TFile("VBF_Systematics.root")
c1 = ROOT.TCanvas('c1','Dijet_Mass_Systematics',0,0,640,640)
c1.SetLogy()

hist = 'DijetMass_2jet_1'
rebin = 4

#Draw for the Signal-----------------------------------------------------
leg = ROOT.TLegend(0.5,0.67,0.9,0.87)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)

nom_hist = root_file.Get(datasets_sig[0]+"/Normalized_XS/"+hist+"_norm")
nom_hist = nom_hist.Clone()
nom_hist.Rebin(rebin)
Max_Vals.append(nom_hist.GetMaximum())
leg.AddEntry(nom_hist,datasets_sig[0],"l")

CKKW30_hist = root_file.Get(datasets_sig[1]+"/Normalized_XS/"+hist+"_norm")
CKKW30_hist = CKKW30_hist.Clone()
CKKW30_hist.Rebin(rebin)
CKKW30_hist.SetLineColor(ROOT.TAttFill.kOrange)
Max_Vals.append(CKKW30_hist.GetMaximum())
leg.AddEntry(CKKW30_hist,datasets_sig[1],"l")

MuFdown_hist = root_file.Get(datasets_sig[2]+"/Normalized_XS/"+hist+"_norm")
MuFdown_hist = MuFdown_hist.Clone()
MuFdown_hist.Rebin(rebin)
MuFdown_hist.SetLineColor(ROOT.TAttFill.kRed)
Max_Vals.append(MuFdown_hist.GetMaximum())
leg.AddEntry(MuFdown_hist,datasets_sig[2],"l")

MuFup_hist = root_file.Get(datasets_sig[3]+"/Normalized_XS/"+hist+"_norm")
MuFup_hist = MuFup_hist.Clone()
MuFup_hist.Rebin(rebin)
MuFup_hist.SetLineColor(ROOT.TAttFill.kOrange+7)
Max_Vals.append(MuFup_hist.GetMaximum())
leg.AddEntry(MuFup_hist,datasets_sig[3],"l")

mpi1_hist = root_file.Get(datasets_sig[4]+"/Normalized_XS/"+hist+"_norm")
mpi1_hist = mpi1_hist.Clone()
mpi1_hist.Rebin(rebin)
mpi1_hist.SetLineColor(ROOT.TAttFill.kGreen+3)
Max_Vals.append(mpi1_hist.GetMaximum())
leg.AddEntry(mpi1_hist,datasets_sig[4],"l")

mpi2_hist = root_file.Get(datasets_sig[5]+"/Normalized_XS/"+hist+"_norm")
mpi2_hist = mpi2_hist.Clone()
mpi2_hist.Rebin(rebin)
mpi2_hist.SetLineColor(ROOT.TAttFill.kViolet-6)
Max_Vals.append(mpi2_hist.GetMaximum())
leg.AddEntry(mpi2_hist,datasets_sig[5],"l")

Shower1_hist = root_file.Get(datasets_sig[6]+"/Normalized_XS/"+hist+"_norm")
Shower1_hist = Shower1_hist.Clone()
Shower1_hist.Rebin(rebin)
Shower1_hist.SetLineColor(ROOT.TAttFill.kMagenta-3)
Max_Vals.append(Shower1_hist.GetMaximum())
leg.AddEntry(Shower1_hist,datasets_sig[6],"l")

MuRdown_hist = root_file.Get(datasets_sig[7]+"/Normalized_XS/"+hist+"_norm")
MuRdown_hist = MuRdown_hist.Clone()
MuRdown_hist.Rebin(rebin)
MuRdown_hist.SetLineColor(ROOT.TAttFill.kTeal+4)
Max_Vals.append(MuRdown_hist.GetMaximum())
leg.AddEntry(MuRdown_hist,datasets_sig[7],"l")

MuRup_hist = root_file.Get(datasets_sig[8]+"/Normalized_XS/"+hist+"_norm")
MuRup_hist = MuRup_hist.Clone()
MuRup_hist.Rebin(rebin)
MuRup_hist.SetLineColor(ROOT.TAttFill.kBlue)
Max_Vals.append(MuRup_hist.GetMaximum())
leg.AddEntry(MuRup_hist,datasets_sig[8],"l")

Max = max(Max_Vals)

nom_hist.SetMaximum(Max*1.05)
nom_hist.Draw("hist")
CKKW30_hist.Draw("hist same")
MuFdown_hist.Draw("hist same")
MuFup_hist.Draw("hist same")
mpi1_hist.Draw("hist same")
mpi2_hist.Draw("hist same")
Shower1_hist.Draw("hist same")
MuRdown_hist.Draw("hist same")
MuRup_hist.Draw("hist same")
nom_hist.Draw("hist same")
leg.Draw()

c1.Update()
c1.SaveAs("Signal_Plots.pdf")
c1.Clear()
del nom_hist, CKKW30_hist, MuFdown_hist, mpi1_hist, mpi2_hist, Shower1_hist, MuRdown_hist, MuRup_hist, leg
Max_Vals = []

#Drow for the Background-----------------------------------------------------
leg = ROOT.TLegend(0.5,0.67,0.9,0.87)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)

nom_hist = root_file.Get(datasets_back[0]+"/Normalized_XS/"+hist+"_norm")
nom_hist = nom_hist.Clone()
nom_hist.Rebin(rebin)
Max_Vals.append(nom_hist.GetMaximum())
leg.AddEntry(nom_hist,datasets_back[0],"l")

CKKW30_hist = root_file.Get(datasets_back[1]+"/Normalized_XS/"+hist+"_norm")
CKKW30_hist = CKKW30_hist.Clone()
CKKW30_hist.Rebin(rebin)
CKKW30_hist.SetLineColor(ROOT.TAttFill.kOrange)
Max_Vals.append(CKKW30_hist.GetMaximum())
leg.AddEntry(CKKW30_hist,datasets_back[1],"l")

MuFdown_hist = root_file.Get(datasets_back[2]+"/Normalized_XS/"+hist+"_norm")
MuFdown_hist = MuFdown_hist.Clone()
MuFdown_hist.Rebin(rebin)
MuFdown_hist.SetLineColor(ROOT.TAttFill.kRed)
Max_Vals.append(MuFdown_hist.GetMaximum())
leg.AddEntry(MuFdown_hist,datasets_back[2],"l")

MuFup_hist = root_file.Get(datasets_back[3]+"/Normalized_XS/"+hist+"_norm")
MuFup_hist = MuFup_hist.Clone()
MuFup_hist.Rebin(rebin)
MuFup_hist.SetLineColor(ROOT.TAttFill.kOrange+7)
Max_Vals.append(MuFup_hist.GetMaximum())
leg.AddEntry(MuFup_hist,datasets_back[3],"l")

mpi1_hist = root_file.Get(datasets_back[4]+"/Normalized_XS/"+hist+"_norm")
mpi1_hist = mpi1_hist.Clone()
mpi1_hist.Rebin(rebin)
mpi1_hist.SetLineColor(ROOT.TAttFill.kGreen+3)
Max_Vals.append(mpi1_hist.GetMaximum())
leg.AddEntry(mpi1_hist,datasets_back[4],"l")

mpi2_hist = root_file.Get(datasets_back[5]+"/Normalized_XS/"+hist+"_norm")
mpi2_hist = mpi2_hist.Clone()
mpi2_hist.Rebin(rebin)
mpi2_hist.SetLineColor(ROOT.TAttFill.kViolet-6)
Max_Vals.append(mpi2_hist.GetMaximum())
leg.AddEntry(mpi2_hist,datasets_back[5],"l")

Shower1_hist = root_file.Get(datasets_back[6]+"/Normalized_XS/"+hist+"_norm")
Shower1_hist = Shower1_hist.Clone()
Shower1_hist.Rebin(rebin)
Shower1_hist.SetLineColor(ROOT.TAttFill.kMagenta-3)
Max_Vals.append(Shower1_hist.GetMaximum())
leg.AddEntry(Shower1_hist,datasets_back[6],"l")

MuRdown_hist = root_file.Get(datasets_back[7]+"/Normalized_XS/"+hist+"_norm")
MuRdown_hist = MuRdown_hist.Clone()
MuRdown_hist.Rebin(rebin)
MuRdown_hist.SetLineColor(ROOT.TAttFill.kTeal+4)
Max_Vals.append(MuRdown_hist.GetMaximum())
leg.AddEntry(MuRdown_hist,datasets_back[7],"l")

MuRup_hist = root_file.Get(datasets_back[8]+"/Normalized_XS/"+hist+"_norm")
MuRup_hist = MuRup_hist.Clone()
MuRup_hist.Rebin(rebin)
MuRup_hist.SetLineColor(ROOT.TAttFill.kBlue)
Max_Vals.append(MuRup_hist.GetMaximum())
leg.AddEntry(MuRup_hist,datasets_back[8],"l")

Max = max(Max_Vals)

nom_hist.SetMaximum(Max*1.05)
nom_hist.Draw("hist")
CKKW30_hist.Draw("hist")
MuFdown_hist.Draw("hist same")
MuFup_hist.Draw("hist same")
mpi1_hist.Draw("hist same")
mpi2_hist.Draw("hist same")
Shower1_hist.Draw("hist same")
MuRdown_hist.Draw("hist same")
MuRup_hist.Draw("hist same")
nom_hist.Draw("hist same")
leg.Draw()

c1.Update()
c1.SaveAs("Background_Plots.pdf")