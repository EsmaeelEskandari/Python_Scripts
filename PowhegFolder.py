import glob, os, shutil

def getFolderName(channel,shift,folder_names,E_cm):
    if channel == "w2jet":
        for folder in folder_names[0:7]:
            if shift in folder:
                is_Dir = os.path.isdir("./"+folder)
                return folder,is_Dir
    elif channel == "VBF_Wmunu":
        for folder in folder_names[7:15]:
            if E_cm == "7TeV":
                is_Dir = os.path.isdir("./"+folder)
                return folder_names[14],is_Dir
            elif shift in folder:
                is_Dir = os.path.isdir("./"+folder)
                return folder,is_Dir
                
def makeAndMove(is_Dir,channel,folder):
    if not is_Dir:
        cmd = "mkdir {0}".format(folder)
        os.system(cmd)
    cmd = "mv {0} {1}".format(channel,folder)
    os.system(cmd)
    return

folder_names = ["000001.Powheg.W2jets.Nominal.bornsuppfact", "000002.Powheg.W2jets.MuFdown.bornsuppfact", 
                "000003.Powheg.W2jets.MuFup.bornsuppfact", "000004.Powheg.W2jets.MuRdown.bornsuppfact", 
                "000005.Powheg.W2jets.MuRup.bornsuppfact", "000006.Powheg.W2jets.MuRdownMuFdown.bornsuppfact", 
                "000007.Powheg.W2jets.MuRupMuFup.bornsuppfact",
                "000015.Powheg.VBF.Nominal.ptj_gencut", "000016.Powheg.VBF.MuFdown.ptj_gencut", 
                "000017.Powheg.VBF.MuFup.ptj_gencut", "000018.Powheg.VBF.MuRdown.ptj_gencut", 
                "000019.Powheg.VBF.MuRup.ptj_gencut","000020.Powheg.VBF.MuRdownMuFdown.ptj_gencut", 
                "000021.Powheg.VBF.MuRupMuFup.ptj_gencut", "000022.Powheg.VBF.Nominal.ptj_gencut_7TeV",
                "000023.Powheg.VBF.Nominal.7TeV_noshower"]
                
shifts = [".Nominal.", ".MuFdown.", ".MuFup.", ".MuRdown.", ".MuRup.", ".MuRdownMuFdown.", ".MuRupMuFup."]
                
dataset_folders = glob.glob("*.PowhegPythia8.*")

for dataset in dataset_folders:
    if dataset.split("_")[-1] == "r1":
        dest = "_".join(dataset.split("_")[:-1])
        cmd = "mv {0}/* {1}".format(dataset,dest)
        os.system(cmd)
        cmd = "rm -r {0}".format(dataset)
        os.system(cmd)
        
dataset_folders = glob.glob("*.PowhegPythia8.*")

for dataset in dataset_folders:
    for shift in shifts:
        E_cm = "8TeV"
        if ("VBF_Wmunu" in dataset) and (shift in dataset) and ("Wplus" in dataset):
            if "7TeV" in dataset: E_cm = "7TeV"
            folder,is_Dir = getFolderName("VBF_Wmunu",shift,folder_names,E_cm)
            os.rename(dataset, "Wplus")
            makeAndMove(is_Dir,"Wplus",folder)
        elif ("VBF_Wmunu" in dataset) and (shift in dataset) and ("Wminus" in dataset):
            if "7TeV" in dataset: E_cm = "7TeV"
            folder,is_Dir = getFolderName("VBF_Wmunu",shift,folder_names,E_cm)
            os.rename(dataset, "Wminus")
            makeAndMove(is_Dir,"Wminus",folder)
        elif ("w2jet" in dataset) and (shift in dataset) and ("Wplus" in dataset):
            folder,is_Dir = getFolderName("w2jet",shift,folder_names,E_cm)
            os.rename(dataset, "Wplus")
            makeAndMove(is_Dir,"Wplus",folder)
        elif ("w2jet" in dataset) and (shift in dataset) and ("Wminus" in dataset):
            folder,is_Dir = getFolderName("w2jet",shift,folder_names,E_cm)
            os.rename(dataset, "Wminus")
            makeAndMove(is_Dir,"Wminus",folder)
