#!/bin/bash

# Need to source ROOT and PyAMI and Rucio

# User inputs the directory that contains the dataset folders
# Script first copies necessary scripts to that directory
# then changes to that directory
include_scripts="Prepare_Syst_File.sh Aux_Functions.py Rename_Folder.py \
		 MergeAidaFiles.py CompileRootFiles.py Find_Error_Band.py aidamerge.py"
work_dir=$1
if test -z "$work_dir" ; then
  work_dir=$PWD
fi
cp ${include_scripts} ${work_dir}
cd ${work_dir}

echo "Aux_Functions.py script stores the majority of the functions and specifications"
echo "referred to by all other scripts. It also stores necessary lists that may need"
echo "to be adjusted depending on if any new datasets are added or in any histograms"
echo "are added to the Rivet analysis."
echo "Scripts need to be in the directory in which the dataset directories are stored."
echo
echo
echo "Input the number corresponding to what you wish to do."
echo "0.  Do all of the following options in order (1-6)."
echo "1.  Do options 2-6 (i.e. skip rucio-get process)"
echo "2.  Use Rucio to get datasets in output_dataset.txt"
echo "3.  Rename Folders"
echo "4.  Merge Aida Files"
echo "5.  Compile Root Files"
echo "6.  Find Error Band"

read -p "Input number? " -n 1 -r
echo
echo

if [ $REPLY = "0" ] ; then
  # Check if output_dataset.txt file exists.
  out_data_file="./output_dataset.txt"
  if [ -f ${out_data_file} ]; then
    break
  else
    echo "The file ${out_data_file} was not found in current directory."
    exit 1
  fi
  echo "Running rucio-get and all scripts..."
  echo
  voms-proxy-init -voms atlas
  rucio-get -F output_dataset.txt
  wait
  REPLY="1"
fi
if [ $REPLY = "1" ] ; then
  echo "Running all scripts...minus rucio-get"
  echo "Adjusting directory names to satisfy script requirements"
  echo
  python Rename_Folder.py
  wait
  echo "Merging Aida files to produce a single .root file for each dataset."
  echo "Aida files are averaged and their errors are added in quadrature."
  echo
  python MergeAidaFiles.py
  wait
  echo "Compiling the individual dataset .root files into one single .root file."
  echo "The VBF_Systematics.root file stores each input .root file into a new directory."
  echo
  python CompileRootFiles.py
  wait
  echo "Making the error band plots. Currently you have to adjust the histograms"
  echo "to be created in the Find_Error_Band.py script."
  echo
  python Find_Error_Band.py
  wait
elif [ $REPLY = "2" ] ; then
  echo "Using rucio-get to get datasets given in output_dataset.txt."
  echo
  voms-proxy-init -voms atlas
  rucio-get -F output_dataset.txt
elif [ $REPLY = "3" ] ; then
  echo "Adjusting directory names to satisfy script requirements."
  echo
  python Rename_Folder.py
elif [ $REPLY = "4" ] ; then
  echo "Merging Aida files to produce a single .root file for each dataset."
  echo "Aida files are averaged and their errors are added in quadrature."
  echo
  python MergeAidaFiles.py
elif [ $REPLY = "5" ] ; then
  echo "Compiling the individual dataset .root files into one single .root file."
  echo "The VBF_Systematics.root file stores each input .root file into a new directory."
  echo
  python CompileRootFiles.py
elif [ $REPLY = "6" ] ; then
  echo "Making the error band plots. Currently you have to adjust the histograms"
  echo "to be created in the Find_Error_Band.py script."
  echo
  python Find_Error_Band.py
else
  echo "Wrong user input..."
  exit 1
fi