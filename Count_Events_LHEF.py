import glob

total = []
for file in glob.glob('./*.lhe'):
  num = 0
  with open(file) as f:
    for line in f:
      if '<event>' in line: num += 1
  total.append(num)
  print file+" has "+str(num)+" events in it."
  
print "Total number of events in given files: %i" % sum(total)