import random
import time
import sys
import os
import glob
from multiprocessing import Pool, cpu_count

outputFilename = "testFinal"
maxFiles = 50
nProcs = cpu_count()

def doMerge(nTuple):
  inList,stage,uniqueID = nTuple
  outputName = "output-st{0}-{1}.yoda".format(stage,uniqueID)
  inputName = " ".join(inList)
  cmd = "yodamerge -o {0} {1}".format(outputName,inputName)
  os.system( cmd )
  return outputName
  
if __name__ == '__main__':
  
  #mark the start time
  startTime = time.time()

  #Creat list of lists of yoda files
  stage = 0
  yodaFiles = glob.glob("*.yoda")
  totFiles = len(yodaFiles)
  numSplits = int( totFiles/maxFiles )+1
  listOfYodaLists = []
  for i in range(numSplits):
    listOfYodaLists.append( yodaFiles[i*maxFiles:(i+1)*maxFiles] )

  intermediateFiles = []
  tasks = [ (x,stage,n) for n,x in enumerate(listOfYodaLists) ]
  while totFiles > 1:
    #create a process Pool with 4 processes
    pool = Pool(processes=nProcs)
    #map doWork to availble Pool processes
    results = pool.map(doMerge, tasks)
    intermediateFiles += results

    # Recreate list of yodaFiles with next stage of merged files
    totFiles = len(results)
    numSplits = int( totFiles/maxFiles )+1
    listOfYodaLists = []
    for i in range(numSplits):
      listOfYodaLists.append( results[i*maxFiles:(i+1)*maxFiles] )
    stage += 1
    tasks = [ (x,stage,n) for n,x in enumerate(listOfYodaLists) ]
    finalOutputFile = results[0]
  
  # Rename last file to outputName
  os.rename(finalOutputFile, outputFilename+".yoda")
  intermediateFiles.remove(finalOutputFile)
  # Delete intermediate files
  for file in intermediateFiles:
    os.remove(file)

  #calculate the total time it took to complete the work
  workTime =  time.time() - startTime

  #print results
  print "The job took {0} seconds to complete for {1} parallel processes".format(workTime, nProcs)