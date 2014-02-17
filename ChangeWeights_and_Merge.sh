#!/bin/bash

ln -s ~/Desktop/HEP/WZ+Jets/PythonScripts/changeEventWeight.py .

python changeEventWeight.py
wait

for folder in "MuFdown" "MuFup" "MuRdown" "MuRup" "MuRdownMuFdown" "MuRupMuFup"; do
  cd ${folder}
  ln -s ~/Desktop/HEP/WZ+Jets/PythonScripts/mergeLHE.py .
  python mergeLHE.py
  mv outfile.lhe ${folder}.lhe
  mv ${folder}.lhe ..
  cd ..
  rm -r ${folder}
done