import glob, os, math
import numpy as np

filenames = glob.glob("*.lhe")
file_root_names = [os.path.splitext(name)[0] for name in filenames]

def getTheWeights(eventBlock):
    numParticles = int(eventBlock[1][0])
    currWeight = float(eventBlock[1][2])
    weight = []
    weight.append(currWeight)
    for i in range(numParticles+4,numParticles+14):
        weight.append(float(eventBlock[i][2]))
    
    return weight
	
numEvents = 0
acc_weight = np.zeros((11,), dtype=np.float64)
acc_weight_sqr = np.zeros((11,), dtype=np.float64)
xsecval = np.zeros((11,), dtype=np.float64)
xsecerr = np.zeros((11,), dtype=np.float64)
xsecerr2 = np.zeros((11,), dtype=np.float64)

shifts = ["Nominal", "MuRFdown", "MuFdown", "MuRdown", "MuFup", "MuRup", "MuRFup",
          "NNPDF23_as_118", "CT10as", "MSTW2008nlo68cl", "MSTW2008nlo90cl"]

for name_index,fname in enumerate(filenames):
    with open(fname) as infile:
        eventBlock = []
        getWeights = False
        for index,line in enumerate(infile):
            changeWeights = False
            if "<event>" in line: 
                numEvents += 1
                if (numEvents % 25000 == 0): print "Processed {0} events!".format(numEvents)
                getWeights = True
                changeWeights = False
                eventBlock = []
            if "</event>" in line: 
                getWeights = False
                changeWeights = True
            if getWeights:
                eventBlock.append(line.split())
            if changeWeights: 
                weights = getTheWeights(eventBlock)
                
                # weights = ["Nominal", "MuRFdown", "MuFdown", "MuRdown", "MuFup", "MuRup", "MuRFup",
                #           "NNPDF23_as_118", "CT10as", "MSTW2008nlo68cl", "MSTW2008nlo90cl"]
                for i in range(11):
                    acc_weight[i] += np.float64(weights[i])
                    acc_weight_sqr[i] += np.float64(weights[i])*np.float64(weights[i])
                
                    xsecval[i] = acc_weight[i]/np.float64(numEvents)
                    xsecerr2[i] = (acc_weight_sqr[i]/np.float64(numEvents) - xsecval[i]*xsecval[i])/np.float64(numEvents)
                    if xsecerr2[i] < 0: 
                        print "{0} XS error2 was < 0.0, forcing it to 0.0.".format(shifts[i])
                        xsecerr2[i] = 0.0
                    xsecerr[i] = math.sqrt(xsecerr2[i])

for i in range(11):
    print "Estimated {0} cross-section = {1} +- {2} pb. Calculated from {3} events.".format(shifts[i],xsecval[i],xsecerr[i],numEvents)
                