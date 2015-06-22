import ROOT
from Aux_Functions import *

datasets = GetListDataset('pwhg_sig_ptjgencut')
datasetNames = GetListDataset('dataset_names')

file_name="VBF_Systematics_DEta"
root_file = ROOT.TFile.Open(file_name+".root")

fidXS = []
CutFlowNames = ["CutFlow_1", "WeightCutFlow_1"]
for ds in datasets:
    xsec = datasetNames[ds][0]
    cf = root_file.Get(ds+"/"+CutFlowNames[0])
    wcf = root_file.Get(ds+"/"+CutFlowNames[1])
    cf_ratio = cf.GetBinContent(9)/cf.GetBinContent(2)
    wcf_ratio = wcf.GetBinContent(9)/wcf.GetBinContent(2)
    fidXS.append(wcf_ratio*xsec*1000.)
    print ds
    print "CutFlow:\t{0}\t{1}".format(cf_ratio,cf_ratio*xsec)
    print "WeightCutFlow:\t{0}\t{1}".format(wcf_ratio,wcf_ratio*xsec)
    print ""
    
Nominal = fidXS[0]
fidXS_diff = []
for var in fidXS:
    fidXS_diff.append(var-Nominal)
    
print "{0} +{1} {2} fb".format(Nominal, max(fidXS_diff), min(fidXS_diff))
