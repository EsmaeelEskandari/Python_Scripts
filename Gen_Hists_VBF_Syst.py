import ROOT,sys

root_file = ROOT.TFile.Open("VBF_Systematics.root")
ROOT.gStyle.SetOptStat(0)

c1 = ROOT.TCanvas('c1','Stats Comparison',50,50,865,780)
leg = ROOT.TLegend(0.2,0.2,0.3,0.4)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)

colors = ["ROOT.TAttFill.kBlack","ROOT.TAttFill.kRed","ROOT.TAttFill.kGreen+1","ROOT.TAttFill.kBlue",
          "ROOT.TAttFill.kMagenta+2","ROOT.TAttFill.kOrange+8","ROOT.TAttFill.kSpring+3"]
datasets_to_get = ["129916.Nominal_Sherpa_Signal", "000015.Powheg.VBF.Nominal.ptj_gencut"]
histograms_to_get = ["DijetMass_2jet_1", "DijetMass_CR_1"]
print "Reference histogram is datasets_to_get[0]: {0}".format(datasets_to_get[0])
if len(datasets_to_get) > len(colors): 
    print "You need to define more colors!! (in colors list)"
    sys.exit()

NORMALIZE = True    # Boolean: Decides whether to normalize to integral or not.
FORCE_REBIN = False # Boolean: Decides whether to force rebinning to specified number.
rebin = 1

for hist_to_get in histograms_to_get:
    c1.cd()
    pad1 = ROOT.TPad("pad1","top pad",0,0.40,1,1)
    pad2 = ROOT.TPad("pad2","bottom pad",0,0,1,0.40)
    pad1.SetFillStyle(0)
    pad1.SetFrameFillStyle(0)
    pad2.SetFillStyle(0)
    pad2.SetFrameFillStyle(0)
    pad1.Draw()
    pad2.Draw()
    
    histos = []
    for idx,dataset in enumerate(datasets_to_get):
        histo1 = root_file.Get(dataset+"/"+hist_to_get)
        num_of_bins = histo1.GetNbinsX()
        if not FORCE_REBIN:
            if num_of_bins >= 200: rebin = 5
        
        histo1.Rebin(rebin)
        histo1.SetLineColor(eval(colors[idx]))
        if NORMALIZE:
            histo1.Scale(1.0/histo1.Integral("width"))
        
        leg.AddEntry(histo1,dataset,"l")
        histos.append(histo1)

#------------Histograms-------------------------
    pad1.cd()
    pad1.SetLogy()
    for idx in range(len(datasets_to_get)):
        histos[idx].Draw("HIST E SAME")
    leg.Draw()

#------------Ratio Plot-------------------------
    pad2.cd()
    histo_err = histos[0].Clone()
    histo_ref = histos[0].Clone()
    histo_err.Divide(histo_err)
    histo_err.SetFillStyle(3004)
    histo_err.SetFillColor(ROOT.TAttLine.kBlack)
    histo_err.Draw("E2")
    for idx in range(1,len(datasets_to_get)):
        histo_rat = histos[idx].Clone()
        histo_rat.Divide(histo_ref)
        histo_rat.Draw("SAME")

    c1.SaveAs(hist_to_get+".pdf")
    leg.Clear()
    c1.Clear()