import sys,glob,os

platform = sys.platform

for file in glob.glob("*.lhe"):
  line_number = 0
  for line in reversed(open(file).readlines()):
    if "</event>" in line:
      break
    else:
      line_number += 1
  new_file = file+".new"
  if line_number <= 1: continue
  if platform == "darwin":
    cmd = "ghead -n -"+str(line_number)+" "+file+" > "+new_file+" && mv "+new_file+" "+file
  else:
    cmd = "head -n -"+str(line_number)+" "+file+" > "+new_file+" && mv "+new_file+" "+file
  print cmd
  os.system(cmd)
