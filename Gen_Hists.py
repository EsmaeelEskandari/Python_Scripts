import ROOT

root_file_1 = ROOT.TFile.Open("129930.root")
root_file_2 = ROOT.TFile.Open("129929.root")
root_file_3 = ROOT.TFile.Open("Powheg_w2jet.root")
root_file_4 = ROOT.TFile.Open("200900.root")
ROOT.gStyle.SetOptStat(0)

c1 = ROOT.TCanvas('c1','Stats Comparison',50,50,865,780)
leg = ROOT.TLegend(0.2,0.2,0.3,0.4)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)

histograms_to_get = ["DijetMass_nocuts", "DijetMass_2jet_1", "BosonPt_nocuts", "FirstJetPt_nocuts",
                     "SecondJetPt_nocuts", "DeltaPhi_2jet_1", "DeltaY_2jet_1", "DeltaR_2jet_1",
                     "DijetMass_CR_1", "Ht_2jet_1", "ThirdZep_3jet_1", "JetRapidity_1",
                     "DeltaYElecJet_1"]
axis_labels = [("Dijet Mass","m_{jj} [GeV]","(1/N)d#sigma /dm_{jj} [events/GeV]"),
               ("Dijet Mass - Signal Region","m_{jj} [GeV]","(1/N)d#sigma /dm_{jj} [events/GeV]"), 
               ("W Boson p_{T}","p_{T} [GeV]","(1/N)d#sigma /dp_{T} [events/GeV]"),
               ("Leading Jet p_{T}","p_{T} [GeV]","(1/N)d#sigma /dp_{T} [events/GeV]"),
               ("Second Jet p_{T}","p_{T} [GeV]","(1/N)d#sigma /dp_{T} [events/GeV]"),
               ("#Delta#phi for Two Leading Jets - Signal Region","#Delta#phi","(1/N)d#sigma /#Delta#phi [events]"), 
               ("#Deltay for Two Leading Jets - Signal Region","#Deltay","(1/N)d#sigma /#Deltay [events]"),
               ("#DeltaR for Two Leading Jets - Signal Region","#DeltaR","(1/N)d#sigma /#DeltaR [events]"),
               ("Dijet Mass - Control Region","m_{jj} [GeV]","(1/N)d#sigma /dm_{jj} [events/GeV]"),
               ("Scalar Sum of Event p_{T} - Signal Region","H_{T} [GeV]","(1/N)d#sigma /dH_{T} [events/GeV]"),
               ("Boosted Third Jet Rapidity - Signal Region","#Deltay^{*}","(1/N)d#sigma /#Deltay^{*} [events]"),
               ("Jet Rapidity - Signal Region","#Deltay","(1/N)d#sigma /#Deltay [events]"),
               ("#Deltay for Leading Jet and Lepton - Signal Region","#Deltay","(1/N)d#sigma /#Deltay [events]")]

for idx,hist_to_get in enumerate(histograms_to_get):
    c1.cd()
    pad1 = ROOT.TPad("pad1","top pad",0,0.40,1,1)
    pad2 = ROOT.TPad("pad2","bottom pad",0,0,1,0.40)
    pad1.SetFillStyle(0)
    pad1.SetFrameFillStyle(0)
    pad2.SetFillStyle(0)
    pad2.SetFrameFillStyle(0)
    pad1.Draw()
    pad2.Draw()
    
    bin = 1
    rebin = 1
    histo1 = root_file_1.Get(hist_to_get)
    num_of_bins = histo1.GetNbinsX()
    if num_of_bins >= 200: rebin = 5
    if rebin == 1 and num_of_bins >= 100: rebin = 2
    histo1.Rebin(rebin)
    histo1.SetLineColor(ROOT.TAttFill.kBlack)
    histo1.Scale(1.0/histo1.Integral("width"))
    first_bin1 = histo1.GetBinContent(bin)
    while first_bin1 == 0.0:
        bin += 1
        first_bin1 = histo1.GetBinContent(bin)

    histo2 = root_file_2.Get(hist_to_get)
    histo2.Rebin(rebin)
    histo2.SetLineColor(ROOT.TAttFill.kRed)
    first_bin2 = histo2.GetBinContent(bin)
    histo2.Scale(1.0/histo2.Integral("width"))

    histo3 = root_file_3.Get(hist_to_get)
    histo3.Rebin(rebin)
    histo3.SetLineColor(ROOT.TAttFill.kGreen)
    first_bin3 = histo3.GetBinContent(bin)
    histo3.Scale(1.0/histo3.Integral("width"))

    histo4 = root_file_4.Get(hist_to_get)
    histo4.Rebin(rebin)
    histo4.SetLineColor(ROOT.TAttFill.kBlue)
    first_bin4 = histo4.GetBinContent(bin)
    histo4.Scale(1.0/histo4.Integral("width"))

    leg.AddEntry(histo1,"Sherpa 1.4 Wmunu","l")
    leg.AddEntry(histo2,"Sherpa 1.4 Wenu","l")
    leg.AddEntry(histo3,"Powheg Wmunu", "l")
    leg.AddEntry(histo4,"Sherpa 2.0 Wenu", "l")


    #------------Histograms-------------------------
    pad1.cd()
    pad1.SetLogy()

    histo1.SetTitle(axis_labels[idx][0])
    histo1.GetXaxis().SetTitle(axis_labels[idx][1])
    histo1.GetYaxis().SetTitle(axis_labels[idx][2])
    histo1.Draw("HIST E SAME")
    histo2.Draw("HIST E SAME")
    histo3.Draw("HIST E SAME")
    histo4.Draw("HIST E SAME")
    leg.Draw()

    #------------Ratio Plot-------------------------
    pad2.cd()
    histo_err = histo1.Clone()
    histo_err.Divide(histo_err)
    histo_err.GetXaxis().SetTitle(axis_labels[idx][1])
    histo_err.GetYaxis().SetTitle("Other_MC/Black_MC")
    histo_err.SetFillStyle(3004)
    histo_err.SetFillColor(ROOT.TAttLine.kBlack)
    histo_err.Draw("E2")

    histo_rat = histo2.Clone()
    histo_rat.Divide(histo1)
    histo_rat.Draw("SAME")

    histo_rat2 = histo3.Clone()
    histo_rat2.Divide(histo1)
    histo_rat2.Draw("SAME")

    histo_rat3 = histo4.Clone()
    histo_rat3.Divide(histo1)
    histo_rat3.Draw("SAME")

    c1.SaveAs(hist_to_get+".pdf")
    leg.Clear()
    c1.Clear()
    
    #del histo1,histo2,histo3,histo4
    #del histo_err,histo_rat,histo_rat2,histo_rat3