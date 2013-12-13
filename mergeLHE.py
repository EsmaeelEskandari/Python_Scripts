import glob

# TODO: add the capabality to choose between
#           globbing all lhe files
#           inputting specific files by hand
#       add the capability to name output file

filenames = glob.glob('*.events')

with open('./outfile.lhe', 'w') as outfile:
    numEvents = 0
    outfile.write("""<LesHouchesEvents version="1.0">\n""")
    with open(filenames[0]) as toGetHeader:
        writeHeader = False
        for line in toGetHeader:
            if "<!--" in line: writeHeader = True
            if "</init>" in line:
                outfile.write(line)
                break
            if writeHeader: outfile.write(line)
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
    
print "There were %s events processed in %s files." %numEvents, len(filenames)