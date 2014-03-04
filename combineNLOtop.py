import glob, sys
from optparse import OptionParser

parser = OptionParser(usage="Run this script in the directory containing the .top files to be averaged[added]")
parser.add_option("-o", "--outfile", dest="OUTFILE", default="merged-NLO.top", help="file for merged top output.")
parser.add_option("-s", "--sum", action="store_true", dest="performSum", default=False,
                  help="sum the bin values instead of averaging, but the error will still be averaged. (for combining different processes.)")
opts, args = parser.parse_args()

if (opts.performSum):
    if (len(args) < 1):
        sys.stderr.write("Must specify at least one top file.\n")
        sys.exit(1)
    filenames = args
    print "Performing summation over all top files."
else:
    filenames = glob.glob('*.top')
    print "Performing average over all top files."
num_files = len(filenames)

output_matrix = [] # [line][line_element]
for index,fname in enumerate(filenames):
    if index == 0: firstFile = True
    else: firstFile = False
    with open(fname) as infile:
        for idx,line in enumerate(infile):
            new_line = line.split()
            line_length = len(new_line)
            if firstFile:
                if "#" not in line:     # new_line = [xbin_low, xbin_high, bin_content, bin_error]
                    for j,element in enumerate(new_line):
                        if "D" in element: element = element.replace("D","E")
                        new_line[j] = float(element)
                    output_matrix.append(new_line)
                else: output_matrix.append(new_line)
            else:
                if "#" not in line:
                    for j,element in enumerate(new_line):
                        if "D" in element: element = element.replace("D","E")
                        new_line[j] = float(element)
                        output_matrix[idx][j] = output_matrix[idx][j]+new_line[j]
                else: continue
                
with open('./'+opts.OUTFILE, 'w') as outfile:
    for line in output_matrix:
        for idx,element in enumerate(line):
            if "#" in line:
                outfile.write(str(element))
                outfile.write("  ")
            else:
                avg = element/num_files
                if (opts.performSum):
                    if idx == 2:
                        outfile.write(str(element))
                        outfile.write("  ")
                    else:
                        outfile.write(str(avg))
                        outfile.write("  ")
                else:
                    outfile.write(str(avg))
                    outfile.write("  ")
        outfile.write("\n")
