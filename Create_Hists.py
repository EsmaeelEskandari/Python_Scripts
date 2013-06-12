import ROOT
import os

#-------Things to do----------------------------------------------
# 1. 	Make 16 folders (one for each systematic variable)
# 2. 	Fill each folder with plots of the normalized versions of 
#		each systematic variable (min_n_tchannels and with out)
#-----------------------------------------------------------------

dataset_names_1 = ["147294.min_n_tchannels_CKKW30", "147295.min_n_tchannels_CKKW30_MjjFilt",
				"147296.min_n_tchannels_MuFdown", "147297.min_n_tchannels_MuFdown_MjjFilt",
				"147298.min_n_tchannels_MuFup", "147299.min_n_tchannels_MuFup_MjjFilt",
				"147300.min_n_tchannels_mpi1", "147301.min_n_tchannels_mpi1_MjjFilt",
				"147302.min_n_tchannels_mpi2", "147303.min_n_tchannels_mpi2_MjjFilt",
				"147304.min_n_tchannels_Shower1", "147305.min_n_tchannels_Shower1_MjjFilt",
				"147306.min_n_tchannels_MuRdown", "147307.min_n_tchannels_MuRdown_MjjFilt",
				"147308.min_n_tchannels_MuRup", "147309.min_n_tchannels_MuRup_MjjFilt"]
				
dataset_names_2 = ["147310.CKKW30", "147311.CKKW30_MjjFilt", "147312.MuFdown", "147313.MuFdown_MjjFilt",
				"147314.MuFup", "147315.MuFup_MjjFilt", "147316.mpi1", "147317.mpi1_MjjFilt",
				"147318.mpi2", "147319.mpi2_MjjFilt", "147320.Shower1", "147321.Shower1_MjjFilt",
				"147322.MuRdown", "147323.MuRdown_MjjFilt", "147324.MuRup", "147325.MuRup_MjjFilt"]
				
hist_list = ["NJetExcl_1", "NJetExcl_2", "RatioNJetExcl_1", "RatioNJetExcl_2", "FirstJetPt_2jet_1", "FirstJetPt_2jet_2",
			"FirstJetPt_3jet_1", "FirstJetPt_3jet_2", "FirstJetPt_4jet_1", "FirstJetPt_4jet_2", "SecondJetPt_2jet_1", "SecondJetPt_2jet_2",
			"SecondJetPt_3jet_1", "SecondJetPt_3jet_2", "SecondJetPt_4jet_1", "SecondJetPt_4jet_2", "ThirdJetPt_3jet_1", "ThirdJetPt_3jet_2",
			"ThirdJetPt_4jet_1", "ThirdJetPt_4jet_2", "FourthJetPt_4jet_1", "FourthJetPt_4jet_2", "Ht_2jet_1", "Ht_2jet_2",
			"Ht_3jet_1", "Ht_3jet_2", "Ht_4jet_1", "Ht_4jet_2", "Minv_2jet_1", "Minv_2jet_2", "Minv_3jet_1", "Minv_3jet_2",
			"Minv_4jet_1", "Minv_4jet_2", "JetRapidity_1", "JetRapidity_2", "DeltaYElecJet_1", "DeltaYElecJet_2", "SumYElecJet_1", "SumYElecJet_2",
			"DeltaR_2jet_1", "DeltaR_2jet_2", "DeltaY_2jet_1", "DeltaY_2jet_2", "DeltaPhi_2jet_1", "DeltaPhi_2jet_2",
			"DijetMass_2jet_1", "DijetMass_2jet_2", "DijetMass_3jet_1", "DijetMass_3jet_2",
			"DijetMass_4jet_1", "DijetMass_4jet_2","AntiDijetMass_2jet_1", "AntiDijetMass_2jet_2",
			"AntiDijetMass_3jet_1", "AntiDijetMass_3jet_2","AntiDijetMass_4jet_1", "AntiDijetMass_4jet_2",
			"ThirdZep_3jet_1", "ThirdZep_3jet_2", "ThirdZep_4jet_1", "ThirdZep_4jet_2", "FourthZep_4jet_1", "FourthZep_4jet_2",
			"AntiDijetEtaDiff_2jet_1", "AntiDijetEtaDiff_2jet_2", "AntiDijetEtaDiff_3jet_1", "AntiDijetEtaDiff_3jet_2",
			"AntiDijetEtaDiff_4jet_1", "AntiDijetEtaDiff_4jet_2", "AntiDijetPhiDiff_2jet_1", "AntiDijetPhiDiff_2jet_2", 
			"AntiDijetPhiDiff_3jet_1", "AntiDijetPhiDiff_3jet_2", "AntiDijetPhiDiff_4jet_1", "AntiDijetPhiDiff_4jet_2"]

#-----------------------------------------------------------------
# Global style settings go here!
# Most of these are ATLAS defaults
#ROOT.gStyle.Reset()	-> I have style settings in script before this
    
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
ROOT.gStyle.SetPadLeftMargin(0.12)

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
	leg = ROOT.TLegend(0.2,0.77,0.5,0.87)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.SetTextSize(0.04)
	#leg.AddEntry(h1,"min_n_tchannels (signal)","f")
	#leg.AddEntry(h2,"W+jets","f")
	leg.AddEntry(h1,"min_n_tchannels (signal)","l")
	leg.AddEntry(h2,"W+jets","l")
	return leg
	
def SetHistStyle(h1,h2,max_1,max_2,min_1,min_2):
	#h1.SetFillColor(ROOT.TAttFill.kYellow)
	#h1.SetLineColor(ROOT.TAttLine.kBlack)
	h1.SetLineColor(ROOT.TAttLine.kBlue)
	h1.SetLineWidth(3)
	h1.GetYaxis().SetTitleOffset(1.5)
	#h2.SetFillColor(ROOT.TAttFill.kGreen-8)
	#h2.SetLineColor(ROOT.TAttLine.kBlack)
	h2.SetLineColor(ROOT.TAttLine.kRed)
	h2.SetLineWidth(3)
	h2.GetYaxis().SetTitleOffset(1.5)
	if max_1 > max_2 and max_1 != 0:
		h1.SetMaximum(10*max_1)
		if min_1 < min_2:
			h1.SetMinimum(min_1/5)
		else:
			h1.SetMinimum(min_2/5)
	elif max_2 > max_1 and max_2 != 0:
		h2.SetMaximum(10*max_2)
		if min_1 < min_2:
			h2.SetMinimum(min_1/5)
		else:
			h2.SetMinimum(min_2/5)
	return h1, h2
	
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
			histogram1 = root_file.Get(dataset_names_1[index]+'/Normalized/'+hist+'_norm')
			histo1 = histogram1.Clone(hist+'_1')
			histogram2 = root_file.Get(dataset_names_2[index]+'/Normalized/'+hist+'_norm')
			histo2 = histogram2.Clone(hist+'_2')
			max_1 = histo1.GetMaximum()
			max_2 = histo2.GetMaximum()
			min_1 = histo1.GetMinimum(0)
			min_2 = histo2.GetMinimum(0)
			SetHistStyle(histo1,histo2,max_1,max_2,min_1,min_2)
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
			else:			#If k is odd (Jet pT > 25*GeV)
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
		
		
