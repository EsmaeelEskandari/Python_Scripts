#! /usr/bin/env python

import sys, os, copy
from math import sqrt
from subprocess import Popen
import lighthisto

def MergeChannels(hist_errs):     # Merge statistics when adding two channels
    if len(hist_errs) > 2:
        sys.stderr.write("Should not try to merge more than two channels\n")
        sys.exit(1)
    bin_err1 = hist_errs[0]
    bin_err2 = hist_errs[1]
    if bin_err1 == 0.0: weight1 = 0.0
    else: weight1 = 1.0/(bin_err1**2)
    if bin_err2 == 0.0: weight2 = 0.0
    else: weight2 = 1.0/(bin_err2**2)
    new_stat = weight1+weight2
    if new_stat != 0.0:
        new_bin_err = 1.0/new_stat
    else: new_bin_err = 1.e308
    
    return new_bin_err

## Try to load faster but non-standard cElementTree module
try:
    import xml.etree.cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        try:
            import xml.etree.ElementTree as ET
        except:
            sys.stderr.write("Can't load the ElementTree XML parser: please install it!\n")
            sys.exit(1)

from optparse import OptionParser
parser = OptionParser(usage="%prog aidafile [aidafile2 ...]")
parser.add_option("-o", "--outfile", dest="OUTFILE",
                  default="merged.aida", help="file for merged aida output.")
parser.add_option("-s", "--sum",
                  action="store_true", dest="performSum", default=False,
                  help="sum the bin values instead of averaging")
parser.add_option("-c", "--sum-channels",
                  action="store_true", dest="sumChannels", default=False,
                  help="sum the bin values instead of averaging but average the errors")
opts, args = parser.parse_args()
headerprefix = ""

if len(args) < 1:
    sys.stderr.write("Must specify at least one AIDA histogram file\n")
    sys.exit(1)


try:
    outaida = open(opts.OUTFILE, "w")
except:
    sys.stderr.write("Couldn't open outfile %s for writing." % opts.OUTFILE)

try:
    outdat = open(opts.OUTFILE.replace(".aida", ".dat"), "w")
except:
    sys.stderr.write("Couldn't open outfile %s for writing." % opts.OUTFILE.replace(".aida", ".dat"))

## Get histos
inhistos = {}
weights = {}
for aidafile in args:
    tree = ET.parse(aidafile)
    for dps in tree.findall("dataPointSet"):
        h = lighthisto.Histo.fromDPS(dps)
        if not inhistos.has_key(h.fullPath()):
            inhistos[h.fullPath()] = {}
        inhistos[h.fullPath()][aidafile] = h

## Merge histos
outhistos = {}
for path, hs in inhistos.iteritems():
    #print path, hs
    outhistos[path] = copy.deepcopy(hs.values()[0])
    for i, b in enumerate(outhistos[path].getBins()):
        sum_val = 0.0
        sum_err2 = 0.0
        n = 0
        if opts.sumChannels:
            hist_errs = []
            for infile, h in hs.iteritems():
                sum_val += h.getBin(i).val
                hist_errs.append(h.getBin(i).getErr())
            sum_err2 = MergeChannels(hist_errs)
        else:
            for infile, h in hs.iteritems():
                sum_val += h.getBin(i).val
                try:
                    sum_err2 += h.getBin(i).getErr()**2
                except OverflowError:
                    # in case the **2 produces overflow errors
                    # set sum to 'inf'
                    sum_err2 = float('inf')
                n += 1
            
        if (opts.performSum or opts.sumChannels): outhistos[path].getBin(i).val = sum_val
        else:                 outhistos[path].getBin(i).val = sum_val / n

        try:
            if (opts.performSum or opts.sumChannels): outhistos[path].getBin(i).setErr(sum_err2**0.5 )
            else:                 outhistos[path].getBin(i).setErr(sum_err2**0.5 / n)
        except OverflowError:
            # to get back to numerics, replace an eventual 'inf' 
            # in sum_err2 with max float available ~1.e+308
            outhistos[path].getBin(i).setErr(1.e308)

## Write out merged histos
#print sorted(outhistos.values())
outdat.write("\n\n".join([h.asFlat() for h in sorted(outhistos.values())]))
outdat.write("\n")
outdat.close()

Popen(["flat2aida", opts.OUTFILE.replace(".aida", ".dat")], stdout=outaida).wait()

os.unlink(opts.OUTFILE.replace(".aida", ".dat"))
