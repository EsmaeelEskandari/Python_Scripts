import ROOT
import os
import numpy as np
import math
from Aux_Functions import *

#Get DijetMass_2jet_1 histogram from 
#	["147310.CKKW30", "147312.MuFdown", "147314.MuFup", "147316.mpi1",
#	"147318.mpi2", "147320.Shower1", "147322.MuRdown", "147324.MuRup"].
#Plot histogram from each one on the same canvas...this is just to help guide me
#We need to find the difference of each theory systematic from the nominal (CKKW30),
#This must be done bin-by-bin. Add the negative shifts in quadrature and add the positive
#shifts in quadrature. Then plot the band around the nominal line. Be sure to
#include the systematic uncertainty in your subraction.

#-----------------------------------------------------------------
# Global style settings go here!
# Most of these are ATLAS defaults
style = AtlasStyle()
ROOT.gROOT.SetStyle( style.GetName() )
ROOT.gROOT.ForceStyle()
#-----------------------------------------------------------------------
	
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

lx, ly = 0.55, 0.7	# Only adjust these, the others are defined relative to these
px, py = lx+0.16, ly
qx, qy = lx, ly+0.05

datasets_sig = GetListDataset('datasets_sig')
datasets_back = GetListDataset('datasets_back')

root_file = ROOT.TFile("VBF_Systematics.root")
c1 = ROOT.TCanvas('c1','Theory_Systematics',0,0,640,960)
error_pad = ROOT.TPad('pad1','Error Band',0.,0.34,1.0,1.0)
error_pad.Draw()
ratio_pad = ROOT.TPad('pad2','Error Ratio',0.0,0.0,1.0,0.33)
ratio_pad.Draw()

hist = 'DijetMass_2jet_1'	# Change this to check another histogram
#-----Find Error Bands for Signal---------------------------------------
error_pad.cd()
error_pad.SetLogy()
nom_hist, nom_graph = FindErrorBands(datasets_sig,root_file,hist)
nom_hist.Draw("hist")
nom_graph.SetFillColor(ROOT.TAttFill.kGreen)
nom_graph.Draw("E5 same")
nom_hist.GetYaxis().SetTitleOffset(1.8)
nom_hist.Draw("hist same")
leg = MakeErrorBandLegend(nom_hist,nom_graph)
leg.Draw()
l.DrawLatex(lx,ly,"ATLAS")
p.DrawLatex(px,py,"Internal")
error_pad.Modified()

ratio_pad.cd()
ratio_plot = MakeRatioPlot(nom_hist,nom_graph)
ratio_plot.SetFillColor(ROOT.TAttFill.kYellow)
ratio_plot.SetLineColor(ROOT.TAttFill.kYellow)
# This gives us a dotted line at 'y = 1'
line = ROOT.TF1("one","1",0,1)
line.SetLineColor(1)
line.SetLineWidth(1)
line.SetLineStyle(1)
line.SetRange(300,0.5,1500,1.5)		# fix this so it gets the min_x and max_x from input nom_hist
line.SetMaximum(1.2)
line.SetMinimum(0.8)
line.GetYaxis().SetTitle("Nominal/Systematic")
line.Draw()
ratio_plot.Draw("E5 same")
line.Draw("same")
ROOT.gPad.RedrawAxis()
ratio_pad.Modified()

c1.Update()
c1.SaveAs(hist+"_signal_syst.pdf")
c1.Clear()
del nom_hist, nom_graph, line, ratio_plot

#-----Find Error Bands for Background---------------------------------------
# error_pad.cd()
# nom_hist, nom_graph = FindErrorBands(datasets_back,root_file,hist)
# nom_hist.Draw("hist")
# nom_graph.SetFillColor(ROOT.TAttFill.kGreen)
# nom_graph.Draw("E5 same")
# nom_hist.GetYaxis().SetTitleOffset(1.8)
# nom_hist.Draw("hist same")
# leg = MakeErrorBandLegend(nom_hist,nom_graph)
# leg.Draw()
# l.DrawLatex(lx,ly,"ATLAS")
# p.DrawLatex(px,py,"Internal")
# error_pad.Modified()
# 
# ratio_pad.cd()
# ratio_plot = MakeRatioPlot(nom_hist,nom_graph)
# ratio_plot.SetFillColor(ROOT.TAttFill.kYellow)
# ratio_plot.SetLineColor(ROOT.TAttFill.kYellow)
# # This gives us a dotted line at 'y = 1'
# line = ROOT.TF1("one","1",0,1)
# line.SetLineColor(1)
# line.SetLineWidth(1)
# line.SetLineStyle(1)
# line.SetRange(300,0.5,1500,1.5)
# line.SetMaximum(1.25)
# line.SetMinimum(0.75)
# line.GetYaxis().SetTitle("Nominal/Systematic")
# line.Draw()
# ratio_plot.Draw("E5 same")
# line.Draw("same")
# ROOT.gPad.RedrawAxis()
# ratio_pad.Modified()
# 
# c1.Update()
# c1.SaveAs(hist+"_background_syst.pdf")
# c1.Clear()
# del nom_hist, nom_graph, line, ratio_plot
		