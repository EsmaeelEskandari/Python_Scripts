import ROOT

root_file = ROOT.TFile.Open("VBF_Systematics.root")
#root_file_stats = ROOT.TFile.Open("VBF_Systematics_merged_stats.root")
ROOT.gStyle.SetOptStat(0)

c1 = ROOT.TCanvas('c1','Stats Comparison',50,50,865,780)
c1.cd()
pad1 = ROOT.TPad("pad1","top pad",0,0.40,1,1)
pad2 = ROOT.TPad("pad2","bottom pad",0,0,1,0.40)
pad1.SetFillStyle(0)
pad1.SetFrameFillStyle(0)
pad2.SetFillStyle(0)
pad2.SetFrameFillStyle(0)
pad1.Draw()
pad2.Draw()
leg = ROOT.TLegend(0.2,0.2,0.5,0.4)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)

hist_to_get = "129930.Nominal_Sherpa_Background_MjjFilt/DijetMass_2jet_1"
hist_to_get2 = "000001.Powheg.W2jets.Nominal/DijetMass_2jet_1"

histo1 = root_file.Get(hist_to_get)
histo1 = histo1.Clone()
histo1.Rebin(5)
histo1.SetLineColor(ROOT.TAttFill.kBlue)
first_bin1 = histo1.GetBinContent(5)
#histo2 = root_file_stats.Get(hist_to_get)
histo2 = root_file.Get(hist_to_get2)
histo2 = histo2.Clone()
histo2.Rebin(5)
histo2.SetLineColor(ROOT.TAttFill.kRed)
first_bin2 = histo2.GetBinContent(5)
histo2.Scale(first_bin1/first_bin2)

leg.AddEntry(histo1,"Sherpa","l")
leg.AddEntry(histo2,"Powheg","l")


#------------Histograms-------------------------
pad1.cd()
pad1.SetLogy()
histo1.Draw("HIST E SAME")
histo2.Draw("HIST E SAME")
leg.Draw()

#------------Ratio Plot-------------------------
pad2.cd()
histo_err = histo1.Clone()
histo_err.Divide(histo_err)
histo_err.GetYaxis().SetTitle("Powheg/Sherpa")
histo_err.SetFillStyle(3004)
histo_err.SetFillColor(ROOT.TAttLine.kBlack)
histo_err.Draw("E2")

histo_rat = histo2.Clone()
histo_rat.Divide(histo1)
histo_rat.Draw("SAME")

c1.SaveAs("Sherpa_v_Powheg_Nominal.pdf")
c1.Clear()