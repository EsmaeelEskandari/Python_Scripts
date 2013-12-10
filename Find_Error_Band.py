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
px, py = lx+0.13, ly
qx, qy = lx, ly+0.05

datasets_sig = GetListDataset('datasets_sig')
datasets_back = GetListDataset('datasets_back')
datasets_sig_MjjFilt = GetListDataset('datasets_sig_MjjFilt')
datasets_back_MjjFilt = GetListDataset('datasets_back_MjjFilt')
dataset_lists_to_check = [datasets_sig,datasets_sig_MjjFilt,datasets_back,datasets_back_MjjFilt]
dataset_lists_names = ['Sig','Sig_MjjFilt','Back','Back_MjjFilt']

root_file = ROOT.TFile("VBF_Systematics.root")
c1 = ROOT.TCanvas('c1','Theory_Systematics',0,0,640,960)

#hist = 'DijetMass_2jet_1'	# Change this to check another histogram
hists_to_comp = ['DijetMass_2jet_1','FirstJetPt_2jet_1','Ht_2jet_1']

#-----Find Error Bands for Signal---------------------------------------
for idx,dataset_list in enumerate(dataset_lists_to_check):
    for hist in hists_to_comp:
	error_pad = ROOT.TPad('pad1','Error Band',0.,0.34,1.0,1.0)
	ratio_pad = ROOT.TPad('pad2','Error Ratio',0.0,0.0,1.0,0.33)
	error_pad.Draw()
	ratio_pad.Draw()

	error_pad.cd()
	error_pad.SetLogy()
	nom_hist, nom_graph, tot_stat_errors = FindErrorBands(dataset_list,root_file,hist)
	nom_hist.Draw("hist")
	nom_graph.SetFillColor(ROOT.TAttFill.kGreen)
	nom_graph.Draw("E5 same")
	nom_hist.GetYaxis().SetTitleOffset(1)
	nom_hist.Draw("hist same")
	leg = MakeErrorBandLegend(nom_hist,nom_graph)
	leg.Draw()
	l.DrawLatex(lx,ly,"ATLAS")
	p.DrawLatex(px,py,"Internal")
	error_pad.Modified()

	ratio_pad.cd()
	ratio_plot, stat_plot = MakeRatioPlot(nom_hist,nom_graph,tot_stat_errors)
	ratio_plot.SetFillColor(ROOT.TAttFill.kYellow)
	ratio_plot.SetLineColor(ROOT.TAttFill.kYellow)
	stat_plot.SetFillColor(ROOT.TAttFill.kRed-7)
	stat_plot.SetLineColor(ROOT.TAttFill.kRed-7)
	# This gives us a dotted line at 'y = 1'
	line = ROOT.TF1("one","1",0,1)
	line.SetLineColor(1)
	line.SetLineWidth(1)
	line.SetLineStyle(1)
	upper_ratio_lim = nom_hist.GetXaxis().GetXmax()
	lower_ratio_lim = nom_hist.GetXaxis().GetXmin()
	line.SetRange(lower_ratio_lim,0.0,upper_ratio_lim,2.0)	# fix this so it gets the min_x and max_x from input nom_hist
	line.SetMaximum(1.75)
	line.SetMinimum(0.5)
	line.GetYaxis().SetTitle("Nominal/Systematic")
	line.Draw()
	ratio_plot.Draw("E5 same")
	stat_plot.Draw("E5 same")
	line.Draw("same")
	ROOT.gPad.RedrawAxis()
	ratio_pad.Modified()

	c1.Update()
	c1.SaveAs(hist+'_'+dataset_lists_names[idx]+".pdf")
	c1.Clear()
	del nom_hist, nom_graph, line, ratio_plot, tot_stat_errors, stat_plot

