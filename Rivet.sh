#!/bin/bash

for hepmc in $( ls *.hepmc ); do
	rivet -a WJETS_SYST_NEWANALYSIS ${hepmc}
	wait
	mv Rivet.yoda ${hepmc}.yoda
done

# # For W2jets - Background
# xsec=( 5228.18638778672 7497.65468562505 3652.66944215 3539.19590298 )
# index=0
# for prefix in "No_bornsuppfact" "bornsuppfact_lin_mjj"; do
#   for suffix in "Wminus" "Wplus"; do
#     cd /Volumes/FIREWIRE_HD/POWHEG_W2jet_Wmunu/${prefix}/${suffix}/HepMC/
#     echo $PWD
#     rivet -x ${xsec[index]} -a WJETS_SYST_NEWANALYSIS *.hepmc
#     wait
#     mv Rivet.yoda ~/Desktop/WFinder_All_Cuts/W2jets_${prefix}_${suffix}.yoda
#     let index=index+1
#   done
# done

# For VBF - Signal
# xsec=( 1.33756983926 2.11001724826 3.03772126412 4.03204089973 )
# index=0
# for prefix in "ptj_gencut" "bornsuppfact"; do
#   for suffix in "Wminus" "Wplus"; do
#     cd /Volumes/FIREWIRE_HD/POWHEG_VBF_Wmunu/${prefix}/${suffix}/HepMC/
#     echo $PWD
#     rivet -x ${xsec[index]} -a WJETS_SYST_NEWANALYSIS Nominal.hepmc
#     wait
#     mv Rivet.yoda ~/Desktop/WFinder_All_Cuts/VBF_${prefix}_${suffix}.yoda
#     let index=index+1
#   done
# done