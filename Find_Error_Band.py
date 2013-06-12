import ROOT
import os
import numpy as np
import math

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
#ROOT.gStyle.Reset()	#-> I have style settings in script before this
    
# use plain black on white colors
icol=0 # WHITE
ROOT.gStyle.SetFrameBorderMode(icol)
ROOT.gStyle.SetFrameFillColor(icol)
ROOT.gStyle.SetCanvasBorderMode(icol)
ROOT.gStyle.SetCanvasColor(icol)
ROOT.gStyle.SetPadBorderMode(icol)
ROOT.gStyle.SetPadColor(icol)
ROOT.gStyle.SetStatColor(icol)

# set the paper & margin sizes
ROOT.gStyle.SetPaperSize(20,26)

# set margin sizes
ROOT.gStyle.SetPadTopMargin(0.1)
ROOT.gStyle.SetPadRightMargin(0.025)
ROOT.gStyle.SetPadBottomMargin(0.1)
ROOT.gStyle.SetPadLeftMargin(0.13)

# set title offsets (for axis label)
ROOT.gStyle.SetTitleXOffset(1.3)
ROOT.gStyle.SetTitleYOffset(1.3)
ROOT.gStyle.SetTitleOffset(0.5)

# use large fonts
#font=72 # Helvetica italics
font=42 # Helvetica
tsize=0.04
ROOT.gStyle.SetTextFont(font)

ROOT.gStyle.SetTextSize(tsize)
ROOT.gStyle.SetLabelFont(font,"x")
ROOT.gStyle.SetTitleFont(font,"x")
ROOT.gStyle.SetLabelFont(font,"y")
ROOT.gStyle.SetTitleFont(font,"y")

ROOT.gStyle.SetLabelSize(tsize,"x")
ROOT.gStyle.SetTitleSize(tsize,"x")
ROOT.gStyle.SetLabelSize(tsize,"y")
ROOT.gStyle.SetTitleSize(tsize,"y")
#
## put tick marks on top and RHS of plots
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

ROOT.gStyle.SetOptStat(0)
#-----------------------------------------------------------------------
def MakeLegend(h1,h2):
	leg = ROOT.TLegend(0.55,0.77,0.75,0.87)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.SetTextSize(0.04)
	leg.AddEntry(h1,"Nominal Sherpa","l")
	leg.AddEntry(h2,"Systematic Error","f")
	return leg
	
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

datasets_sig = 	["129916.Nominal_Sherpa_Signal", "147294.min_n_tchannels_CKKW30","147296.min_n_tchannels_MuFdown",
				"147300.min_n_tchannels_mpi1","147302.min_n_tchannels_mpi2","147304.min_n_tchannels_Shower1",
				"147306.min_n_tchannels_MuRdown","147308.min_n_tchannels_MuRup"]
				
datasets_back = ["129916.Nominal_Sherpa_Background", "147310.CKKW30", "147312.MuFdown", "147314.MuFup", 
				"147316.mpi1",	"147318.mpi2", "147320.Shower1", "147322.MuRdown", "147324.MuRup"]

root_file = ROOT.TFile("VBF_Systematics.root")
c1 = ROOT.TCanvas('c1','Theory_Systematics',0,0,640,960)
error_pad = ROOT.TPad('pad1','Error Band',0.,0.34,1.0,1.0)
error_pad.Draw()
ratio_pad = ROOT.TPad('pad2','Error Ratio',0.0,0.0,1.0,0.33)
ratio_pad.Draw()
#c1.SetLogy()

def FindErrorBands(datasets,root_file,hist):
	rebin = 4					# Set this to how many bins should be merged (1 -> no change)
	nom_hist = root_file.Get(datasets[0]+"/Normalized/"+hist+'_norm')
	nom_hist = nom_hist.Clone()
	nom_hist.Rebin(rebin)
	nom_graph = ROOT.TGraphAsymmErrors(nom_hist)
	nom_graph.SetLineColor(ROOT.TAttFill.kGreen)
	nbins = nom_hist.GetNbinsX()

	upper_error = []
	lower_error = []
	sequence = datasets[1:]
	for bin in range(1,nbins+1):
		positive_shifts2 = []
		negative_shifts2 = []
		nom_bin_val = nom_hist.GetBinContent(bin)
		nom_bin_err = nom_hist.GetBinError(bin)
	
		for dataset in sequence:
			hist_to_clone = root_file.Get(dataset+"/Normalized/"+hist+'_norm')
			hist_to_comp = hist_to_clone.Clone(dataset)
			hist_to_comp.Rebin(rebin)
		
			comp_bin_val = hist_to_comp.GetBinContent(bin)
			comp_bin_err = hist_to_comp.GetBinError(bin)
		
			diff = comp_bin_val - nom_bin_val
			if diff > 0.0:
				positive_shifts2.append(diff*diff)
			else:
				negative_shifts2.append(diff*diff)

		upper_error.append(math.sqrt(math.fsum(positive_shifts2)))
		lower_error.append(math.sqrt(math.fsum(negative_shifts2)))
	
		nom_graph.SetPointEYhigh(bin-1,upper_error[bin-1])
		nom_graph.SetPointEYlow(bin-1,lower_error[bin-1])
		
	return nom_hist, nom_graph
	
def MakeRatioPlot(nom_hist,nom_graph):
	npoints = nom_hist.GetNbinsX()
	ratio_plot = ROOT.TGraphAsymmErrors(npoints)
	for point in range(npoints):
		Error_High = nom_graph.GetErrorYhigh(point)
		Error_Low = nom_graph.GetErrorYlow(point)
		Y_point = nom_hist.GetBinContent(point+1)
		X_point = nom_hist.GetBinCenter(point+1)
		X_Axis = nom_hist.GetXaxis()
		ratio_up = Error_High/Y_point
		ratio_down = Error_Low/Y_point
		print X_point, ratio_up, ratio_down
		ratio_plot.SetPoint(point, X_point, 1.0)
		ratio_plot.SetPointEXhigh(point, nom_hist.GetBinWidth(point)/2.0)
		ratio_plot.SetPointEXlow(point, nom_hist.GetBinWidth(point)/2.0)
		ratio_plot.SetPointEYhigh(point, ratio_up)
		ratio_plot.SetPointEYlow(point, ratio_down)
	
	return ratio_plot


hist = 'DijetMass_2jet_1'	# Change this to check another histogram
#-----Find Error Bands for Signal---------------------------------------
error_pad.cd()
nom_hist, nom_graph = FindErrorBands(datasets_sig,root_file,hist)
nom_hist.Draw("hist")
nom_graph.SetFillColor(ROOT.TAttFill.kGreen)
nom_graph.Draw("E5 same")
nom_hist.GetYaxis().SetTitleOffset(1.8)
nom_hist.Draw("hist same")
leg = MakeLegend(nom_hist,nom_graph)
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
# leg = MakeLegend(nom_hist,nom_graph)
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
		