#TODO: Add a scale factor check.

import glob, os
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-x", "--xsecup", dest="xSection", default="-1.00", help="Manually set the cross-section (pb) in LHE files (default is -1.0). This adjusts the original file and is only needed if the LHE file has -1.0 where the cross-section should be.")
parser.add_option("-e", "--xerrup", dest="xsErr", default="-1.00", help="Manually set the cross-section error (pb) in LHE files (default is -1.0). This adjusts the original file and is only needed if the LHE file has -1.0 where the cross-section error should be.")
(options, args) = parser.parse_args()

xSec = '%.5E' % float(options.xSection) # Convert it to string and in scientific notation
xErr = '%.5E' % float(options.xsErr)
if float(options.xSection) != -1.00: setXS = True
else: setXS = False
print "Set Cross-section: {0}. Current value: {1}".format(setXS, options.xSection)

#filenames = ["powheg.events"]
filenames = glob.glob("*.lhe")
file_root_names = [os.path.splitext(name)[0] for name in filenames]

def getTheWeights(eventBlock):
    numParticles = int(eventBlock[1][0])
    currWeight = eventBlock[1][2]
    renfact = []
    facfact = []
    weight = []
    for i in range(numParticles+4,numParticles+16):
        sci_not = '%.5E' % float(eventBlock[i][2])
        weight.append(sci_not)
        renfact.append(eventBlock[i][3])
        facfact.append(eventBlock[i][4])
    
    return renfact, facfact, weight, currWeight
    
dir_names = ["MuRdownMuFdown", "MuFdown", "MuRdown", "MuFup", "MuRup", "MuRupMuFup",
             "NNPDF23_as_118", "CT10as_113", "MSTW2008nlo68cl", "MSTW2008nlo90cl",
             "CT10_117", "CT10_119"]
             
for dir_name in dir_names[10:]:
    if not os.path.exists("./"+dir_name):
        os.mkdir("./"+dir_name)

for name_index,fname in enumerate(filenames):
    numEvents = 0
    eventLine = 0
    with open(fname) as infile:
        eventBlock = []
        allNewWeights = []
        allCurrWeights = []
        allRenFacts = []
        allFacFacts = []
        getWeights = False
        if setXS:
            with open("./"+fname+".1", "w") as new_infile:
                initLine = 0
                for index,line in enumerate(infile):
                    changeWeights = False
                    if setXS:
                        newline = line
                        if "<init>" in line: 
                            initLine = index
                        if index == initLine+2:
                            newline = line.replace("-1.00000E+00",xSec,1)
                            newline = newline.replace("-1.00000E+00",xErr,1)
                        new_infile.write(newline)
                    if "<event>" in line: 
                        numEvents += 1
                        getWeights = True
                        changeWeights = False
                        eventLine = index
                        eventBlock = []
                    if "</event>" in line: 
                        getWeights = False
                        changeWeights = True
                    if getWeights:
                        eventBlock.append(line.split())
                    if changeWeights: 
                        renfact, facfact, weight, currWeight = getTheWeights(eventBlock)
                        allNewWeights.append(weight)
                        allCurrWeights.append(currWeight)
                        allRenFacts.append(renfact)
                        allFacFacts.append(facfact)
        else:
            for index,line in enumerate(infile):
                changeWeights = False
                if "<event>" in line: 
                    numEvents += 1
                    getWeights = True
                    changeWeights = False
                    eventLine = index
                    eventBlock = []
                if "</event>" in line: 
                    getWeights = False
                    changeWeights = True
                if getWeights:
                    eventBlock.append(line.split())
                if changeWeights: 
                    renfact, facfact, weight, currWeight = getTheWeights(eventBlock)
                    allNewWeights.append(weight)
                    allCurrWeights.append(currWeight)
                    allRenFacts.append(renfact)
                    allFacFacts.append(facfact)
    if setXS: os.rename(fname+".1",fname)
    
    for j,folder in enumerate(dir_names):
        print "Working on file: {0}".format(fname)
        infile = open(fname)
        with open("./"+folder+"/"+file_root_names[name_index]+".lhe", "w") as out_file:
            numEvents = 0
            for index,line in enumerate(infile):
                if "<event>" in line:
                    numEvents += 1
                    eventLine = index
                if "#new" not in line:
                    newline = line
                    if index == eventLine+1:
                        newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][j])
                    out_file.write(newline)
        infile.close()
                
    # infile = open(fname)    
    # with open("./MuRdownMuFdown/"+file_root_names[name_index]+".lhe", "w") as out_MuRMuFdown:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][0])
    #             out_MuRMuFdown.write(newline)
    # infile.close()
    #         
    # infile = open(fname)
    # with open("./MuFdown/"+file_root_names[name_index]+".lhe", "w") as out_MuFdown:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line: 
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][1])
    #             out_MuFdown.write(newline)
    # infile.close()
    #         
    # infile = open(fname)
    # with open("./MuRdown/"+file_root_names[name_index]+".lhe", "w") as out_MuRdown:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][2])
    #             out_MuRdown.write(newline)
    # infile.close()
    #     
    # infile = open(fname)    
    # with open("./MuFup/"+file_root_names[name_index]+".lhe", "w") as out_MuFup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][3])
    #             out_MuFup.write(newline)
    # infile.close()
    #  
    # infile = open(fname)       
    # with open("./MuRup/"+file_root_names[name_index]+".lhe", "w") as out_MuRup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][4])
    #             out_MuRup.write(newline)
    # infile.close()
    # 
    # infile = open(fname)        
    # with open("./MuRupMuFup/"+file_root_names[name_index]+".lhe", "w") as out_MuRMuFup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][5])
    #             out_MuRMuFup.write(newline)
    # infile.close()
    #
    # infile = open(fname)
    # with open("./NNPDF23_as_118/"+file_root_names[name_index]+".lhe", "w") as out_MuRMuFup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][6])
    #             out_MuRMuFup.write(newline)
    # infile.close()
    #
    # infile = open(fname)
    # with open("./CT10as_113/"+file_root_names[name_index]+".lhe", "w") as out_MuRMuFup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][7])
    #             out_MuRMuFup.write(newline)
    # infile.close()
    #
    # infile = open(fname)
    # with open("./MSTW2008nlo68cl/"+file_root_names[name_index]+".lhe", "w") as out_MuRMuFup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][8])
    #             out_MuRMuFup.write(newline)
    # infile.close()
    #
    # infile = open(fname)
    # with open("./MSTW2008nlo90cl/"+file_root_names[name_index]+".lhe", "w") as out_MuRMuFup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][9])
    #             out_MuRMuFup.write(newline)
    # infile.close()
    #
    # infile = open(fname)
    # with open(".//"+file_root_names[name_index]+".lhe", "w") as out_MuRMuFup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][7])
    #             out_MuRMuFup.write(newline)
    # infile.close()
    #
    # infile = open(fname)
    # with open("./CT10_119/"+file_root_names[name_index]+".lhe", "w") as out_MuRMuFup:
    #     numEvents = 0
    #     for index,line in enumerate(infile):
    #         if "<event>" in line:
    #             numEvents += 1
    #             eventLine = index
    #         if "#new" not in line:
    #             newline = line
    #             if index == eventLine+1:
    #                 newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][7])
    #             out_MuRMuFup.write(newline)
    # infile.close()