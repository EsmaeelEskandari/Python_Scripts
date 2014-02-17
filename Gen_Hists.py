import ROOT

root_file = ROOT.TFile.Open("VBF_Systematics.root")
root_file_stats = ROOT.TFile.Open("VBF_Systematics_merged_stats.root")

hist_to_get = "147295.min_n_tchannels_CKKW30_MjjFilt/DijetMass_2jet_1"

histo1 = root_file.Get(hist_to_get)
histo1.Rebin(5)
histo2 = root_file_stats.Get(hist_to_get)
histo2.Rebin(5)
histo2.SetLineColor(ROOT.TAttFill.kRed)

c1 = ROOT.TCanvas('c1','Stats Comparison',0,0,640,640)
c1.SetLogy()

histo1.Draw("HIST E SAME")
histo2.Draw("HIST E SAME")

c1.SaveAs("Stats_Comparison.pdf")
c1.Clear()