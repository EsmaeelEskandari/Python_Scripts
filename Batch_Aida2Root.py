import glob
import os
import ROOT

hist_list = ["d01-x01-y01", "d01-x01-y02", "d02-x01-y01", "d02-x01-y02",
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
			"d25-x01-y01", "d25-x01-y02", "DijetMass_2jet_1", "DijetMass_2jet_2",
			"DijetMass_3jet_1", "DijetMass_3jet_2", "DijetMass_4jet_1", "DijetMass_4jet_2",
			"AntiDijetMass_2jet_1", "AntiDijetMass_2jet_2", "AntiDijetMass_3jet_1", "AntiDijetMass_3jet_2",
			"AntiDijetMass_4jet_1", "AntiDijetMass_4jet_2", "ThirdZep_3jet_1", "ThirdZep_3jet_2",
			"ThirdZep_4jet_1", "ThirdZep_4jet_2", "FourthZep_4jet_1", "FourthZep_4jet_2",
			"AntiDijetEtaDiff_2jet_1", "AntiDijetEtaDiff_2jet_2", "AntiDijetEtaDiff_3jet_1", "AntiDijetEtaDiff_3jet_2",
			"AntiDijetEtaDiff_4jet_1", "AntiDijetEtaDiff_4jet_2", "AntiDijetPhiDiff_2jet_1", "AntiDijetPhiDiff_2jet_2", 
			"AntiDijetPhiDiff_3jet_1", "AntiDijetPhiDiff_3jet_2", "AntiDijetPhiDiff_4jet_1", "AntiDijetPhiDiff_4jet_2"]

dataset_names = ["147294.min_n_tchannels_CKKW30", "147295.min_n_tchannels_CKKW30_MjjFilt",
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
				
# Get rid of all the current root files (Clean the slate!)
os.system('find . -name \*.root -exec rm -rf {} \;')
				
# Time to merge some files!
for folder in dataset_names:
	folder = folder+"/"
	root_file_list = []
	if os.path.exists(folder) == True:
		os.chdir(folder)
		Aida_Files = glob.glob("*.aida")
		
		# Run aida2root over every file in Aida_Files list.
		for aida in Aida_Files:
			cmd = 'aida2root '+aida
			os.system(cmd)
			aida = os.path.splitext(aida)
			root_file = aida[0]+".root"
			root_file_list.append(root_file)
		
		# Merge Root files (use hadd?)
		arguments = "%s" % " ".join(map(str, root_file_list))
		file_name = folder.split('.')
		cmd = "hadd -f "+file_name[0]+".root "+arguments
		os.system(cmd)
		
		# Need to divide histograms by number of merged files to make average...
		# This may not be right, considering the average should be done bin-by-bin
		# and each bin may not have same number of points...
		merged_root = ROOT.TFile(file_name[0]+".root", 'UPDATE')
		for hist in hist_list:
			histogram = merged_root.Get(hist)
			histogram.Scale(1.0/float(len(root_file_list)))
			histogram.Write('',ROOT.TObject.kOverwrite)
		#merged_root.Write()	
		merged_root.Close()
		
		
		# Prepare for next folder	
		os.chdir("..")
		Aida_Files = []
			
	else:
		continue