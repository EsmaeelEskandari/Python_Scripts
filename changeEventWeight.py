#TODO: Add a scale factor check.

import glob, os

#filenames = ["powheg.events"]
filenames = glob.glob("*.events")
file_root_names = [os.path.splitext(name)[0] for name in filenames]

def getTheWeights(eventBlock):
    numParticles = int(eventBlock[1][0])
    currWeight = eventBlock[1][2]
    renfact = []
    facfact = []
    weight = []
    for i in range(numParticles+4,numParticles+10):
        sci_not = '%.5E' % float(eventBlock[i][2])
        weight.append(sci_not)
        renfact.append(eventBlock[i][3])
        facfact.append(eventBlock[i][4])
    
    return renfact, facfact, weight, currWeight
    
dir_names = ["MuRdownMuFdown", "MuFdown", "MuRdown", "MuFup", "MuRup", "MuRupMuFup"]
for dir_name in dir_names:
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
    
    infile = open(fname)    
    with open("./MuRdownMuFdown/"+file_root_names[name_index]+"_MuRdownMuFdown.events", "w") as out_MuRMuFdown:
        numEvents = 0
        for index,line in enumerate(infile):
            if "<event>" in line:
                numEvents += 1
                eventLine = index
            if "#new" not in line:
                newline = line
                if index == eventLine+1:
                    newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][0])
                out_MuRMuFdown.write(newline)
    infile.close()
            
    infile = open(fname)
    with open("./MuFdown/"+file_root_names[name_index]+"_MuFdown.events", "w") as out_MuFdown:
        numEvents = 0
        for index,line in enumerate(infile):
            if "<event>" in line: 
                numEvents += 1
                eventLine = index
            if "#new" not in line:
                newline = line
                if index == eventLine+1:
                    newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][1])
                out_MuFdown.write(newline)
    infile.close()
            
    infile = open(fname)
    with open("./MuRdown/"+file_root_names[name_index]+"_MuRdown.events", "w") as out_MuRdown:
        numEvents = 0
        for index,line in enumerate(infile):
            if "<event>" in line:
                numEvents += 1
                eventLine = index
            if "#new" not in line:
                newline = line
                if index == eventLine+1:
                    newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][2])
                out_MuRdown.write(line)
    infile.close()
        
    infile = open(fname)    
    with open("./MuFup/"+file_root_names[name_index]+"_MuFup.events", "w") as out_MuFup:
        numEvents = 0
        for index,line in enumerate(infile):
            if "<event>" in line:
                numEvents += 1
                eventLine = index
            if "#new" not in line:
                newline = line
                if index == eventLine+1:
                    newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][3])
                out_MuFup.write(line)
    infile.close()
     
    infile = open(fname)       
    with open("./MuRup/"+file_root_names[name_index]+"_MuRup.events", "w") as out_MuRup:
        numEvents = 0
        for index,line in enumerate(infile):
            if "<event>" in line:
                numEvents += 1
                eventLine = index
            if "#new" not in line:
                newline = line
                if index == eventLine+1:
                    newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][4])
                out_MuRup.write(line)
    infile.close()
    
    infile = open(fname)        
    with open("./MuRupMuFup/"+file_root_names[name_index]+"_MuRupMuFup.events", "w") as out_MuRMuFup:
        numEvents = 0
        for index,line in enumerate(infile):
            if "<event>" in line:
                numEvents += 1
                eventLine = index
            if "#new" not in line:
                newline = line
                if index == eventLine+1:
                    newline = line.replace(allCurrWeights[numEvents-1],allNewWeights[numEvents-1][5])
                out_MuRMuFup.write(line)
    infile.close()
