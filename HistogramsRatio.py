import ROOT

def Large_label_title_top(histo1):
    histo1.GetXaxis().SetLabelSize(33)
    histo1.GetXaxis().SetTitleSize(0.065)
    histo1.GetYaxis().SetTitleSize(0.065)
    histo1.GetXaxis().SetTickLength(0.04)
    histo1.GetYaxis().SetTickLength(0.04)
    histo1.GetXaxis().SetLabelSize(0.065)
    histo1.GetYaxis().SetLabelSize(0.065)
    histo1.GetYaxis().SetNdivisions(507)
    histo1.GetYaxis().SetTitleOffset(0.62*1.37)
    histo1.SetLineWidth(2)
    
def Large_label_title_bot(histo1):
    histo1.GetXaxis().SetLabelSize(33)
    histo1.GetXaxis().SetTitleSize(0.12)
    histo1.GetYaxis().SetTitleSize(0.12)
    histo1.GetXaxis().SetTickLength(0.05)
    histo1.GetYaxis().SetTickLength(0.05)
    histo1.GetXaxis().SetLabelSize(0.12)
    histo1.GetYaxis().SetLabelSize(0.12)
    histo1.GetYaxis().SetTitleOffset(0.45)
    histo1.GetYaxis().SetNdivisions(507)
    histo1.SetLineWidth(2)

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
RATRY1=0.0
RATRY2=3.0
NORMED=True
INTEGRATE=False
max_val = 0.0

# Number of files to be opened
FILES=1
# Number of curves to be plotted
REPNFIL=3
# Histogram base name
hist_base = "DijetMass_2jet_1"
if (NORMED): hist_base = "Normalized_XS/"+hist_base+"_norm"

# open files, set normalization, retrieve+scale && rebin histos
fnames1 = ["VBF_Systematics.root"]
legents = ["Sherpa Nominal", "Sherpa Nominal MjjFilt", "POWHEG Nominal bornsuppfact"]
histpaths = ["147775.Nominal_Sherpa_Background/", "129930.Nominal_Sherpa_Background_MjjFilt/", "000001.Powheg.W2jets.Nominal/"]

fpoint1 = []
for i in range(FILES):
    file_name = ROOT.TFile(fnames1[i])
    fpoint1.append(file_name)
    if not fpoint1[i].IsOpen():
        print "no file found for: "+fnames1[i]+"\n"
        ROOT.gROOT.ProcessLine(".q")
        
hvect1 = []
LineStyle = [1 , 1, 1]
LineColor = ["ROOT.TAttLine.kBlack" , "ROOT.TAttLine.kRed+1", "ROOT.TAttLine.kBlue"]
LineWidth = [2 , 2, 2]
MarkerStyle = [0 , 0, 0]
MarkerSize = [0 , 0, 0]
        
for i in range(REPNFIL):
    hist_to_get = histpaths[i] + hist_base
    hvect1.append(fpoint1[0].Get(hist_to_get))
    hvect1[i].Rebin(5) 
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
    hvect1[i].Draw("same")
    hvect1[i].Draw("samep")

# margins :
lx1,lx2=0.60,0.90 
ly1,ly2=0.9-0.10*REPNFIL,0.89
ptitx1,ptitx2=0.01,lx1+0.1
ptity1,ptity2=0.91,0.996

# legend
leg = ROOT.TLegend(lx1,ly1,lx2,ly2)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetBorderSize(0)
for i in range(REPNFIL):
    leg.AddEntry(hvect1[i],legents[i],"pl")
leg.Draw()

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
for i in range(REPNFIL):
    hist_clones.append(hvect1[i].Clone())
    hist_clones[i].Divide(hist_clones[0])
hist_clones[0].Divide(hist_clones[0])

if (SETYRATRANGE == 1): hist_clones[0].SetAxisRange(RATRY1,RATRY2,"y")
#hist_clones[0].GetXaxis().SetTitle("pt[GeV]")
hist_clones[0].GetYaxis().SetTitle("Filt/NoFilt")
hist_clones[0].SetFillStyle(3004)
hist_clones[0].SetFillColor(eval(LineColor[0]))
Large_label_title_bot(hist_clones[0])
hist_clones[0].Draw("E2")

for i in range(REPNFIL):
    hist_clones[i].Draw("same")
    hist_clones[i].Draw("samep")

#---------------------------------------------------------------------------------------
if not NORMED: c0.SaveAs("Distribution.pdf")
if NORMED: c0.SaveAs("Normalized.pdf")

ROOT.gROOT.ProcessLine(".q")