
for file in glob.glob('./*.lhe'):
  num = 0
  with open(file) as f:
    for line in f:
      if '<event>' in line: num += 1
  print file+" has "+str(num)+" events in it."