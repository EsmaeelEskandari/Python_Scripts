import ROOT
import os
from pyAMI.client import AMIClient
from pyAMI.auth import AMI_CONFIG, create_auth_config
from pyAMI.query import *
from pyAMI.exceptions import *

hf = ROOT.TFile("VBF_Systematics.root", "RECREATE")

datasets = 	['mc12_8TeV.129916.Sherpa_CT10_Wmunu2JetsEW1JetQCD15GeV_min_n_tchannels.evgen.EVNT.e1557/',
			 'mc12_8TeV.147294.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_CKKW30.evgen.EVNT.e1805/',
			 'mc12_8TeV.147295.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_CKKW30_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147296.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFdown.evgen.EVNT.e1805/',
			 'mc12_8TeV.147297.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFdown_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147298.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFup.evgen.EVNT.e1805/',
			 'mc12_8TeV.147299.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFup_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147300.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi1.evgen.EVNT.e1805/',
			 'mc12_8TeV.147301.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi1_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147302.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi2.evgen.EVNT.e1805/',
			 'mc12_8TeV.147303.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi2_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147304.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_Shower1.evgen.EVNT.e1805/',
			 'mc12_8TeV.147305.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_Shower1_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147306.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRdown.evgen.EVNT.e1805/',
			 'mc12_8TeV.147307.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRdown_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147308.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRup.evgen.EVNT.e1805/',
			 'mc12_8TeV.147309.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRup_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147310.Sherpa_CT10_Wmunu_CKKW30.evgen.EVNT.e1805/',
			 'mc12_8TeV.147311.Sherpa_CT10_Wmunu_CKKW30_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147312.Sherpa_CT10_Wmunu_MuFdown.evgen.EVNT.e1805/',
			 'mc12_8TeV.147313.Sherpa_CT10_Wmunu_MuFdown_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147314.Sherpa_CT10_Wmunu_MuFup.evgen.EVNT.e1805/',
			 'mc12_8TeV.147315.Sherpa_CT10_Wmunu_MuFup_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147316.Sherpa_CT10_Wmunu_mpi1.evgen.EVNT.e1805/',
			 'mc12_8TeV.147317.Sherpa_CT10_Wmunu_mpi1_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147318.Sherpa_CT10_Wmunu_mpi2.evgen.EVNT.e1805/',
			 'mc12_8TeV.147319.Sherpa_CT10_Wmunu_mpi2_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147320.Sherpa_CT10_Wmunu_Shower1.evgen.EVNT.e1805/',
			 'mc12_8TeV.147321.Sherpa_CT10_Wmunu_Shower1_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147322.Sherpa_CT10_Wmunu_MuRdown.evgen.EVNT.e1805/',
			 'mc12_8TeV.147323.Sherpa_CT10_Wmunu_MuRdown_MjjFilt.evgen.EVNT.e1805/',
			 'mc12_8TeV.147324.Sherpa_CT10_Wmunu_MuRup.evgen.EVNT.e1805/',
			 'mc12_8TeV.147325.Sherpa_CT10_Wmunu_MuRup_MjjFilt.evgen.EVNT.e1805/']

dataset_names = ["129916.Nominal_Sherpa_Signal", "147294.min_n_tchannels_CKKW30", "147295.min_n_tchannels_CKKW30_MjjFilt",
				"147296.min_n_tchannels_MuFdown", "147297.min_n_tchannels_MuFdown_MjjFilt",
				"147298.min_n_tchannels_MuFup", "147299.min_n_tchannels_MuFup_MjjFilt",
				"147300.min_n_tchannels_mpi1", "147301.min_n_tchannels_mpi1_MjjFilt",
				"147302.min_n_tchannels_mpi2", "147303.min_n_tchannels_mpi2_MjjFilt",
				"147304.min_n_tchannels_Shower1", "147305.min_n_tchannels_Shower1_MjjFilt",
				"147306.min_n_tchannels_MuRdown", "147307.min_n_tchannels_MuRdown_MjjFilt",
				"147308.min_n_tchannels_MuRup", "147309.min_n_tchannels_MuRup_MjjFilt",
				"147310.CKKW30", "147311.CKKW30_MjjFilt", "147312.MuFdown", "147313.MuFdown_MjjFilt",
				"147314.MuFup", "147315.MuFup_MjjFilt", "147316.mpi1", "147317.mpi1_MjjFilt",
				"147318.mpi2", "147319.mpi2_MjjFilt", "147320.Shower1", "147321.Shower1_MjjFilt",
				"147322.MuRdown", "147323.MuRdown_MjjFilt", "147324.MuRup", "147325.MuRup_MjjFilt"]
				
exp_hist_list = ["d01-x01-y01", "d01-x01-y02", "d02-x01-y01", "d02-x01-y02",
			"d03-x01-y01", "d03-x01-y02", "d04-x01-y01", "d04-x01-y02",
			"d05-x01-y01", "d05-x01-y02", "d06-x01-y01", "d06-x01-y02",
			"d07-x01-y01", "d07-x01-y02", "d08-x01-y01", "d08-x01-y02",
			"d09-x01-y01", "d09-x01-y02", "d10-x01-y01", "d10-x01-y02",
			"d11-x01-y01", "d11-x01-y02", "d12-x01-y01", "d12-x01-y02",
			"d13-x01-y01", "d13-x01-y02", "d14-x01-y01", "d14-x01-y02",
			"d15-x01-y01", "d15-x01-y02", "d16-x01-y01", "d16-x01-y02",
			"d17-x01-y01", "d17-x01-y02", "d18-x01-y01", "d18-x01-y02",
			"d19-x01-y01", "d19-x01-y02", "d20-x01-y01", "d20-x01-y02",
			"d21-x01-y01", "d21-x01-y02", "d22-x01-y01", "d22-x01-y02",
			"d23-x01-y01", "d23-x01-y02", "d24-x01-y01", "d24-x01-y02",
			"d25-x01-y01", "d25-x01-y02"]
			
hist_list = ["NJetExcl_1", "NJetExcl_2", "RatioNJetExcl_1", "RatioNJetExcl_2", "FirstJetPt_2jet_1", "FirstJetPt_2jet_2",
			"FirstJetPt_3jet_1", "FirstJetPt_3jet_2", "FirstJetPt_4jet_1", "FirstJetPt_4jet_2", "SecondJetPt_2jet_1", "SecondJetPt_2jet_2",
			"SecondJetPt_3jet_1", "SecondJetPt_3jet_2", "SecondJetPt_4jet_1", "SecondJetPt_4jet_2", "ThirdJetPt_3jet_1", "ThirdJetPt_3jet_2",
			"ThirdJetPt_4jet_1", "ThirdJetPt_4jet_2", "FourthJetPt_4jet_1", "FourthJetPt_4jet_2", "Ht_2jet_1", "Ht_2jet_2",
			"Ht_3jet_1", "Ht_3jet_2", "Ht_4jet_1", "Ht_4jet_2", "Minv_2jet_1", "Minv_2jet_2", "Minv_3jet_1", "Minv_3jet_2",
			"Minv_4jet_1", "Minv_4jet_2", "JetRapidity_1", "JetRapidity_2", "DeltaYElecJet_1", "DeltaYElecJet_2", "SumYElecJet_1", "SumYElecJet_2",
			"DeltaR_2jet_1", "DeltaR_2jet_2", "DeltaY_2jet_1", "DeltaY_2jet_2", "DeltaPhi_2jet_1", "DeltaPhi_2jet_2",
			"DijetMass_2jet_1", "DijetMass_2jet_2", "DijetMass_3jet_1", "DijetMass_3jet_2",
			"DijetMass_4jet_1", "DijetMass_4jet_2","AntiDijetMass_2jet_1", "AntiDijetMass_2jet_2",
			"AntiDijetMass_3jet_1", "AntiDijetMass_3jet_2","AntiDijetMass_4jet_1", "AntiDijetMass_4jet_2",
			"ThirdZep_3jet_1", "ThirdZep_3jet_2", "ThirdZep_4jet_1", "ThirdZep_4jet_2", "FourthZep_4jet_1", "FourthZep_4jet_2",
			"AntiDijetEtaDiff_2jet_1", "AntiDijetEtaDiff_2jet_2", "AntiDijetEtaDiff_3jet_1", "AntiDijetEtaDiff_3jet_2",
			"AntiDijetEtaDiff_4jet_1", "AntiDijetEtaDiff_4jet_2", "AntiDijetPhiDiff_2jet_1", "AntiDijetPhiDiff_2jet_2", 
			"AntiDijetPhiDiff_3jet_1", "AntiDijetPhiDiff_3jet_2", "AntiDijetPhiDiff_4jet_1", "AntiDijetPhiDiff_4jet_2"]
			
title_list = 	["Jet Multiplicity (W+#geq 2 jets)", "Jet Multiplicity Ratio", "First Jet p_{T} (W+#geq 2 jets)", "First Jet p_{T} (W+#geq 3 jets)", "First Jet p_{T} (W+#geq 4 jets)",
				"Second Jet p_{T}", "Second Jet p_{T} (W+#geq 3 jets)", "Second Jet p_{T} (W+#geq 4 jets)", "Third Jet p_{T}", "Third Jet p_{T} (W+#geq 4 jets)",
				"Fourth Jet p_{T}", "H_{T} (W+#geq 2 jets)", "H_{T} (W+#geq 3 jets)", "H_{T} (W+#geq 4 jets)", "Jet Invariant Mass (W+ #geq 2 jets)",
				"Jet Invariant Mass (W+ #geq 3 jets)", "Jet Invariant Mass (W+ #geq 4 jets)", "First Jet Rapidity", "Lepton-Jet Rapidity Difference", "Lepton-Jet Rapidity Sum", 
				"#Delta R Distance of Leading Jets", "Rapidity Distance of Leading Jets", "Azimuthal Distance of Leading Jets","Dijet Mass (W+#geq 2 jets)",
				"Dijet Mass (W+#geq 3 jets)", "Dijet Mass (W+#geq 4 jets)", "Most Forward/Rearward Dijet Mass (W+#geq 2 jets)","Most Forward/Rearward Dijet Mass (W+#geq 3 jets)",
				"Most Forward/Rearward Dijet Mass (W+#geq 4 jets)", "Third Jet Pseudorapidity in Dijet CM (W+#geq 3 jets)", "Third Jet Pseudorapidity in Dijet CM (W+#geq 4 jets)",
				"Fourth Jet Pseudorapidity in Dijet CM (W+#geq 4 jets)", "Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 2 jets)",
				"Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 3 jets)", "Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 4 jets)",
				"cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 2 jets)", "cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 3 jets)",
				"cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 4 jets)"]
				
x_axis_list = 	["N_{jet}", "N_{jet}", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]",
				 "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "H_{T} [GeV]", "H_{T} [GeV]", "H_{T} [GeV]",
				 "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "y", "y(Lepton)-y(First Jet)", "y(Lepton)+y(First Jet)",
				 "#Delta R(First Jet, Second Jet)", "#Delta y(First Jet, Second Jet)", "#Delta#phi(First Jet, Second Jet)",
				 "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]",
				 "#eta_{3} (Third Jet)", "#eta_{3} (Third Jet)", "#eta_{4} (Fourth Jet)",
				 "#Delta#eta_{j_1j_2}", "#Delta#eta_{j_1j_2}", "#Delta#eta_{j_1j_2}",
				 "cos|#phi_{j_1}-#phi_{j_2}|", "cos|#phi_{j_1}-#phi_{j_2}|", "cos|#phi_{j_1}-#phi_{j_2}|"]

y_axis_list = 	["#sigma (W+#geq N_{jet} jets) [pb]", "#sigma (#geq N_{jet} jets)/#sigma (#geq N_{jet}-1 jets)",
				 "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
				 "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
				 "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
				 "d#sigma/dH_{T} [pb/GeV]", "d#sigma/dH_{T} [pb/GeV]", "d#sigma/dH_{T} [pb/GeV]",
				 "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]",
				 "d#sigma/d#it{y} [pb]", "d#sigma/d#Delta#it{y} [pb]", "d#sigma/d#Sigma#it{y} [pb]",
				 "d#sigma/d#Delta#it{R} [pb]", "d#sigma/d#Delta#it{y} [pb]", "d#sigma/d#Delta#phi [pb]",
				 "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
				 "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
				 "d#sigma/d#eta_{3} [pb]", "d#sigma/d#eta_{3} [pb]", "d#sigma/d#eta_{4} [pb]",
				 "d#sigma/d#eta_{j_1j_2} [pb]", "d#sigma/d#eta_{j_1j_2} [pb]", "d#sigma/d#eta_{j_1j_2} [pb]",
				 "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]"]
				
y_axis_list_norm = 	["#sigma (W+#geq N_{jet} jets)", "#sigma (#geq N_{jet} jets)/#sigma (#geq N_{jet}-1 jets)",
					 "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
					 "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
					 "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
					 "d#sigma/dH_{T} [events/GeV]", "d#sigma/dH_{T} [events/GeV]", "d#sigma/dH_{T} [events/GeV]",
					 "d#sigma/d#it{m} [events/GeV]","d#sigma/d#it{m} [events/GeV]", "d#sigma/d#it{m} [events/GeV]",
					 "d#sigma/d#it{y} [events]", "d#sigma/d#Delta#it{y} [events]", "d#sigma/d#Sigma#it{y} [events]",
					 "d#sigma/d#Delta#it{R} [events]", "d#sigma/d#Delta#it{y} [events]", "d#sigma/d#Delta#phi [events]",
					 "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]",
					 "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]",
					 "d#sigma/d#eta_{3} [events]", "d#sigma/d#eta_{3} [events]", "d#sigma/d#eta_{4} [events]",
					 "d#sigma/d#eta_{j_1j_2} [events]", "d#sigma/d#eta_{j_1j_2} [events]", "d#sigma/d#eta_{j_1j_2} [events]",
					 "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]"]
			
def StyleHistogram(index, h1):
	index = int(index/2)
	h1.SetTitle(title_list[index])
	h1.GetXaxis().SetTitle(x_axis_list[index])
	h1.GetYaxis().SetTitle(y_axis_list[index])
	h1.SetOption("HIST E")
	
def StyleData(index, h1):
	index = int(index/2)
	h1.SetTitle(title_list[index])
	h1.GetXaxis().SetTitle(x_axis_list[index])
	h1.GetYaxis().SetTitle(y_axis_list[index])
	h1.SetMarkerStyle(20)
	h1.SetMarkerSize(0.9)

#Setup AMIClient.	
#This works only on my laptop, otherwise you need to run 'ami auth'
client = AMIClient()
if not os.path.exists(AMI_CONFIG):
	create_auth_config()
client.read_config(AMI_CONFIG)

if os.path.exists("Exp_Data_arXiv12011276.root") == True:
	hf.mkdir("Exp_Data_2012")
	hf.cd("Exp_Data_2012")
	exp_data = ROOT.TFile.Open("Exp_Data_arXiv12011276.root")
	for index, hist in enumerate(exp_hist_list):
		histogram = exp_data.Get(hist)
		hf.cd("Exp_Data_2012")
		StyleData(index, histogram)
		histogram.Write()
		del histogram
	exp_data.Close()
	hf.cd()


#Folder names must be the same as in the dataset_names list
#I could try to get the script to just to check for run number in folder name (do this later)
#Root file needs to be named after the dataset run number
#for folder in dataset_names:
for folder, data in zip(dataset_names, datasets):
	if os.path.exists(folder+"/") == True:
		#First get the crossSection_mean and GenFiltEff_mean for this dataset from AMI for normalizations
		xsec, effic = get_dataset_xsec_effic(client, data)
		xsec = 1000*xsec*effic #Converts nb to pb and applies GenFiltEff
		print xsec, effic
		
		#histogram manipulation and such
		os.chdir(folder+"/")
		hf.mkdir(folder)
		hf.cd(folder)
		ROOT.gDirectory.mkdir("Normalized")
		file_name = folder.split('.')
		file_name = file_name[0]
		root_file = ROOT.TFile.Open(file_name+".root")
		for index, hist in enumerate(hist_list):
			histogram = root_file.Get(hist)
			hf.cd(folder)
			StyleHistogram(index, histogram)
			histogram.Write()
			# Clone root histograms, normalize to area, and move to Normalized directory
			histogram_norm = histogram.Clone(hist+"_norm")
			#histogram_norm.GetYaxis().SetTitle("(1/N) "+y_axis_list_norm[int(index/2)])
			histogram_norm.GetYaxis().SetTitle("(1/#sigma) "+y_axis_list_norm[int(index/2)])
			histogram_norm.Scale(1/xsec)
			ROOT.gDirectory.cd("Normalized")
			histogram_norm.Write()
			ROOT.gDirectory.cd()
			del histogram_norm
		root_file.Close()
		hf.cd()
		os.chdir("..")
	else:
		continue

hf.Write()
hf.Close()
print "Job Complete!!!"