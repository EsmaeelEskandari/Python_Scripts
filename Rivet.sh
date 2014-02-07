#!/bin/bash

for hepmc in $( ls *.hepmc ); do
	rivet -a WJETS_SYST_NEWANALYSIS ${hepmc}
	wait
	mv Rivet.yoda ${hepmc}.yoda
done
