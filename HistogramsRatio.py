import ROOT, os, sys
from optparse import OptionParser

help_text = """python HistogramRatio.py <-i|-n> [root file (default=VBF_Systematics_JLC.root)]"""
parser = OptionParser(usage=help_text)
parser.add_option("-n", "--normXS", action="store_true", dest="normalizeXS", default=False, help="Plot histograms that are normalized by their respective cross-section.")
parser.add_option("-i", "--integrate", action="store_true", dest="integrate", default=False, help="Plot histograms that are normalized by their respective integrals.")
parser.add_option("-r", "--rebin", type="int", dest="new_rebin", metavar="REBIN", default=None, help="Rebin override: forces scirpt to rebin using given number.")
(options, args) = parser.parse_args()
ROOT.gStyle.SetOptStat(0)

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

def PlotCurves(hist_base,NORMED_XS,NORMED_INT,fnames1,legents,histpaths):
    SETLOGY=True
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
    RATRY2=2.2
    INTEGRATE=False
    max_val = 0.0
    # Number of files to be opened
    FILES=len(fnames1)
    # Number of curves to be plotted
    REPNFIL=len(histpaths)
    
    fpoint1 = []
    for i in range(FILES):
        file_name = ROOT.TFile(fnames1[i])
        fpoint1.append(file_name)
        if not fpoint1[i].IsOpen():
            print "no file found for: "+fnames1[i]+"\n"
            ROOT.gROOT.ProcessLine(".q")
        
    hvect1 = []
    LineStyle = [1 , 1, 1, 2, 2, 3, 3]
    LineColor = ["ROOT.TAttLine.kBlack" , "ROOT.TAttLine.kRed+1", "ROOT.TAttLine.kBlue",
                 "ROOT.TAttLine.kGreen+3", "ROOT.TAttLine.kOrange+7", "ROOT.TAttLine.kYellow-6",
                 "ROOT.TAttLine.kBlue-6"]
    LineWidth = [2 , 2, 2, 2, 2, 2, 2]
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
    
    if options.new_rebin is not None:
        rebin = options.new_rebin
    else: rebin = 5
    for i in range(REPNFIL):
        hist_to_get = histpaths[i] + hist_base
        hvect1.append(fpoint1[0].Get(hist_to_get))
        if NORMED_INT:
            hvect1[i].Scale(1.0/hvect1[i].Integral("width"))
            hvect1[i].GetYaxis().SetTitle("Norm to One")
        num_xbins = hvect1[i].GetNbinsX()
        if (num_xbins > 52) and (num_xbins <= 102): hvect1[i].Rebin(2)
        elif (num_xbins > 102): hvect1[i].Rebin(rebin)
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

    pad1 = ROOT.TPad("pad1","top pad",0,0.40,1,1)
    pad2 = ROOT.TPad("pad2","bottom pad",0,0,1,0.40)

    pad1.SetFillStyle(0)
    pad1.SetFrameFillStyle(0)
    pad2.SetFillStyle(0)
    pad2.SetFrameFillStyle(0)

    pad1.Draw()
    pad2.Draw()

    #---------------------------------------------------------------------------------------
    pad1.SetBottomMargin(0.0)
    if SETLOGY: pad1.SetLogy()
    pad1.cd()

    if (SETXRANGE == 1): hvect1[0].SetAxisRange(RX1,RX2,"x")
    if (SETYRANGE == 1): hvect1[0].SetAxisRange(RY1,RY2,"y")
    Large_label_title_top(hvect1[0])
    hvect1[0].GetYaxis().SetTitle(hvect1[0].GetYaxis().GetTitle())
    if (SETNDIV==1): hvect1[0].GetXaxis().SetNdivisions()
    if (CENTERLAB==1): hvect1[0].GetXaxis().CenterLabels()

    hvect1[0].SetMaximum(2.0*max_val)
    hvect1[0].Draw()
    for i in range(REPNFIL):
        hvect1[i].SetBit(ROOT.TH1.kNoTitle)
        hvect1[i].Draw("same")
        hvect1[i].Draw("samep")

    # margins :
    lx1,lx2=0.60,0.90 
    ly1,ly2=0.9-0.05*REPNFIL,0.89
    ptitx1,ptitx2=0.01,lx1+0.1
    ptity1,ptity2=0.91,0.996

    # legend
    leg = ROOT.TLegend(lx1,ly1,lx2,ly2)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetShadowColor(0)
    leg.SetBorderSize(0)
    for i in range(REPNFIL):
        leg.AddEntry(hvect1[i],legents[i],"pl")
    leg.Draw()
    
    # ATLAS Internal
    lx, ly = 0.2, 0.1	# Only adjust these, the others are defined relative to these
    px, py = lx+0.08, ly
    l.DrawLatex(lx,ly,"ATLAS")
    p.DrawLatex(px,py,"Internal")

    # histo title
    ptit = ROOT.TPaveText(ptitx1,ptity1,ptitx2,ptity2,"NDC")
    ptit.SetBorderSize(0)
    ptit.SetFillColor(0)
    ptit.SetTextFont(62)
    ptit.SetMargin(0.01)
    ptit.AddText(hvect1[0].GetTitle())
    ptit.Draw("same")

    #---------------------------------------------------------------------------------------
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
        hist_clones[i].Draw("samep")

    #---------------------------------------------------------------------------------------
    if not NORMED_XS and not NORMED_INT:
        c0.SaveAs("Distribution_"+hist_base+".pdf")
    elif NORMED_XS and not NORMED_INT: 
        hist_base = hist_base.split("/")[1]
        c0.SaveAs("Normalized_"+hist_base+".pdf")
    elif not NORMED_XS and NORMED_INT:
        c0.SaveAs("Integrated_"+hist_base+".pdf")
    else:
        print "You are trying to normalize histograms by both the"
        print "cross-section and integral. Don't do this yet..."
    
    c0.Destructor()
    return

#-----------Define things here-----------------------------------------------------------
# Histogram base name
NORMED_XS = options.normalizeXS
NORMED_INT = options.integrate
histograms = ["DijetMass_2jet_1"]
if (NORMED_XS): 
    for j,base_name in enumerate(histograms):
        histograms[j] = "Normalized_XS/"+base_name+"_norm"

# open files, set normalization, retrieve+scale && rebin histos
if len(args) > 0:
    fnames1 = args[0:1]
    File_Exists = os.path.isfile(fnames1[0])
    if not File_Exists: 
        print "{0} does not exist!".format(fnames1[0])
else:
    fnames1 = ["VBF_Systematics_JLC.root"]
    File_Exists = os.path.isfile(fnames1[0])
    if not File_Exists: 
        print "VBF_Systematics_JLC.root does not exist!"
        print "Define a histogram root file in command line arguments. (see --help)"
    
#legents = ["Nominal", "MuFdown", "MuFup", "MuRdown", "MuRup", "MuR/Fdown", "MuR/Fup"]
#legents = ["Nominal", "CKKW(20->30)", "MPI_1", "MPI_2", "Shower_1"]

# Be sure directory names end in /
#histpaths = ["129930.Nominal_Sherpa_Background_MjjFilt/", "147313.MuFdown_MjjFilt/", "147315.MuFup_MjjFilt/", "147323.MuRdown_MjjFilt/", "147325.MuRup_MjjFilt/"]
#histpaths = ["129930.Nominal_Sherpa_Background_MjjFilt/","147311.CKKW30_MjjFilt/","147317.mpi1_MjjFilt/","147319.mpi2_MjjFilt/","147321.Shower1_MjjFilt/"]
#histpaths = ["000001.Powheg.W2jets.Nominal.bornsuppfact/","000002.Powheg.W2jets.MuFdown.bornsuppfact/","000003.Powheg.W2jets.MuFup.bornsuppfact/","000004.Powheg.W2jets.MuRdown.bornsuppfact/","000005.Powheg.W2jets.MuRup.bornsuppfact/","000006.Powheg.W2jets.MuRdownMuFdown.bornsuppfact/","000007.Powheg.W2jets.MuRupMuFup.bornsuppfact/"]

for hist_base in histograms:
    PlotCurves(hist_base,NORMED_XS,NORMED_INT,fnames1,legents,histpaths)

ROOT.gROOT.ProcessLine(".q")
