import glob,os

events_list = glob.glob("*.events")
file_in = events_list[0]
file_out = file_in+".1"

with open(file_out, "wt") as fout:
    with open(file_in, "rt") as fin:
        for line in fin:
            line_list = line.split()
            if len(line_list) == 0:
                line = "\n"
                fout.write(line)
            elif (line_list[0] == "13") or (line_list[0] == "-13"):
                new_line = line.replace("13","15",1)
                fout.write(new_line)
            elif (line_list[0] == "14") or (line_list[0] == "-14"):
                new_line = line.replace("14","16",1)
                fout.write(new_line)
            else:
                fout.write(line)

os.rename(file_out, file_in)