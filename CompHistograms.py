#!/usr/local/bin/python

import ROOT, os, sys
import array
from optparse import OptionParser

help_text = """./HistogramRatio.py <-i|-n|-l> [root file (default=histos.root)]"""
parser = OptionParser(usage=help_text)
parser.add_option("-n", "--normXS", action="store_true", dest="normalizeXS", default=False, help="Plot histograms that are normalized by their respective cross-section.")
parser.add_option("-i", "--integrate", action="store_true", dest="integrate", default=False, help="Plot histograms that are normalized by their respective integrals.")
parser.add_option("-r", "--rebin", type="int", dest="new_rebin", metavar="REBIN", default=None, help="Rebin override: forces scirpt to rebin using given number.")
parser.add_option("-l", "--lin-y", action="store_true", dest="linear", default=False, help="Sets the y-axis to linear scale (Defaults to log.).")
parser.add_option("-d", "--no-ratio", action="store_false", dest="ratPlot", default=True, help="Print the ratio plot. (default=True)" )
(options, args) = parser.parse_args()
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2(True)

def DivideBinWidth(h1):
    for bin in range(h1.GetNbinsX()+2):
        bin_width = h1.GetBinWidth(bin)
        bin_cont = h1.GetBinContent(bin)/bin_width
        bin_err = h1.GetBinError(bin)/bin_width
        h1.SetBinContent(bin,bin_cont)
        h1.SetBinError(bin,bin_err)
    return h1

def query_yes_no(question, default="yes"):
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def Large_label_title_top(histo1):
    histo1.GetXaxis().SetLabelSize(33)
    histo1.GetXaxis().SetTitleSize(0.065)
    histo1.GetYaxis().SetTitleSize(0.065)
    histo1.GetXaxis().SetTickLength(0.04)
    histo1.GetYaxis().SetTickLength(0.04)
    histo1.GetXaxis().SetLabelSize(0.065)
    histo1.GetYaxis().SetLabelSize(0.065)
    histo1.GetYaxis().SetNdivisions(507)
    histo1.GetYaxis().SetTitleOffset(0.55*1.37)
    histo1.SetLineWidth(2)
    
def Large_label_title_bot(histo1):
    histo1.GetXaxis().SetLabelSize(33)
    histo1.GetXaxis().SetTitleSize(0.12)
    histo1.GetYaxis().SetTitleSize(0.08)
    histo1.GetXaxis().SetTickLength(0.05)
    histo1.GetYaxis().SetTickLength(0.05)
    histo1.GetXaxis().SetLabelSize(0.065)
    histo1.GetYaxis().SetLabelSize(0.065)
    histo1.GetYaxis().SetTitleOffset(0.45)
    histo1.GetYaxis().SetNdivisions(507)
    histo1.SetLineWidth(2)

def PlotCurves(histograms,NORMED_XS,NORMED_INT,file_name,axisLabels=None,legents=None):
    SETLOGY= not options.linear
    SETXRANGE=0
    SETYRANGE=0
    SETYRATRANGE=1
    SETNDIV=0
    CENTERLAB=0
    RX1=20.0
    RX2=260.0
    RY1=0.0
    RY2=0.0
    RATRY1=0.25
    RATRY2=2.0-RATRY1
    INTEGRATE=False
    max_val = 0.0
    # Number of files to be opened
    FILES=len(fnames1)
    # Number of curves to be plotted
    REPNFIL=len(histograms)
    if REPNFIL == 0: REPNFIL = 1
    
    fpoint1 = []
    fpoint1.append(file_name)
        
    hvect1 = []
    LineStyle = [1, 1, 1, 1, 2, 3, 3]
    LineColor = ["ROOT.TAttLine.kBlack" , "ROOT.TAttLine.kRed+1", "ROOT.TAttLine.kBlue",
                 "ROOT.TAttLine.kGreen+3", "ROOT.TAttLine.kOrange+7", "ROOT.TAttLine.kYellow-6",
                 "ROOT.TAttLine.kBlue-6"]
    LineWidth = [1 , 2, 2, 2, 2, 2, 2]
    MarkerStyle = [0 , 0, 0, 0, 0, 0, 0]
    MarkerSize = [0 , 0, 0, 0, 0, 0, 0]
    if (REPNFIL > len(LineColor)): 
        use_default = query_yes_no("Would you like to use default values for line Style/Color/Width and marker style/size.")
        if use_default:
            for k in range(REPNFIL-len(LineColor)):
                LineStyle.append(LineStyle[0])
                LineColor.append(LineColor[0])
                LineWidth.append(LineWidth[0])
                MarkerStyle.append(MarkerStyle[0])
                MarkerSize.append(MarkerSize[0])
        else:
            print "Define more line attributes, too many curves...check lines 63-67"
    
    if options.new_rebin == -1:
        rebin = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000,1250,1500,1750,2000,2250,2500,2750,3000,3500,5000])
    elif options.new_rebin is not None:
        rebin = options.new_rebin
    else: rebin = 1
    
    for i in range(REPNFIL):
        hist_to_get = histograms[i]
        hvect1.append(fpoint1[0].Get(hist_to_get))
        if NORMED_INT:
            hvect1[i].Scale(1.0/hvect1[i].Integral("width"))
            hvect1[i].GetYaxis().SetTitle("Norm to One")
        num_xbins = hvect1[i].GetNbinsX()
        if options.new_rebin == -1:
            new_hist = hvect1[i].Rebin(len(rebin)-1,"DijetMass_rebin",rebin)
            hvect1[i] = DivideBinWidth(new_hist)
        #elif (num_xbins > 52) and (num_xbins <= 102): hvect1[i].Rebin(10)
        #elif (num_xbins > 102): hvect1[i].Rebin(rebin)
        else: hvect1[i].Rebin(rebin)
        
        # if (num_xbins > 52) and (num_xbins <= 102): hvect1[i].Rebin(2)
        # elif (num_xbins > 102): hvect1[i].Rebin(rebin)
        #hvect1[i].Rebin(rebin)
        
        max_val_tmp=hvect1[i].GetMaximum()
        if (max_val < max_val_tmp): max_val = max_val_tmp
        hvect1[i].SetLineStyle(LineStyle[i])
        hvect1[i].SetLineColor(eval(LineColor[i]))
        hvect1[i].SetLineWidth(LineWidth[i])
        hvect1[i].SetMarkerStyle(MarkerStyle[i])
        hvect1[i].SetMarkerSize(MarkerSize[i])
        hvect1[i].SetMarkerColor(eval(LineColor[i]))
    print hvect1

    #---------------------------------------------------------------------------------------
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
    
    # Initialize canvas and draw pads
    c0 = ROOT.TCanvas("c0","",50,50,865,780)
    c0.cd()

    if not options.ratPlot:
        pad1 = ROOT.TPad("pad1","top pad",0,0,1,1)
        pad1.SetFillStyle(0)
        pad1.SetFrameFillStyle(0)
        pad1.Draw()
    else:
        pad1 = ROOT.TPad("pad1","top pad",0,0.40,1,1)
        pad2 = ROOT.TPad("pad2","bottom pad",0,0,1,0.40)
        pad1.SetFillStyle(0)
        pad1.SetFrameFillStyle(0)
        pad2.SetFillStyle(0)
        pad2.SetFrameFillStyle(0)
        pad1.Draw()
        pad2.Draw()

    #---------------------------------------------------------------------------------------
    if options.ratPlot:
        pad1.SetBottomMargin(0.0)
    if SETLOGY: pad1.SetLogy()
    pad1.cd()

    if (SETXRANGE == 1): hvect1[0].SetAxisRange(RX1,RX2,"x")
    if (SETYRANGE == 1): hvect1[0].SetAxisRange(RY1,RY2,"y")
    if options.ratPlot: Large_label_title_top(hvect1[0])
    if axisLabels:
        hvect1[0].GetXaxis().SetTitle(axisLabels[0])
        hvect1[0].GetYaxis().SetTitle(axisLabels[1])
    else:
        hvect1[0].GetYaxis().SetTitle(hvect1[0].GetYaxis().GetTitle())
    if (SETNDIV==1): hvect1[0].GetXaxis().SetNdivisions()
    if (CENTERLAB==1): hvect1[0].GetXaxis().CenterLabels()

    if SETLOGY: hvect1[0].SetMaximum(2.0*max_val)
    else: hvect1[0].SetMaximum(1.1*max_val)
    hvect1[0].Draw("COLZ")
    for i in range(REPNFIL):
        hvect1[i].SetBit(ROOT.TH1.kNoTitle)
        if hvect1[i].GetDimension() == 2:
            hvect1[i].Draw("same")
            hvect1[i].Draw("same colz")
        else:
            hvect1[i].Draw("same")
            hvect1[i].Draw("same p")

    # margins :
    lx1,lx2=0.60,0.90 
    ly1,ly2=0.5-0.05*REPNFIL,0.49
    ptitx1,ptitx2=0.01,lx1+0.1
    ptity1,ptity2=0.91,0.996

    # legend
    leg = ROOT.TLegend(lx1,ly1,lx2,ly2)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetShadowColor(0)
    leg.SetBorderSize(0)
    if legents==None: legents = histograms.split("/")[1]
    for i in range(REPNFIL):
        leg.AddEntry(hvect1[i],legents[i],"pl")
    leg.Draw()
    
    # ATLAS Internal
    if options.ratPlot:
        lx, ly = 0.2, 0.1	# Only adjust these, the others are defined relative to these
        px, py = lx+0.08, ly
    else:
        lx, ly = 0.1, 0.2	# Only adjust these, the others are defined relative to these
        px, py = lx+0.1, ly
    #l.DrawLatex(lx,ly,"ATLAS")
    #p.DrawLatex(px,py,"Internal")

    # histo title
    ptit = ROOT.TPaveText(ptitx1,ptity1,ptitx2,ptity2,"NDC")
    ptit.SetBorderSize(0)
    ptit.SetFillColor(0)
    ptit.SetTextFont(62)
    ptit.SetMargin(0.01)
    ptit.AddText(hvect1[0].GetTitle())
    ptit.Draw("same")

    #---------------------------------------------------------------------------------------
    if options.ratPlot:
        pad2.SetTopMargin(0.0)
        pad2.SetBottomMargin(0.12/0.46)
        pad2.cd()

        hist_clones = []
        hist_clones.append(hvect1[0].Clone())
        for i in range(1,REPNFIL):
            hist_clones.append(hvect1[i].Clone())
            hist_clones[i].Divide(hist_clones[0])
        hist_clones[0].Divide(hist_clones[0])

        if (SETYRATRANGE == 1): hist_clones[0].SetAxisRange(RATRY1,RATRY2,"y")
        hist_clones[0].GetYaxis().SetTitle("#frac{Variation}{Nominal}")
        hist_clones[0].SetFillStyle(3004)
        hist_clones[0].SetFillColor(eval(LineColor[0]))
        Large_label_title_bot(hist_clones[0])
        hist_clones[0].Draw("E2")

        for i in range(REPNFIL):
            hist_clones[i].Draw("same")
            hist_clones[i].Draw("same p")

    #---------------------------------------------------------------------------------------
    hist_base = histograms[0].split("/")[-1]
    hist_pre = histograms[0].split("/")[0]
    #hist_base = "Mjj"
    if not NORMED_XS and not NORMED_INT:
        c0.SaveAs(hist_pre+hist_base+"_dist.pdf")
    elif NORMED_XS and not NORMED_INT: 
        hist_base = hist_base.split("/")[1]
        c0.SaveAs(hist_pre+hist_base+"_norm.pdf")
    elif not NORMED_XS and NORMED_INT:
        c0.SaveAs(hist_pre+hist_base+"_int.pdf")
    else:
        print "You are trying to normalize histograms by both the"
        print "cross-section and integral. Don't do this yet..."
    
    c0.Destructor()
    return
    
#-----------Presets----------------------------------------------------------------------
presets = {
    'rPT':["hResolution_pT_All","hResolution_pT_newpos_All","hResolution_pT_energy_All"],
    'rE':["hResolution_E_All","hResolution_E_newpos_All","hResolution_E_energy_All"],
    'rETA':["hResolution_Eta_All","hResolution_Eta_newpos_All","hResolution_Eta_energy_All"],
    'rPHI':["hResolution_Phi_All","hResolution_Phi_newpos_All","hResolution_Phi_energy_All"],
    'rMJJ':["hResolution_Mjj_All","hResolution_Mjj_newpos_All","hResolution_Mjj_energy_All"],
    'rDR':["hResolution_DR_All","hResolution_DR_newpos_All","hResolution_DR_energy_All"],
    'cpPT1':["hControlPlot_OffJet1_pT_All","hControlPlot_Jet1_pT_All","hControlPlot_Jet1_pT_newpos_All","hControlPlot_Jet1_pT_energy_All"],
    'cpE1':["hControlPlot_OffJet1_E_All","hControlPlot_Jet1_E_All","hControlPlot_Jet1_E_newpos_All","hControlPlot_Jet1_E_energy_All"],
    'cpETA1':["hControlPlot_OffJet1_Eta_All","hControlPlot_Jet1_Eta_All","hControlPlot_Jet1_Eta_newpos_All","hControlPlot_Jet1_Eta_energy_All"],
    'cpPHI1':["hControlPlot_OffJet1_Phi_All","hControlPlot_Jet1_Phi_All","hControlPlot_Jet1_Phi_newpos_All","hControlPlot_Jet1_Phi_energy_All"],
    'cpPT2':["hControlPlot_OffJet2_pT_All","hControlPlot_Jet2_pT_All","hControlPlot_Jet2_pT_newpos_All","hControlPlot_Jet2_pT_energy_All"],
    'cpE2':["hControlPlot_OffJet2_E_All","hControlPlot_Jet2_E_All","hControlPlot_Jet2_E_newpos_All","hControlPlot_Jet2_E_energy_All"],
    'cpETA2':["hControlPlot_OffJet2_Eta_All","hControlPlot_Jet2_Eta_All","hControlPlot_Jet2_Eta_newpos_All","hControlPlot_Jet2_Eta_energy_All"],
    'cpPHI2':["hControlPlot_OffJet2_Phi_All","hControlPlot_Jet2_Phi_All","hControlPlot_Jet2_Phi_newpos_All","hControlPlot_Jet2_Phi_energy_All"],
    'cpDR':["hControlPlot_Off_DeltaR_All","hControlPlot_DeltaR_All","hControlPlot_DeltaR_newpos_All","hControlPlot_DeltaR_energy_All"],
    'cpGTOWS1':["hControlPlot_Jet1_numGTowers_All","hControlPlot_Jet1_numGTowers_newpos_All","hControlPlot_Jet1_numGTowers_energy_All"],
    'cpGTOWS2':["hControlPlot_Jet2_numGTowers_All","hControlPlot_Jet2_numGTowers_newpos_All","hControlPlot_Jet2_numGTowers_energy_All"],
    'cpNJETS':["hControlPlot_gJetNJet_All","hControlPlot_oJetNJet_All","hControlPlot_truJetNJet_All"],
    'oMJJ':["hDijetMass_All","hDijetMassTruth_All","hDijetMassReg_All","hDijetMassNewPos_All","hDijetMassEnergy_All"],
    'oDMJJoff':["hDijetMass_DOffReg_All","hDijetMass_DOffNewpos_All","hDijetMass_DOffEnergy_All","hDijetMass_DOffTruth_All"],
    'oDMJJtru':["hDijetMass_DTruReg_All","hDijetMass_DTruNewpos_All","hDijetMass_DTruEnergy_All","hDijetMass_DTruOff_All"]
}

presetsAxisLabels = {
    'rPT':["#frac{P_{T}-P_{T,ref}}{P_{T,ref}}","#frac{dN}{dP_{T}}"],
    'rE':["#frac{E-E_{ref}}{E_{ref}}","#frac{dN}{dE} [GeV^{-1}]"],
    'rETA':["#eta-#eta_{ref}","#frac{dN}{d#eta}"],
    'rPHI':["#phi-#phi_{ref}","#frac{dN}{d#phi}"],
    'rMJJ':["#frac{M_{jj}-M_{jj,ref}}{M_{jj,ref}}","#frac{dN}{dM_{jj}}"],
    'rDR':["#frac{#DeltaR-#DeltaR_{ref}}{#DeltaR_{ref}}","#frac{dN}{d#DeltaR}"],
    'cpPT1':["P_{T} [GeV]","#frac{dN}{dP_{T}} [GeV^{-1}]"],
    'cpE1':["Energy [GeV]","#frac{dN}{dE} [GeV^{-1}]"],
    'cpETA1':["#eta [GeV]","#frac{dN}{d#eta}"],
    'cpPHI1':["#phi [GeV]","#frac{dN}{d#phi}"],
    'cpPT2':["P_{T} [GeV]","#frac{dN}{dP_{T}} [GeV^{-1}]"],
    'cpE2':["Energy [GeV]","#frac{dN}{dE} [GeV^{-1}]"],
    'cpETA2':["#eta [GeV]","#frac{dN}{d#eta}"],
    'cpPHI2':["#phi [GeV]","#frac{dN}{d#phi}"],
    'cpDR':["#DeltaR_{j1,j2}","#frac{dN}{d#DeltaR} [GeV^{-1}]"],
    'cpGTOWS1':["#N_{gTow}","#frac{dN}{d#N_{gTow}}"],
    'cpGTOWS2':["#N_{gTow}","#frac{dN}{d#N_{gTow}}"],
    'cpNJETS':["#N_{jets}","#frac{dN}{d#N_{jets}}"],
    'oMJJ':["M_{jj} [GeV]","#frac{dN}{dM_{jj}} [GeV^{-1}]"],
    'oDMJJoff':["#DeltaM_{jj} [GeV]","#frac{dN}{d#DeltaM_{jj}} [GeV^{-1}]"],
    'oDMJJtru':["#DeltaM_{jj} [GeV]","#frac{dN}{d#DeltaM_{jj}} [GeV^{-1}]"]
}

#-----------Define things here-----------------------------------------------------------
# Histogram base name
NORMED_XS = options.normalizeXS
NORMED_INT = options.integrate

if (NORMED_XS): 
    for j,base_name in enumerate(histograms):
        histograms[j] = "Normalized_XS/"+base_name+"_norm"

# open files, set normalization, retrieve+scale && rebin histos
if len(args) == 1:
    fnames1 = args[0]
    print args
    File_Exists = os.path.isfile(fnames1)
    if not File_Exists: 
        print "{0} does not exist!".format(fnames1)
else:
    fnames1 = "histos.root"
    File_Exists = os.path.isfile(fnames1)
    if not File_Exists: 
        print "histos.root does not exist!"
        print "Define a histogram root file in command line arguments. (see --help)"
        
file_name = ROOT.TFile(fnames1)

possibles = [(i,k) for i,k in enumerate(file_name.GetListOfKeys())]
dictPossibles = dict(possibles)
for key,value in dictPossibles.iteritems():
    print "{0}\t\t{1}".format(key,value.GetName())
    if value.IsFolder() and (key%len(possibles) == 1):
        file_name.cd(value.GetName())
        file_name.ls()
        file_name.cd()
# for key,value in presets.iteritems():
#     print "{0}\t\t{1}".format(key,value)

print "Enter histograms to plotted on same canvas (separated by commas),"
print "Choose from histogram presets (can be a comma separate list of presets),"
print """Or type "all" to plot all histograms in root file separately."""
histString = raw_input("Histograms: ")
histString = histString.replace(" ","")
histKeys = histString.split(",")
legendInput = raw_input("Lengend Entries: ")
legendInput = legendInput.replace(" ","")
legents = legendInput.split(",")

if histString == "all":
    for histo in possibles:
        PlotCurves([histo],NORMED_XS,NORMED_INT,file_name)
elif sorted(histKeys) == sorted(list(set(histKeys) & set(presets.keys()))):
    for key in histKeys:
        histograms = presets[key]
        labels = presetsAxisLabels[key]
        PlotCurves(histograms,NORMED_XS,NORMED_INT,file_name,axisLabels=labels)
else:
    histograms = histString.split(",")
    PlotCurves(histograms,NORMED_XS,NORMED_INT,file_name,legents=legents)

ROOT.gROOT.ProcessLine(".q")
