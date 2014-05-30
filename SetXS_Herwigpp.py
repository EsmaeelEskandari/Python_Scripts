#!/bin/python

import glob,os

xsec = ("3.65267E+03","5.00552E+02")    #Wminus
#xsec = ("3.53920E+03","7.08419E+02")    #Wplus
events_list = glob.glob("*.events")
file_in = events_list[0]
file_out = file_in+".1"

with open(file_out, "wt") as fout:
    with open(file_in, "rt") as fin:
        replace_XS = False
        index = 0
        for line in fin:
            index+=1
            if "<init>" in line:
                replace_XS = True
                init_line = index
            if ( replace_XS ) and ( index == init_line+2 ):
                new_line = line.replace("-1.00000E+00", xsec[0], 1)
                line = new_line.replace("-1.00000E+00", xsec[1], 1)
                replace_XS = False
            fout.write(line)

os.rename(file_out, file_in)
