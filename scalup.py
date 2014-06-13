import glob,os

scalup_fact = 0.75  # 1.5
events_list = glob.glob("*.events")
file_in = events_list[0]
file_out = file_in+".1"

with open(file_out, "wt") as fout:
    with open(file_in, "rt") as fin:
        replace_SU = False
        index = 0
        for line in fin:
            index+=1
            if "<event>" in line:
                replace_SU = True
                event_line = index
            if ( replace_SU ) and ( index == event_line+1 ):
                line_list = line.split()
                old_scalup = float(line_list[3])
                new_scalup = old_scalup*scalup_fact
                line_list[3] = '%.5E' % new_scalup
                line = " ".join(line_list)
                line = '      ' + line + '\n'
                replace_SU = False
            fout.write(line)

os.rename(file_out, file_in)