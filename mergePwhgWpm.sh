
#!/bin/bash

for folder in $( ls -d 0* ); do
#####---Make sure aidamerge.py is NOT averaging when using -s option.---#####
#  echo $folder
#  cd $folder
#  for channel in "Wminus" "Wplus"; do
#    cd $channel
#    python ../../aidamerge.py *.aida* -o ${channel}_avg.aida
#    python ../../aidamerge.py -s *.aida* -o ${channel}_add.aida
#    mv ${channel}_avg.aida ${channel}_add.aida ..
#    cd ..
#  done
#  cd ..

######----Make sure aidamerge.py is averaging when using -s option.----######
  IFS='.' read -a string_bits <<< "${folder}"
  cd $folder
  echo $folder
  python ../aidamerge.py -s Wminus_avg.aida Wplus_avg.aida -o ${string_bits[0]}.aida
  python ../aidamerge.py -s Wminus_add.aida Wplus_add.aida -o ${string_bits[0]}_add.aida
  aida2root ${string_bits[0]}.aida
  aida2root ${string_bits[0]}_add.aida
  cd ..
done