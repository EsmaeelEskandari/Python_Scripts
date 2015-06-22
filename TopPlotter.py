import ROOT
import os, array, sys
from optparse import OptionParser

parser = OptionParser(usage="python %prog *NLO.top1 [*NLO.top2 ...]")
opts, args = parser.parse_args()

input_list = args
if (len(input_list) < 1):
    sys.stderr.write("Must specify at least one top file.\n")
    sys.exit(1)

for input_file in input_list:
    file_name = os.path.splitext(input_file)[0]
    root_file = ROOT.TFile(file_name+".root", "RECREATE")
    with open(input_file) as file:
        startOfHist = False
        fillHist = False
        for number,line in enumerate(file):
            if "#" in line:
                hist_key = line.split()[1]
                startOfHist = True
                line_number = number
                xbins_low = []
                bin_cont = []
                bin_err = []
            if not line.strip(): 
                startOfHist = False
                fillHist = True
            if startOfHist and (number != line_number):
                line_content = line.replace("D","E").split()
                xbins_low.append(float(line_content[0]))
                bin_cont.append(float(line_content[2]))
                bin_err.append(float(line_content[3]))
                poss_last_bin = float(line_content[1])
            if fillHist:
                xbins_low.append(poss_last_bin)
                xbins_low_array = array.array('d',xbins_low)
                histogram = ROOT.TH1F(hist_key,hist_key,len(xbins_low)-1,xbins_low_array)
                for index in range(len(bin_cont)):
                    histogram.SetBinContent(index+1,bin_cont[index])
                    histogram.SetBinError(index+1,bin_err[index])
                histogram.Write()
                del histogram
                fillHist = False
            
    root_file.Close()