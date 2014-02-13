import ROOT
import os
from Aux_Functions import *

#-------Things to do----------------------------------------------
# 1. 	Make 16 folders (one for each systematic variable)
# 2. 	Fill each folder with plots of the normalized versions of 
#		each systematic variable (min_n_tchannels and with out)
#-----------------------------------------------------------------

# #-----------------------------------------------------------------
# # Global style settings go here!
# # Most of these are ATLAS defaults
style = AtlasStyle()
ROOT.gROOT.SetStyle(style.GetName())
ROOT.gROOT.ForceStyle()
#-----------------------------------------------------------------------
	
# Open Root File
root_file = ROOT.TFile("VBF_Systematics.root")

# Create a canvas
#c1 = ROOT.TCanvas('c1','Normalized',0,0,640,640)
#c1.SetLogy()
#c2 = ROOT.TCanvas('c2','Un-normalized',0,0,640,640)
#c2.SetLogy()

# This is the ATLAS Internal Label. 
# lx,ly,px,py are the locations of the labels in NDC
l = ROOT.TLatex()
l.SetNDC()
l.SetTextFont(72)
l.SetTextSize(.05)
l.SetTextColor(1)
p = ROOT.TLatex()
p.SetNDC()
p.SetTextFont(42)
p.SetTextSize(.05)
p.SetTextColor(1)
q = ROOT.TLatex()
q.SetNDC()
q.SetTextFont(42)
q.SetTextSize(.03)
q.SetTextColor(1)

lx, ly = 0.63, 0.63	# Only adjust these, the others are defined relative to these
px, py = lx+0.16, ly
qx, qy = lx, ly+0.05

leg = ROOT.TLegend(0.4,0.77,0.6,0.87)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)

#---------------------------------------------------------------------

hist = "DijetMass_2jet_1"

sherpa_mjj_norm = root_file.Get("129930.Nominal_Sherpa_Background_MjjFilt/Normalized_XS/"+hist+"_norm")
sherpa_norm = root_file.Get("147775.Nominal_Sherpa_Background/Normalized_XS/"+hist+"_norm")
powheg_bsf_norm = root_file.Get("000001.Powheg.W2jets.Nominal/Normalized_XS/"+hist+"_norm")
sherpa_mjj = root_file.Get("129930.Nominal_Sherpa_Background_MjjFilt/"+hist)
sherpa = root_file.Get("147775.Nominal_Sherpa_Background/"+hist)
powheg_bsf = root_file.Get("000001.Powheg.W2jets.Nominal/"+hist)

c1.cd()
sherpa_mjj_norm.SetLineColor(ROOT.TAttLine.kBlue)
sherpa_norm.SetLineColor(ROOT.TAttLine.kRed)
powheg_bsf_norm.SetLineColor(ROOT.TAttLine.kBlack)
sherpa_mjj_norm.Rebin(5)
sherpa_norm.Rebin(5)
powheg_bsf_norm.Rebin(5)

max_vals = [sherpa_mjj_norm.GetMaximum(),sherpa_norm.GetMaximum(),powheg_bsf_norm.GetMaximum()]
sherpa_mjj_norm.SetMaximum(5*max(max_vals))

sherpa_mjj_norm.Draw("HIST E")
sherpa_norm.Draw("HIST E SAME")
powheg_bsf_norm.Draw("HIST E SAME")
l.DrawLatex(lx,ly,"ATLAS")
p.DrawLatex(px,py,"Internal")
leg.AddEntry(sherpa_mjj_norm,"Sherpa Nominal MjjFilt","l")
leg.AddEntry(sherpa_norm,"Sherpa Nominal","l")
leg.AddEntry(powheg_bsf_norm,"POWHEG Nominal bornsuppfact","l")
leg.Draw()

c1.SaveAs("Normalized.pdf")
c1.Clear()

c2.cd()
sherpa_mjj.SetLineColor(ROOT.TAttLine.kBlue)
sherpa.SetLineColor(ROOT.TAttLine.kRed)
powheg_bsf.SetLineColor(ROOT.TAttLine.kBlack)
sherpa_mjj.Rebin(5)
sherpa.Rebin(5)
powheg_bsf.Rebin(5)

max_vals = [sherpa_mjj.GetMaximum(),sherpa.GetMaximum(),powheg_bsf.GetMaximum()]
sherpa_mjj.SetMaximum(5*max(max_vals))

sherpa_mjj.Draw("HIST E")
sherpa.Draw("HIST E SAME")
powheg_bsf.Draw("HIST E SAME")
l.DrawLatex(lx,ly,"ATLAS")
p.DrawLatex(px,py,"Internal")
leg.Draw()

c2.SaveAs("Distribution.pdf")
c2.Clear()
          