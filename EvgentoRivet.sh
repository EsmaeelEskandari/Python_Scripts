#!/bin/bash

if [[ -z "$1" ]]
then
    NUM="-1"
    RIVNUM=""
else
    NUM=$1
    RIVNUM="-n $1"
fi

python - > temp.txt <<END             ## (Python section to get names of all EVNT root files in directory)
import os
dir_list = os.listdir("$DIR")
for item in dir_list:
    if (".pool.root" in item):
	    print '"' + '$DIR' + '/' + item + '",',
	    pass
    pass
END
FILES=`more temp.txt`

cat >Ev2Hep.py <<EOF
#! /usr/bin/env python
from AthenaCommon.AppMgr import ServiceMgr
import AthenaPoolCnvSvc.ReadAthenaPool
ServiceMgr.EventSelector.InputCollections = [$FILES]
from AthenaCommon.AlgSequence import AlgSequence
job = AlgSequence()
from McParticleTools.McParticleToolsConf import HepMcWriterTool
from McParticleAlgs.McParticleAlgsConf   import GenEventAsciiWriter
McWriter = HepMcWriterTool(McEvents="GEN_EVENT", Output="hepmc.fifo")
job += GenEventAsciiWriter(McWriter=McWriter, OutputLevel=INFO)
theApp.EvtMax = $NUM
EOF

# Reset the fifo            
rm hepmc.fifo
mkfifo hepmc.fifo

# Run the evgen to HepMC conversion in the background                                                                         
source /afs/cern.ch/atlas/software/dist/AtlasSetup/scripts/asetup.sh 17.2.6.2,slc5 --pythonversion=2.7
athena.py Ev2Hep.py &

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
localSetupROOT --quiet
source /afs/cern.ch/sw/lcg/external/MCGenerators_lcgcmt67/rivet/2.0.0/x86_64-slc6-gcc47-opt/rivetenv.sh
export RIVET_ANALYSIS_PATH=/data/atlas/atlasdata/henderson/custom_rivet:$RIVET_ANALYSIS_PATH

# Set the cross-section for this process
XS=9.8663
RIVET_ANALYSIS="MC_VBF"

# Run rivet on the fifo    
rivet $RIVNUM -a $RIVET_ANALYSIS -x $XS hepmc.fifo

# Clean up
rm -rf Ev2Hep.py hepmc.fifo PoolFileCatalog.xml PoolFileCatalog.xml.BAK eventLoopHeartBeat.txt temp.txt