import glob, os

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