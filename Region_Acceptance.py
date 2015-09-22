import ROOT, sys, math, pprint
from Aux_Functions import *

dataset_names = GetListDataset('dataset_names')
# ============== Electron =============
# --------------- 7 TeV ---------------
Pwhg_QCD_WmJJ_el_7TeV  = [ '185930.PowhegPythia8_W2Jets_Wm_el_Nominal.7TeV' ]
Pwhg_QCD_WpJJ_el_7TeV  = [ '185931.PowhegPythia8_W2Jets_Wp_el_Nominal.7TeV' ]
Pwhg_QCD_WpmJJ_el_7TeV = [ '000031.Powheg.W2jets.Nominal.electron.7TeV' ]
Pwhg_EWK_WmJJ_el_7TeV  = [ '185946.PowhegPythia8_VBF_Wm_el_Nominal.7TeV' ]
Pwhg_EWK_WpJJ_el_7TeV  = [ '185947.PowhegPythia8_VBF_Wp_el_Nominal.7TeV' ]
Pwhg_EWK_WpmJJ_el_7TeV = [ '000032.Powheg.VBFW.electron.7TeV' ]
# --------------- 8 TeV ---------------
Pwhg_QCD_WmJJ_el_8TeV  = [ '185836.PowhegPythia8_Wm_Nominal_elec' ]
Pwhg_QCD_WpJJ_el_8TeV  = [ '185837.PowhegPythia8_Wp_Nominal_elec' ]
Pwhg_QCD_WpmJJ_el_8TeV = [ '000029.Powheg.W2jets.Nominal.electron' ]
Pwhg_EWK_WmJJ_el_8TeV  = [ '185847.PowhegPythia8.VBF_Wm_Nominal_elec' ]
Pwhg_EWK_WpJJ_el_8TeV  = [ '185848.PowhegPythia8.VBF_Wp_Nominal_elec' ]
Pwhg_EWK_WpmJJ_el_8TeV = [ '000030.Powheg.VBFW.electron' ]

# =============== Muon ================
# --------------- 7 TeV ---------------
Pwhg_QCD_WmJJ_mu_7TeV  = [ '185932.PowhegPythia8_W2Jets_Wm_mu_Nominal.7TeV','185933.PowhegPythia8_W2Jets_Wm_mu_MuFdown.7TeV','185934.PowhegPythia8_W2Jets_Wm_mu_MuFup.7TeV','185935.PowhegPythia8_W2Jets_Wm_mu_MuRdown.7TeV','185936.PowhegPythia8_W2Jets_Wm_mu_MuRup.7TeV','185937.PowhegPythia8_W2Jets_Wm_mu_MuRFdown.7TeV','185938.PowhegPythia8_W2Jets_Wm_mu_MuRFup.7TeV' ]
Pwhg_QCD_WpJJ_mu_7TeV  = [ '185939.PowhegPythia8_W2Jets_Wp_mu_Nominal.7TeV','185940.PowhegPythia8_W2Jets_Wp_mu_MuFdown.7TeV','185941.PowhegPythia8_W2Jets_Wp_mu_MuFup.7TeV','185942.PowhegPythia8_W2Jets_Wp_mu_MuRdown.7TeV','185943.PowhegPythia8_W2Jets_Wp_mu_MuRup.7TeV','185944.PowhegPythia8_W2Jets_Wp_mu_MuRFdown.7TeV','185945.PowhegPythia8_W2Jets_Wp_mu_MuRFup.7TeV' ]
Pwhg_QCD_WpmJJ_mu_7TeV = [ '000008.Powheg.W2jets.Nominal.7TeV','000009.Powheg.W2jets.MuFdown.7TeV','000010.Powheg.W2jets.MuFup.7TeV','000011.Powheg.W2jets.MuRdown.7TeV','000012.Powheg.W2jets.MuRup.7TeV','000013.Powheg.W2jets.MuRdownMuFdown.7TeV','000014.Powheg.W2jets.MuRupMuFup.7TeV' ]
Pwhg_EWK_WmJJ_mu_7TeV  = [ '185948.PowhegPythia8_VBF_Wm_mu_Nominal.7TeV','185949.PowhegPythia8_VBF_Wm_mu_MuFdown.7TeV','185950.PowhegPythia8_VBF_Wm_mu_MuFup.7TeV','185951.PowhegPythia8_VBF_Wm_mu_MuRdown.7TeV','185952.PowhegPythia8_VBF_Wm_mu_MuRup.7TeV','185953.PowhegPythia8_VBF_Wm_mu_MuRFdown.7TeV','185954.PowhegPythia8_VBF_Wm_mu_MuRFup.7TeV' ]
Pwhg_EWK_WpJJ_mu_7TeV  = [ '185955.PowhegPythia8_VBF_Wp_mu_Nominal.7TeV','185956.PowhegPythia8_VBF_Wp_mu_MuFdown.7TeV','185957.PowhegPythia8_VBF_Wp_mu_MuFup.7TeV','185958.PowhegPythia8_VBF_Wp_mu_MuRdown.7TeV','185959.PowhegPythia8_VBF_Wp_mu_MuRup.7TeV','185960.PowhegPythia8_VBF_Wp_mu_MuRFdown.7TeV','185961.PowhegPythia8_VBF_Wp_mu_MuRFup.7TeV' ]
Pwhg_EWK_WpmJJ_mu_7TeV = [ '000022.Powheg.VBF.Nominal.7TeV','000023.Powheg.VBF.MuFdown.7TeV','000024.Powheg.VBF.MuFup.7TeV','000025.Powheg.VBF.MuRdown.7TeV','000026.Powheg.VBF.MuRup.7TeV','000027.Powheg.VBF.MuRdownMuFdown.7TeV','000028.Powheg.VBF.MuRupMuFup.7TeV' ]
# --------------- 8 TeV ---------------
Pwhg_QCD_WmJJ_mu_8TeV  = [ '185696.PowhegPythia8_Wm_Nominal','185697.PowhegPythia8_Wm_MuFdown','185698.PowhegPythia8_Wm_MuFup','185699.PowhegPythia8_Wm_MuRdown','185700.PowhegPythia8_Wm_MuRup','185701.PowhegPythia8_Wm_MuRFdown','185702.PowhegPythia8_Wm_MuRFup' ]
Pwhg_QCD_WpJJ_mu_8TeV  = [ '185703.PowhegPythia8_Wp_Nominal','185704.PowhegPythia8_Wp_MuFdown','185705.PowhegPythia8_Wp_MuFup','185706.PowhegPythia8_Wp_MuRdown','185707.PowhegPythia8_Wp_MuRup','185708.PowhegPythia8_Wp_MuRFdown','185709.PowhegPythia8_Wp_MuRFup' ]
Pwhg_QCD_WpmJJ_mu_8TeV = [ '000001.Powheg.W2jets.Nominal.bornsuppfact','000002.Powheg.W2jets.MuFdown.bornsuppfact','000003.Powheg.W2jets.MuFup.bornsuppfact','000004.Powheg.W2jets.MuRdown.bornsuppfact','000005.Powheg.W2jets.MuRup.bornsuppfact','000006.Powheg.W2jets.MuRdownMuFdown.bornsuppfact','000007.Powheg.W2jets.MuRupMuFup.bornsuppfact' ]
Pwhg_EWK_WmJJ_mu_8TeV  = [ '185849.PowhegPythia8.VBF_Wm_Nominal','185850.PowhegPythia8.VBF_Wm_MuFdown','185851.PowhegPythia8.VBF_Wm_MuFup','185852.PowhegPythia8.VBF_Wm_MuRdown','185853.PowhegPythia8.VBF_Wm_MuRup','185854.PowhegPythia8.VBF_Wm_MuRdownMuFdown','185855.PowhegPythia8.VBF_Wm_MuRupMuFup' ]
Pwhg_EWK_WpJJ_mu_8TeV  = [ '185856.PowhegPythia8.VBF_Wp_Nominal','185857.PowhegPythia8.VBF_Wp_MuFdown','185858.PowhegPythia8.VBF_Wp_MuFup','185859.PowhegPythia8.VBF_Wp_MuRdown','185860.PowhegPythia8.VBF_Wp_MuRup','185861.PowhegPythia8.VBF_Wp_MuRdownMuFdown','185862.PowhegPythia8.VBF_Wp_MuRupMuFup' ]
Pwhg_EWK_WpmJJ_mu_8TeV = [ '000015.Powheg.VBF.Nominal.ptj_gencut','000016.Powheg.VBF.MuFdown.ptj_gencut','000017.Powheg.VBF.MuFup.ptj_gencut','000018.Powheg.VBF.MuRdown.ptj_gencut','000019.Powheg.VBF.MuRup.ptj_gencut','000020.Powheg.VBF.MuRdownMuFdown.ptj_gencut','000021.Powheg.VBF.MuRupMuFup.ptj_gencut' ]


All_DS_el_7TeV = Pwhg_QCD_WmJJ_el_7TeV+Pwhg_QCD_WpJJ_el_7TeV+Pwhg_QCD_WpmJJ_el_7TeV+Pwhg_EWK_WmJJ_el_7TeV+Pwhg_EWK_WpJJ_el_7TeV+Pwhg_EWK_WpmJJ_el_7TeV
All_DS_el_8TeV = Pwhg_QCD_WmJJ_el_8TeV+Pwhg_QCD_WpJJ_el_8TeV+Pwhg_QCD_WpmJJ_el_8TeV+Pwhg_EWK_WmJJ_el_8TeV+Pwhg_EWK_WpJJ_el_8TeV+Pwhg_EWK_WpmJJ_el_8TeV
All_DS_mu_7TeV = Pwhg_QCD_WmJJ_mu_7TeV+Pwhg_QCD_WpJJ_mu_7TeV+Pwhg_QCD_WpmJJ_mu_7TeV+Pwhg_EWK_WmJJ_mu_7TeV+Pwhg_EWK_WpJJ_mu_7TeV+Pwhg_EWK_WpmJJ_mu_7TeV
All_DS_mu_8TeV = Pwhg_QCD_WmJJ_mu_8TeV+Pwhg_QCD_WpJJ_mu_8TeV+Pwhg_QCD_WpmJJ_mu_8TeV+Pwhg_EWK_WmJJ_mu_8TeV+Pwhg_EWK_WpJJ_mu_8TeV+Pwhg_EWK_WpmJJ_mu_8TeV
All_DS = All_DS_el_7TeV+All_DS_el_8TeV+All_DS_mu_7TeV+All_DS_mu_8TeV

ListOfDSLists = [ Pwhg_QCD_WmJJ_el_7TeV, Pwhg_QCD_WpJJ_el_7TeV, Pwhg_EWK_WmJJ_el_7TeV, Pwhg_EWK_WpJJ_el_7TeV,
                  Pwhg_QCD_WmJJ_mu_7TeV, Pwhg_QCD_WpJJ_mu_7TeV, Pwhg_EWK_WmJJ_mu_7TeV, Pwhg_EWK_WpJJ_mu_7TeV,
                  Pwhg_QCD_WmJJ_el_8TeV, Pwhg_QCD_WpJJ_el_8TeV, Pwhg_EWK_WmJJ_el_8TeV, Pwhg_EWK_WpJJ_el_8TeV,
                  Pwhg_QCD_WmJJ_mu_8TeV, Pwhg_QCD_WpJJ_mu_8TeV, Pwhg_EWK_WmJJ_mu_8TeV, Pwhg_EWK_WpJJ_mu_8TeV ]

f = ROOT.TFile("VBF_Systematics.root")

# def GetError(Wplus, Wminus, typeName='abs'):
#     listName = [ sum(x) for x in zip(Wplus,Wminus) ]
#     nominal = listName[0]
#     if typeName == 'abs':
#         unit = 'pb'
#         diff_sqrd = [ (nominal-diff)*(nominal-diff) for diff in listName[1:] ]
#     elif typeName == 'rel':
#         unit = '%'
#         diff_sqrd = [ ((nominal-diff)*(nominal-diff))/(diff*diff)*100.0*100.0 for diff in listName[1:] ]
#     else:
#         print """typeName is not set properly: {0}. Needs to be 'abs' or 'rel'""".format(typeName)
#         sys.exit(0)
#
#     #return (nominal, sqrt(sum(diff_sqrd))), unit)
#     #return (nominal, math.sqrt(max(diff_sqrd)), unit)
#     if diff_sqrd:
#         return (nominal, math.sqrt(max(diff_sqrd)), unit)
#     else:
#         return (nominal, 0.0, unit)

def GetError(wChannel, typeName='abs'):
    nominal = wChannel[0]
    if typeName == 'abs':
        unit = 'pb'
        diff_sqrd = [ (nominal-diff)*(nominal-diff) for diff in wChannel[1:] ]
    elif typeName == 'rel':
        unit = '%'
        diff_sqrd = [ ((nominal-diff)*(nominal-diff))/(diff*diff)*100.0*100.0 for diff in wChannel[1:] ]
    else:
        print """typeName is not set properly: {0}. Needs to be 'abs' or 'rel'""".format(typeName)
        sys.exit(0)

    if diff_sqrd:
        return (nominal, math.sqrt(max(diff_sqrd)), unit)
    else:
        return (nominal, 0.0, unit)
        
def PrintInfo(ListOfDSLists, Title, binNames):
    f_out = open("{0}.txt".format(Title), "w")
    f_out.write("# ============ {0} ====================\n".format(Title))
    
    for List in ListOfDSLists:
        FidXS = {}
        NumEvnts = {}
        Acceptance = {}
        f_out.write(List[0]+"\n")
        for regNum in binNames:
            region = binNames[regNum]
            FidXS[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in List ]
            NumEvnts[region] = [ (EventsPerDS[List[i]][region]) for i in range(len(List)) ]
        for regNum in binNames:
            region = binNames[regNum]
            #error = GetError(FidXS_Wm[region],FidXS_Wp[region],'rel')
            error = GetError(FidXS[region],'rel')
            f_out.write("  Region {0}:\n".format(region))
            f_out.write("\tNumber of events: {0}\n".format(NumEvnts[region][0]))
            f_out.write("\tNominal Acceptance: {0}\n".format(NumEvnts[region][0]/NumEvnts['AllEvents'][0]))
            f_out.write("\tCross Section:\t{0} +- {1} {2}\n".format(error[0], error[1], error[2]))
            for i in range(len(List)):
                DS_Name = List[i]
                #f_out.write("""\t'True' Cross Section : {0} pb\n""".format( dataset_names[DS_Name][0] ))
                f_out.write("\tCross Section for {0}:\t{1} pb\n".format(DS_Name, FidXS[region][i]))
        f_out.write("\n")
    
    f_out.close()
    return

# bin 01 = "AllEvents"
# bin 02 = "Inclusive" Region (Passes all cuts w/o veto requirement)
# bin 03 = "HighMass15" Mjj > 1500 GeV (Passes all cuts w/o veto requirement)
# bin 04 = "HighMass20" Mjj > 2000 GeV (Passes all cuts w/o vetos requirement)
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
# bin 15 = "HighMass10" Mjj > 1000 GeV (Passes all cuts w/o veto requirement)
# bin 16 = "Signal10" (Passes all cuts, passes JC veto, passes LC veto, Mjj > 1000 GeV)
binNames = { 1: 'AllEvents', 2: 'Inclusive', 3: 'HighMass15', 4: 'HighMass20', 5: '!LC',
             6: '!JC', 7: '!LC!JC', 8: 'Signal', 9: 'aTGC_WpT500', 10: 'aTGC_WpT600',
             11: 'aTGC_WpT700', 12: 'aTGC_MT10', 13: 'aTGC_MT20', 14: 'aTGC_Mjj1000', 15: 'HighMass10', 16: 'Signal10' }

EventsPerDS = {}
WeightPerDS = {}
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
#pprint.pprint(EventsPerDS)

QCD_Elec_7TeV = [ Pwhg_QCD_WmJJ_el_7TeV, Pwhg_QCD_WpJJ_el_7TeV ]
PrintInfo(QCD_Elec_7TeV, "QCD_Elec_7TeV", binNames)
EWK_Elec_7TeV = [ Pwhg_EWK_WmJJ_el_7TeV, Pwhg_EWK_WpJJ_el_7TeV ]
PrintInfo(EWK_Elec_7TeV, "EWK_Elec_7TeV", binNames)
QCD_Muon_7TeV = [ Pwhg_QCD_WmJJ_mu_7TeV, Pwhg_QCD_WpJJ_mu_7TeV ]
PrintInfo(QCD_Muon_7TeV, "QCD_Muon_7TeV", binNames)
EWK_Muon_7TeV = [ Pwhg_EWK_WmJJ_mu_7TeV, Pwhg_EWK_WpJJ_mu_7TeV ]
PrintInfo(EWK_Muon_7TeV, "EWK_Muon_7TeV", binNames)
QCD_Elec_8TeV = [ Pwhg_QCD_WmJJ_el_8TeV, Pwhg_QCD_WpJJ_el_8TeV ]
PrintInfo(QCD_Elec_8TeV, "QCD_Elec_8TeV", binNames)
EWK_Elec_8TeV = [ Pwhg_EWK_WmJJ_el_8TeV, Pwhg_EWK_WpJJ_el_8TeV ]
PrintInfo(EWK_Elec_8TeV, "EWK_Elec_8TeV", binNames)
QCD_Muon_8TeV = [ Pwhg_QCD_WmJJ_mu_8TeV, Pwhg_QCD_WpJJ_mu_8TeV ]
PrintInfo(QCD_Muon_8TeV, "QCD_Muon_8TeV", binNames)
EWK_Muon_8TeV = [ Pwhg_EWK_WmJJ_mu_8TeV, Pwhg_EWK_WpJJ_mu_8TeV ]
PrintInfo(EWK_Muon_8TeV, "EWK_Muon_8TeV", binNames)

#-----------------------------------------------------------------------------------------------------
# for List in ListOfDSLists:
#     FidXS = {}
#     NumEvnts = {}
#     Acceptance = {}
#     print List[0]
#     for regNum in binNames:
#         region = binNames[regNum]
#         FidXS[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in List ]
#         NumEvnts[region] = [ (EventsPerDS[List[i]][region]) for i in range(len(List)) ]
#     for regNum in [ 1 ]:
#         region = binNames[regNum]
#         #error = GetError(FidXS_Wm[region],FidXS_Wp[region],'rel')
#         error = GetError(FidXS[region],'rel')
#         print "  Region {0}:".format(region)
#         print "\tNumber of events: {0}".format(NumEvnts[region][0])
#         print "\tAcceptance: {0}".format(NumEvnts[region][0]/NumEvnts['AllEvents'][0])
#         print "\tCross Section:\t{0} +- {1} {2}".format(error[0], error[1], error[2])
#         # for i in range(len(List)):
#         #     DS_Name = List[i]
#         #     print "\tCross Section for {0}:\t{1} pb".format(DS_Name, FidXS[region][i])
#     print "\n"

#-----------------------------------------------------------------------------------------------------
# # Pwhg_QCD_WpmJJ
# FidXS_Wm = {}
# FidXS_Wp = {}
# NumEvnts = {}
# Acceptance = {}
# print "----------- POWHEG QCD -----------"
# for regNum in binNames:
#     region = binNames[regNum]
#     FidXS_Wm[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in Pwhg_QCD_WmJJ_mu_7TeV ]
#     FidXS_Wp[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in Pwhg_QCD_WpJJ_mu_7TeV ]
#     NumEvnts[region] = [ (EventsPerDS[Pwhg_QCD_WmJJ_mu_7TeV[i]][region]+EventsPerDS[Pwhg_QCD_WpJJ_mu_7TeV[i]][region]) for i in range(len(Pwhg_QCD_WmJJ_mu_7TeV)) ]
#     error = GetError(FidXS_Wm[region],FidXS_Wp[region],'rel')
#     print "Region {0}:".format(region)
#     print "\tNumber of events: {0}".format(NumEvnts[region][0])
#     print "\tCross Section:\t{0} +- {1} {2}".format(error[0], error[1], error[2])
#     # for i in range(len(Pwhg_QCD_WpmJJ_mu_7TeV)):
#     #     DS_Name = Pwhg_QCD_WpmJJ_mu_7TeV[i]
#     #     print "\tCross Section for {0}:\t{1} pb".format(DS_Name, (FidXS_Wm[region][i]+FidXS_Wp[region][i]))

# # Pwhg_EWK_WpmJJ
# FidXS_Wm = {}
# FidXS_Wp = {}
# NumEvnts = {}
# Acceptance = {}
# print "----------- POWHEG EWK -----------"
# for regNum in binNames:
#     region = binNames[regNum]
#     FidXS_Wm[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in Pwhg_EWK_WmJJ_el_7TeV ]
#     FidXS_Wp[region] = [ (WeightPerDS[ds][region]/EventsPerDS[ds]['AllEvents']) for ds in Pwhg_EWK_WpJJ_el_7TeV ]
#     NumEvnts[region] = [ (EventsPerDS[Pwhg_EWK_WmJJ_el_7TeV[i]][region]+EventsPerDS[Pwhg_EWK_WpJJ_el_7TeV[i]][region]) for i in range(len(Pwhg_EWK_WmJJ_el_7TeV)) ]
#     error = GetError(FidXS_Wm[region],FidXS_Wp[region],'rel')
#     print "Region {0}:".format(region)
#     print "\tNumber of events: {0}".format(NumEvnts[region][0])
#     print "\tCross Section:\t{0} +- {1} {2}".format(error[0], error[1], error[2])
#     # for i in range(len(Pwhg_EWK_WpmJJ_mu_7TeV)):
#     #     DS_Name = Pwhg_EWK_WpmJJ_mu_7TeV[i]
#     #     print "\tCross Section for {0}:\t{1} pb".format(DS_Name, (FidXS_Wm[region][i]+FidXS_Wp[region][i]))






#----------------Extra Things-------------------------------------------------------------------------------------
# xsec_AMI  = [ dataset_names[ds][0] for ds in Pwhg_QCD_WmJJ ]
# error = GetError(xsec_AMI)
# print "Pwhg_QCD_WmJJ Total AMI Cross-section:\t{0}\t+- {1} {2}".format(error[0],error[1],error[2])
# xsec_Calc = [ WeightPerDS[ds]['AllEvents']/EventsPerDS[ds]['AllEvents'] for ds in Pwhg_QCD_WmJJ ]
# error = GetError(xsec_Calc)
# print "Pwhg_QCD_WmJJ Total Calc Cross-section:\t{0}\t+- {1} {2}".format(error[0],error[1],error[2])
