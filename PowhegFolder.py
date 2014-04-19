import glob, os, shutil

def getFolderName(channel,shift,folder_names):
    if channel == "w2jet":
        for folder in folder_names[0:7]:
            if shift in folder:
                return folder
    elif channel == "VBF_Wmunu":
        for folder in folder_names[7:14]:
            if shift in folder:
                return folder

folder_names = ["000001.Powheg.W2jets.Nominal.bornsuppfact", "000002.Powheg.W2jets.MuFdown.bornsuppfact", 
                "000003.Powheg.W2jets.MuFup.bornsuppfact", "000004.Powheg.W2jets.MuRdown.bornsuppfact", 
                "000005.Powheg.W2jets.MuRup.bornsuppfact", "000006.Powheg.W2jets.MuRdownMuFdown.bornsuppfact", 
                "000007.Powheg.W2jets.MuRupMuFup.bornsuppfact",
                "000015.Powheg.VBF.Nominal.ptj_gencut", "000016.Powheg.VBF.MuFdown.ptj_gencut", 
                "000017.Powheg.VBF.MuFup.ptj_gencut", "000018.Powheg.VBF.MuRdown.ptj_gencut", 
                "000019.Powheg.VBF.MuRup.ptj_gencut","000020.Powheg.VBF.MuRdownMuFdown.ptj_gencut", 
                "000021.Powheg.VBF.MuRupMuFup.ptj_gencut"]
                
shifts = [".Nominal.", ".MuFdown.", ".MuFup.", ".MuRdown.", ".MuRup.", ".MuRdownMuFdown.", ".MuRupMuFup."]
                
dataset_folders = glob.glob("*.PowhegPythia8.*")

for dataset in dataset_folders:
    for shift in shifts:
        if ("VBF_Wmunu" in dataset) and (shift in dataset) and ("Wplus" in dataset):
            folder = getFolderName("VBF_Wmunu",shift,folder_names)
            os.rename(dataset, "Wplus")
            shutil.move("Wplus", folder)
        elif ("VBF_Wmunu" in dataset) and (shift in dataset) and ("Wminus" in dataset):
            folder = getFolderName("VBF_Wmunu",shift,folder_names)
            os.rename(dataset, "Wminus")
            shutil.move("Wminus", folder)
        elif ("w2jet" in dataset) and (shift in dataset) and ("Wplus" in dataset):
            folder = getFolderName("w2jet",shift,folder_names)
            os.rename(dataset, "Wplus")
            shutil.move("Wplus", folder)
        elif ("w2jet" in dataset) and (shift in dataset) and ("Wminus" in dataset):
            folder = getFolderName("w2jet",shift,folder_names)
            os.rename(dataset, "Wminus")
            shutil.move("Wminus", folder)
