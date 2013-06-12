import glob
import os

dataset_names = ["129916.Nominal_Sherpa", "147294.min_n_tchannels_CKKW30", "147295.min_n_tchannels_CKKW30_MjjFilt",
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

# Make a list of Aida files available in the current directory
for folder in dataset_names:
	current_dir = folder+"/"
	if os.path.exists(current_dir) == True:
		os.chdir(current_dir)
		Aida_Files = glob.glob("*.aida")
		i = len(Aida_Files)
		print "There were %i in the directory: "%i + current_dir

		# Run aidamerge.py over every file in the Aida_Files list.
		arguments = "%s" % " ".join(map(str, Aida_Files))
		cmd = "python ../aidamerge.py "+arguments
		os.system(cmd)
		
		# Convert merged.aida file to merged.root file and rename to dataset
		# run number (found from the folder name).
		os.system("aida2root merged.aida")
		file_name = folder.split('.')
		file_name = file_name[0]
		cmd = "mv merged.root "+file_name+".root"
		os.system(cmd)
		
		# Remove the merged.aida file in case the script fails.
		# This keeps you from having to delete them by hand before re-running script.
		os.system("rm merged.aida")
		
		# Prepare for next folder
		os.chdir("..")
		Aida_Files = []
	else:
		continue