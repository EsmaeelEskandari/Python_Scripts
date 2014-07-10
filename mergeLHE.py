import glob
from datetime import datetime

# TODO: add the capabality to choose between
#           globbing all lhe files
#           inputting specific files by hand
#       add the capability to name output file

parser.add_option("-s", "--save_loc", type="string", dest="save_loc", default=".", help="Rebin override: forces scirpt to rebin using given number.")
(options, args) = parser.parse_args()

#filenames = glob.glob('*.events')
filenames = glob.glob('*.lhe')
startTime = datetime.now()
save_location = options.save_loc

with open(save_location+'/outfile.lhe', 'w') as outfile:
    numEvents = 0
    outfile.write("""<LesHouchesEvents version="1.0">\n""")
    with open(filenames[0]) as toGetHeader:
        writeHeader = False
        for line in toGetHeader:
            if "<!--" in line: writeHeader = True
            if writeHeader: outfile.write(line)
            if "</init>" in line:
                break
    for fname in filenames:
        writeLine = False
        stopWrite = False
        with open(fname) as infile:
            for line in infile:
                if "<event>" in line:
                    numEvents += 1
                    writeLine = True
                if "</LesHouchesEvents>" in line:
                    stopWrite = True
                if writeLine and not stopWrite:
                    outfile.write(line)
    outfile.write("</LesHouchesEvents>")
    
print "There were {0} events processed in {1} files.".format(numEvents, len(filenames))
print(datetime.now()-startTime)