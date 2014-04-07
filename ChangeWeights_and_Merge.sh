#!/bin/bash

ln -s ~/Desktop/HEP/VBF_W/PythonScripts/changeEventWeight.py .

python changeEventWeight.py
wait

for folder in "MuFdown" "MuFup" "MuRdown" "MuRup" "MuRdownMuFdown" "MuRupMuFup"; do
  cd ${folder}
  ln -s ~/Desktop/HEP/VBF_W/PythonScripts/mergeLHE.py .
  python mergeLHE.py
  mv outfile.lhe ${folder}.lhe
  mv ${folder}.lhe ..
  cd ..
  rm -r ${folder}
  lhef2hepmc ${folder}.lhe ${folder}.hepmc
done