#!/bin/bash

for i in $( ls *.lhe ); 
do
  echo $i
  lhef2hepmc $i $i.hepmc
  wait
done
