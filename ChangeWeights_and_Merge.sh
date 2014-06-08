#!/bin/bash

ln -s ~/Desktop/HEP/VBF_W/PythonScripts/changeEventWeight.py .

python changeEventWeight.py
wait

#for folder in "MuFdown" "MuFup" "MuRdown" "MuRup" "MuRdownMuFdown" "MuRupMuFup" "NNPDF23_as_118" "CT10as" "MSTW2008nlo68cl" "MSTW2008nlo90cl"
for folder in "NNPDF23_as_118" "CT10as" "MSTW2008nlo68cl" "MSTW2008nlo90cl"
do
  cd ${folder}
  ln -s ~/Desktop/HEP/VBF_W/PythonScripts/mergeLHE.py .
  python mergeLHE.py
  mv outfile.lhe ${folder}.lhe
  mv ${folder}.lhe ..
  cd ..
  rm -r ${folder}
  lhef2hepmc ${folder}.lhe ${folder}.hepmc
done