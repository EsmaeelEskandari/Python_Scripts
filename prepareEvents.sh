#!/bin/bash

# To remove any incomplete events from the end of the file
echo "Removing incomplete evetns from the end of the file"
python removeIncEvents.py

# Ask for the file name prefix and also change extenstion from .lhe to .events
echo "Input the file name prefix: (e.g. user.cjohnson.powheg.w2jet.81514.txt._)"
read file_prefix
rename lhe events *.lhe

# Add "</LesHouchesEvents>" to end of each file
for file in *.events
do
	echo "</LesHouchesEvents>" >> $file
done

# Rename the file to use the prefix given earlier
rename pwgevents- ${file_prefix} pwgevents*

# Tarball individual .event file and name the tarball w/o the .events ext.
for file in *.events
do
	echo "Tarballing: " $file
	name=${file%.events}
	tar zcf ${name}.tar.gz $file
done

# Clean up and tarball into one neat package
rm *.events
echo "Tarballing the whole package"
tar zcf events.tar.gz user.cjohnson*
rm user.cjohnson*
