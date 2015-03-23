import ROOT
import os, glob

hf = ROOT.TFile("Acc_Study.root", "RECREATE")

dataset_names = glob.glob("user.cjohnson*")

for idx,folder in enumerate(dataset_names):
    print folder
    # histogram manipulation and such
    #os.chdir(folder+"/")
    hf.mkdir(folder)
    hf.cd(folder)
    ROOT.gDirectory.mkdir(folder)
    file_name = "merged.root"
    root_file = ROOT.TFile.Open("./"+folder+"/"+file_name)
    for hist in root_file.GetListOfKeys():
        histogram = root_file.Get(hist.GetName())
        histogram_add = root_file_add.Get(hist)
        hf.cd(folder)
        histogram.Write()
    hf.cd(folder)
    root_file.Close()
    hf.cd()
    os.chdir("..")

hf.Write()
hf.Close()
print "Job Complete!!!"
