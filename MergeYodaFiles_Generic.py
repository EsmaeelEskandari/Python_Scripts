import glob
import os, subprocess

YodaFiles = glob.glob("*.yoda*")
Yoda_Files = []
# yodamerge does not like file names ending with .yoda.#
proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
(pwd,err) = proc.communicate()
print pwd.strip()
for file in YodaFiles:
    fileName, fileExt = os.path.splitext(pwd.strip()+'/'+file)
    if fileExt != ".yoda":
        os.rename(file,fileName)
        Yoda_Files.append(fileName)
    else: Yoda_Files.append(file)
del YodaFiles
i = len(Yoda_Files)
print "There were {0} in the directory: {1}".format(i,current_dir)

# Run yodamerge.py over every file in the Yoda_Files list.
arguments = "%s" % " ".join(map(str, Yoda_Files))
cmd = "yodamerge -o merged.yoda "+arguments
os.system(cmd)
		
# Remove the merged.yoda file in case the script fails.
# This keeps you from having to delete them by hand before re-running script.
os.system("mv merged.yoda merged.save")