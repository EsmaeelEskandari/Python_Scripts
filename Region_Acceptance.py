import ROOT, sys
from Aux_Functions import *

dataset_names = GetListDataset('dataset_names')
Pwhg_QCD_WmJJ  = [ '185696.PowhegPythia8_Wm_Nominal','185697.PowhegPythia8_Wm_MuFdown','185698.PowhegPythia8_Wm_MuFup','185699.PowhegPythia8_Wm_MuRdown','185700.PowhegPythia8_Wm_MuRup','185701.PowhegPythia8_Wm_MuRFdown','185702.PowhegPythia8_Wm_MuRFup' ]
Pwhg_QCD_WpJJ  = [ '185703.PowhegPythia8_Wp_Nominal','185704.PowhegPythia8_Wp_MuFdown','185705.PowhegPythia8_Wp_MuFup','185706.PowhegPythia8_Wp_MuRdown','185707.PowhegPythia8_Wp_MuRup','185708.PowhegPythia8_Wp_MuRFdown','185709.PowhegPythia8_Wp_MuRFup' ]
Pwhg_QCD_WpmJJ = [ '000001.Powheg.W2jets.Nominal.bornsuppfact','000002.Powheg.W2jets.MuFdown.bornsuppfact','000003.Powheg.W2jets.MuFup.bornsuppfact','000004.Powheg.W2jets.MuRdown.bornsuppfact','000005.Powheg.W2jets.MuRup.bornsuppfact','000006.Powheg.W2jets.MuRdownMuFdown.bornsuppfact','000007.Powheg.W2jets.MuRupMuFup.bornsuppfact' ]
Pwhg_EWK_WmJJ  = [ '185849.PowhegPythia8.VBF_Wm_Nominal','185850.PowhegPythia8.VBF_Wm_MuFdown','185851.PowhegPythia8.VBF_Wm_MuFup','185852.PowhegPythia8.VBF_Wm_MuRdown','185853.PowhegPythia8.VBF_Wm_MuRup','185854.PowhegPythia8.VBF_Wm_MuRdownMuFdown','185855.PowhegPythia8.VBF_Wm_MuRupMuFup' ]
Pwhg_EWK_WpJJ  = [ '185856.PowhegPythia8.VBF_Wp_Nominal','185857.PowhegPythia8.VBF_Wp_MuFdown','185858.PowhegPythia8.VBF_Wp_MuFup','185859.PowhegPythia8.VBF_Wp_MuRdown','185860.PowhegPythia8.VBF_Wp_MuRup','185861.PowhegPythia8.VBF_Wp_MuRdownMuFdown','185862.PowhegPythia8.VBF_Wp_MuRupMuFup' ]
Pwhg_EWK_WpmJJ = [ '000015.Powheg.VBF.Nominal.ptj_gencut','000016.Powheg.VBF.MuFdown.ptj_gencut','000017.Powheg.VBF.MuFup.ptj_gencut','000018.Powheg.VBF.MuRdown.ptj_gencut','000019.Powheg.VBF.MuRup.ptj_gencut','000020.Powheg.VBF.MuRdownMuFdown.ptj_gencut','000021.Powheg.VBF.MuRupMuFup.ptj_gencut' ]
All_DS = Pwhg_QCD_WmJJ+Pwhg_QCD_WpJJ+Pwhg_QCD_WpmJJ+Pwhg_EWK_WmJJ+Pwhg_EWK_WpJJ+Pwhg_EWK_WpmJJ
f = ROOT.TFile("VBF_Systematics.root")

def GetError(listName, typeName='abs'):
    nominal = listName[0]
    if typeName == 'abs':
        unit = 'pb'
        diff_sqrd = [ (nominal-diff)*(nominal-diff) for diff in listName[1:] ]
    elif typeName == 'rel':
        unit = '%'
        diff_sqrd = [ ((nominal-diff)*(nominal-diff))/(diff*diff) for diff in listName[1:] ]
    else:
        print """typeName is not set properly: {0}. Needs to be 'abs' or 'rel'""".format(typeName)
        sys.exit(0)
        
    #return (nominal, sqrt(sum(diff_sqrd))), unit)
    return (nominal, sqrt(max(diff_sqrd)), unit)


EventsPerDS = {}
WeightPerDS = {}

# bin 01 = "AllEvents"
# bin 02 = "Inclusive" Region (Passes all cuts w/o vetos)
# bin 03 = "HighMass15" Mjj > 1500 GeV (Passes all cuts w/o vetos)
# bin 04 = "HighMass20" Mjj > 2000 GeV (Passes all cuts w/o vetos)
# bin 05 = "!LC" (Passes all cuts, passes JC veto, fails LC veto)
# bin 06 = "!JC" (Passes all cuts, fails JC veto, passes LC veto)
# bin 07 = "!LC!JC" (Passes all cuts, fails JC veto, fails LC veto)
# bin 08 = "Signal" (Passes all cuts, passes JC veto, passes, LC veto)
# bin 09 = "aTGC_WpT500" (Signal Region with boson pT > 500 GeV)
# bin 10 = "aTGC_WpT600" (Signal Region with boson pT > 600 GeV)
# bin 11 = "aTGC_WpT700" (Signal Region with boson pT > 700 GeV)
# bin 12 = "aTGC_MT10" (Signal Region with lowered MT > 10 GeV and boson pT > 600 GeV)
# bin 13 = "aTGC_MT20" (Signal Region with lowered MT > 20 GeV and boson pT > 600 GeV)
# bin 14 = "aTGC_Mjj1000" (Signal Region with boson pT > 600 GeV and Mjj > 1000 GeV)
binNames = { 1: 'AllEvents', 2: 'Inclusive', 3: 'HighMass15', 4: 'HighMass20', 5: '!LC',
             6: '!JC', 7: '!LC!JC', 8: 'Signal', 9: 'aTGC_WpT500', 10: 'aTGC_WpT600',
             11: 'aTGC_WpT700', 12: 'aTGC_MT10', 13: 'aTGC_MT20', 14: 'aTGC_Mjj1000' }

for ds in All_DS:
    Events = f.Get(ds+"/RegionPop")
    EventsInRegions = {}
    Weights = f.Get(ds+"/RegionPopWeight")
    WeightInRegions = {}
    for regionBin in binNames:
        Events_binContent = Events.GetBinContent(regionBin)
        EventsInRegions[binNames[regionBin]] = Events_binContent
        Weights_binContent = Weights.GetBinContent(regionBin)
        WeightInRegions[binNames[regionBin]] = Weights_binContent
    EventsPerDS[ds] = EventsInRegions
    WeightPerDS[ds] = WeightInRegions
    
# Now use list of datasets to be compared to extract info from EventsPerDS/WeightPerDS

# xsec_AMI  = [ dataset_names[ds][0] for ds in Pwhg_QCD_WmJJ ]
# error = GetError(xsec_AMI)
# print "Pwhg_QCD_WmJJ Total AMI Cross-section:\t{0}\t+- {1} {2}".format(error[0],error[1],error[2])
# xsec_Calc = [ WeightPerDS[ds]['AllEvents']/EventsPerDS[ds]['AllEvents'] for ds in Pwhg_QCD_WmJJ ]
# error = GetError(xsec_Calc)
# print "Pwhg_QCD_WmJJ Total Calc Cross-section:\t{0}\t+- {1} {2}".format(error[0],error[1],error[2])

# Pwhg_QCD_WmJJ    
FiducialXS = {}
Acceptance = {}
for regNum in binNames:
    region = binNames[regNum]
    FiducialXS[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in Pwhg_QCD_WmJJ ]
    Acceptance[region] = [ (WeightPerDS[ds][region]/WeightPerDS[ds]['AllEvents']) for ds in Pwhg_QCD_WmJJ ]
    error = GetError(FiducialXS[region])
    print "Pwhg_QCD_WmJJ Cross Section in {0} Region:\t{1} +- {2} {3}".format(region,error[0],error[1],error[2])
    
# Pwhg_QCD_WpJJ    
FiducialXS = {}
for regNum in binNames:
    region = binNames[regNum]
    FiducialXS[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in Pwhg_QCD_WpJJ ]
    Acceptance[region] = [ (WeightPerDS[ds][region]/WeightPerDS[ds]['AllEvents']) for ds in Pwhg_QCD_WpJJ ]
    error = GetError(FiducialXS[region])
    print "Pwhg_QCD_WpJJ Cross Section in {0} Region:\t{1} +- {2} {3}".format(region,error[0],error[1],error[2])
    
# WmJJ/WpJJ combined:
FiducialXS = {}
for regNum in binNames:
    region = binNames[regNum]
    FiducialXS[region] = [ ( (WeightPerDS[Pwhg_WmJJ[i]][region]+WeightPerDS[Pwhg_WpJJ[i]][region])/(EventsPerDS[Pwhg_WmJJ[i]]['AllEvents']+EventsPerDS[Pwhg_WpJJ[i]]['AllEvents']) ) for i in range(len(Pwhg_QCD_WmJJ)) ]
    Acceptance[region] = [ ( (WeightPerDS[Pwhg_WmJJ[i]][region]+WeightPerDS[Pwhg_WpJJ[i]][region])/(WeightPerDS[Pwhg_WmJJ[i]]['AllEvents']+WeightPerDS[Pwhg_WpJJ[i]]['AllEvents']) ) for i in range(len(Pwhg_QCD_WmJJ)) ]
    error = GetError(FiducialXS[region])
    print "Pwhg_QCD_(Wp+Wm)JJ Cross Section in {0} Region:\t{1} +- {2} {3}".format(region,error[0],error[1],error[2])

# Pwhg_QCD_WpmJJ
FiducialXS = {}
for regNum in binNames:
    region = binNames[regNum]
    FiducialXS[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in Pwhg_QCD_WpmJJ ]
    Acceptance[region] = [ (WeightPerDS[ds][region]/WeightPerDS[ds]['AllEvents']) for ds in Pwhg_QCD_WpmJJ ]
    error = GetError(FiducialXS[region])
    print "Pwhg_QCD_WpmJJ Cross Section in {0} Region:\t{1} +- {2} {3}".format(region,error[0],error[1],error[2])
