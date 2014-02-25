#!/bin/bash

for folder in "MuFdown" "MuFup" "MuRdown" "MuRup" "MuRdownMuFdown" "MuRupMuFup"; 
do
  echo $folder
  cd $folder
#  mv Wminus_${folder}.events Wminus_${folder}.lhe
  lhef2hepmc Wplus_${folder}.events Wplus_${folder}.hepmc
  wait
  cd ..
done
