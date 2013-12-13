#!/bin/bash

# To remove any incomplete events from the end of the file
#echo "Removing incomplete events from the end of the file"
#python removeIncEvents.py
#echo "Counting Events in each file..."
#python Count_Events_LHEF.py

#echo "Splitting Files..."
#for lhe in $( ls *.lhe );
#do
#	python splitLHE.py -i $lhe -n 50000
#	rm $lhe
#done

# Ask for the file name prefix and also change extenstion from .lhe to .events
echo "Input the file name prefix: (e.g. user.cjohnson.powheg.w2jet.81514.txt._)"
read file_prefix
os_type=`uname`
#if [[ "$os_type" == 'Darwin' ]]; then
	rename 's/lhe/events/' *.lhe
#else
#	rename lhe events *.lhe
#fi

# Add "</LesHouchesEvents>" to end of each file
# To Do: check if </LesHouchesEvents> is already the last line
for file in $( ls *.events )
do
	echo "</LesHouchesEvents>" >> $file
done

# Rename the file to use the prefix given earlier
#if [[ "$os_type" == 'Darwin' ]]; then
	rename "s/pwgevents-/${file_prefix}/" pwgevents*	# For Mac OS X
#else
#	rename pwgevents- ${file_prefix} pwgevents*		# For Linux
#fi

# Tarball individual .event file and name the tarball w/o the .events ext.
for file in $( ls *.events )
do
	echo "Tarballing: " $file
	name=${file%.events}
	tar zcf ${name}.tar.gz $file
done

# Clean up and tarball into one neat package
#rm *.events
#echo "Tarballing the whole package"
#tar zcf events.tar.gz user.cjohnson*
#rm user.cjohnson*
