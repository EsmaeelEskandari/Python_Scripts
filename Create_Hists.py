import ROOT
import os
from Aux_Functions import *

#-------Things to do----------------------------------------------
# 1. 	Make 16 folders (one for each systematic variable)
# 2. 	Fill each folder with plots of the normalized versions of 
#		each systematic variable (min_n_tchannels and with out)
#-----------------------------------------------------------------

dataset_names_1 = GetListDataset('dataset_names_1')
dataset_names_2 = GetListDataset('dataset_names_2')
hist_list = GetListDataset('hist_list')

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
c1 = ROOT.TCanvas('c1','VBF_Systematics',0,0,640,640)
c1.SetLogy()

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

lx, ly = 0.63, 0.75	# Only adjust these, the others are defined relative to these
px, py = lx+0.16, ly
qx, qy = lx, ly+0.05

#---------------------------------------------------------------------
dir = 'Plot_Comparisons'
if not os.path.exists(dir):
	os.makedirs(dir)

#root_file.mkdir(dir)
for index in range(16):
    x = root_file.GetDirectory(dataset_names_1[index])
    y = root_file.GetDirectory(dataset_names_2[index])
    print x
    print y
    if x and y:
	#root_file.cd(dir)
	#ROOT.gDirectory.mkdir(dataset_names_2[index])
	#ROOT.gDirectory.cd()
	for k, hist in enumerate(hist_list):
	    histogram1 = root_file.Get(dataset_names_1[index]+'/Normalized_XS/'+hist+'_norm')
	    histo1 = histogram1.Clone(hist+'_1')
	    histogram2 = root_file.Get(dataset_names_2[index]+'/Normalized_XS/'+hist+'_norm')
	    histo2 = histogram2.Clone(hist+'_2')
	    max_1 = histo1.GetMaximum()
	    max_2 = histo2.GetMaximum()
	    min_1 = histo1.GetMinimum(0)
	    min_2 = histo2.GetMinimum(0)
	    histo1, histo2 = SetHistStyle(histo1,histo2,max_1,max_2,min_1,min_2)
	    if max_1 > max_2:
		histo1.Draw("HIST E")
		histo2.Draw("HIST E SAME")
	    else:
		histo2.Draw("HIST E")
		histo1.Draw("HIST E SAME")
	    ROOT.gPad.RedrawAxis()
	    l.DrawLatex(lx,ly,"ATLAS")
	    p.DrawLatex(px,py,"Internal")
	    if (k%2 == 0):	#If k is even (Jet pT > 30*GeV)
		q.DrawLatex(qx,qy,"Jet p_{T,thresh} > 30 [GeV]")
	    else:		#If k is odd (Jet pT > 25*GeV) ----- No longer true!
		q.DrawLatex(qx,qy,"Jet p_{T,thresh} > 25 [GeV]")
	    leg = MakeLegend(histo1,histo2)
	    leg.Draw()
	    c1.Modified()
	    c1.Update()
	    if not os.path.exists(dir+'/'+dataset_names_2[index]):
		os.makedirs(dir+'/'+dataset_names_2[index])
	    c1.SaveAs(dir+'/'+dataset_names_2[index]+'/'+hist+'.pdf')
	    #root_file.cd(dir)
	    #ROOT.gDirectory.cd(dataset_names_2[index])
	    #c1.Write(hist,ROOT.TObject.kOverwrite)
	    c1.Clear
	    #ROOT.gDirectory.cd()
	    #ROOT.gDirectory.cd()
    else:
	    continue
	      