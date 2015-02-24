import sys, os
import glob
import optparse

pwd = os.getcwd()

# define options
# ==============
optParser = optparse.OptionParser(usage=__doc__,conflict_handler="resolve")
optParser.add_option('-s', '--scope', action='store',type='string', dest='scopeName',
                  default='user.cjohnson', help='Set the scope in which to look for DIDs.')
optParser.add_option('-d', '--dir', action='store',type='string', dest='outDir',
                  default=pwd, help='Set the download directory')
optParser.add_option('-F', '--list', action='store_true',dest='fileList')

# parse options and args
options, args = optParser.parse_args()

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

if options.fileList:
    if len(args) > 1:
        print "Only provide one list of DIDs:"
        print "./rucioDownload [options] -F fileList"
        sys.exit()
    DIDs_to_download = open(args[0]).readlines()
else: DIDs_to_download = args

for DID in DIDs_to_download:
    #remove trailing "\n" and "/"
    DID = DID.strip("\n")
    DID = DID.strip("/")
    
    #ensure there is not a scope already defined
    splitDID = DID.split(":")
    if len(splitDID) == 1: formatedDID = splitDID[0]
    else: formatedDID = splitDID[1]
    
    outputDir = options.outDir+"/"+formatedDID+"/"
    ensure_dir(outputDir)
    cmd = "rucio download --dir={0} {1}:{2}".format(outputDir,options.scopeName,formatedDID)
    os.system(cmd)
    