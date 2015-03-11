import glob
import os, subprocess
from optparse import OptionParser
from Aux_Functions import *

parser = OptionParser(usage="%prog <options>")
parser.add_option("-s", "--skip-merged",
                  action="store_true", dest="skipMerged", default=False,
                  help="Skip the folders that already have merged yoda files.")
opts, args = parser.parse_args()

dataset_names = GetListDataset('dataset_names')
dataset_number = GetListDataset('dataset_number')
powheg_w2jet_list = ['000001','000002','000003','000004','000005','000006','000007']
powheg_w2jet_list_7TeV = ['000008','000009','000010','000011','000012','000013','000014']
powheg_vbfw_list  = ['000015','000016','000017','000018','000019','000020','000021']
powheg_vbfw_list_7TeV  = ['000022','000023','000024','000025','000026','000027','000028']
powheg_dict = dict(zip(dataset_number, dataset_names))

# Make a list of yoda files available in the current directory
for folder in dataset_names:
    current_dir = folder+"/"
    if os.path.exists(current_dir) != True: continue
    file_name = folder.split('.')[0]
    
    os.chdir(current_dir)
    if opts.skipMerged:
        file_exists = os.path.isfile(file_name+".root")
        if file_exists:
            os.chdir("..")
            continue
        
    YodaFiles = glob.glob("*.yoda*")
    Yoda_Files = []
    # yodamerge does not like file names ending with .yoda.#
    for file in YodaFiles:
        splitFile = file.split(".")
        if splitFile[-1] not "yoda":
            Yoda_Files.append(".".join(splitFile))
        else: Yoda_Files.append(file)
    del YodaFiles
    i = len(Yoda_Files)
    print "There were {0} in the directory: {1}".format(i,current_dir)

    if file_name in powheg_w2jet_list:
        dest_Wpm = file_name
        source_Wm = str(int(file_name) + 185695)
        source_Wp = str(int(source_Wm) + 7)
        source_Wm_dir = powheg_dict[source_Wm]
        source_Wp_dir = powheg_dict[source_Wp]
        cmd = "cp ../{0}/merged.save ./merged_Wm.yoda".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged.save ./merged_Wp.yoda".format(source_Wp_dir)
        os.system(cmd)
        os.system("yodamerge -o merged.yoda merged_Wm.yoda merged_Wp.yoda")
    elif file_name in powheg_vbfw_list:
        dest_Wpm = file_name
        source_Wm = str(int(file_name) + 185834)
        source_Wp = str(int(source_Wm) + 7)
        source_Wm_dir = powheg_dict[source_Wm]
        source_Wp_dir = powheg_dict[source_Wp]
        cmd = "cp ../{0}/merged.save ./merged_Wm.yoda".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged.save ./merged_Wp.yoda".format(source_Wp_dir)
        os.system(cmd)
        os.system("yodamerge -o merged.yoda merged_Wm.yoda merged_Wp.yoda")
    elif file_name in powheg_w2jet_list_7TeV:
        dest_Wpm = file_name
        source_Wm = str(int(file_name) + 185924)
        source_Wp = str(int(source_Wm) + 7)
        source_Wm_dir = powheg_dict[source_Wm]
        source_Wp_dir = powheg_dict[source_Wp]
        cmd = "cp ../{0}/merged.save ./merged_Wm.yoda".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged.save ./merged_Wp.yoda".format(source_Wp_dir)
        os.system(cmd)
        os.system("yodamerge -o merged.yoda merged_Wm.yoda merged_Wp.yoda")
    elif file_name in powheg_vbfw_list_7TeV:
        dest_Wpm = file_name
        source_Wm = str(int(file_name) + 185926)
        source_Wp = str(int(source_Wm) + 7)
        source_Wm_dir = powheg_dict[source_Wm]
        source_Wp_dir = powheg_dict[source_Wp]
        cmd = "cp ../{0}/merged.save ./merged_Wm.yoda".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged.save ./merged_Wp.yoda".format(source_Wp_dir)
        os.system(cmd)
        os.system("yodamerge -o merged.yoda merged_Wm.yoda merged_Wp.yoda")
    elif file_name == "000029":
        source_Wm = "185836"
        source_Wp = "185837"
        source_Wm_dir = powheg_dict[source_Wm]
        source_Wp_dir = powheg_dict[source_Wp]
        cmd = "cp ../{0}/merged.save ./merged_Wm.yoda".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged.save ./merged_Wp.yoda".format(source_Wp_dir)
        os.system(cmd)
        os.system("yodamerge -o merged.yoda merged_Wm.yoda merged_Wp.yoda")
    elif file_name == "000030":
        source_Wm = "185847"
        source_Wp = "185848"
        source_Wm_dir = powheg_dict[source_Wm]
        source_Wp_dir = powheg_dict[source_Wp]
        cmd = "cp ../{0}/merged.save ./merged_Wm.yoda".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged.save ./merged_Wp.yoda".format(source_Wp_dir)
        os.system(cmd)
        os.system("yodamerge -o merged.yoda merged_Wm.yoda merged_Wp.yoda")
    elif file_name == "000031":
        source_Wm = "185930"
        source_Wp = "185931"
        source_Wm_dir = powheg_dict[source_Wm]
        source_Wp_dir = powheg_dict[source_Wp]
        cmd = "cp ../{0}/merged.save ./merged_Wm.yoda".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged.save ./merged_Wp.yoda".format(source_Wp_dir)
        os.system(cmd)
        os.system("yodamerge -o merged.yoda merged_Wm.yoda merged_Wp.yoda")
    elif file_name == "000032":
        source_Wm = "185946"
        source_Wp = "185947"
        source_Wm_dir = powheg_dict[source_Wm]
        source_Wp_dir = powheg_dict[source_Wp]
        cmd = "cp ../{0}/merged.save ./merged_Wm.yoda".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged.save ./merged_Wp.yoda".format(source_Wp_dir)
        os.system(cmd)
        os.system("yodamerge -o merged.yoda merged_Wm.yoda merged_Wp.yoda")
    else:
        if not Yoda_Files: continue
        # Run yodamerge.py over every file in the Yoda_Files list.
        arguments = "%s" % " ".join(map(str, Yoda_Files))
        cmd = "yodamerge -o merged.yoda "+arguments
        os.system(cmd)
		
    # Convert merged.yoda file to merged.root file and rename to dataset
    # run number (found from the folder name).
    y2r_cmd = ["yoda2root","merged.yoda"]
    try:
        subprocess.call(["yoda2root","merged.yoda"])
        cmd = "mv merged.root "+file_name+".root"
        os.system(cmd)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print "File {0} in {1} doesn't exist!".format(y2r_cmd,folder)
        else:
            print """Command '{0}' not found!!!""".format(y2r_cmd[0])
            raise
		
    # Remove the merged.yoda file in case the script fails.
    # This keeps you from having to delete them by hand before re-running script.
    os.system("mv merged.yoda merged.save")
	
    # Prepare for next folder
    os.chdir("..")
