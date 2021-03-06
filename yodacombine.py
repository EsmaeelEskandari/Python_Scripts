#! /usr/bin/env python2

"""\
%prog -o outfile <action>  <yodafile1> <yodafile2> ...

where <action> = add, errsum, quaderrsum, envelope, transfererrors
"""

import ROOT
import yoda, optparse, operator, itertools, sys, copy
from math import sqrt

parser = optparse.OptionParser(usage=__doc__)
parser.add_option('-o', '--output', default='-', dest='OUTPUT_FILE')
opts, args = parser.parse_args()
action=args[0]
filenames=args[1:]


## Put the incoming objects into a dict from each path to a list of histos
scatters_in = {}
for filename in filenames:
    for p, ao in yoda.readYODA(filename).iteritems():
        if isinstance(ao, yoda.Scatter2D):
            scatter = ao
        elif isinstance(ao, yoda.Histo1D):
            scatter = yoda.Scatter2D(ao.path, ao.title)
            for bin in ao.bins:
                scatter.addPoint(yoda.Point2D(bin.xMid, bin.height, 0.5*bin.xWidth, bin.heightErr))
        else:
            print "cannot treat ", ao
            continue
        scatters_in.setdefault(ao.path, []).append(scatter)

scatters_out = {}
for p, scatters in scatters_in.iteritems():
    scatters_out[scatters[0].path] = scatters[0].clone()
    
    for i, point in enumerate(scatters_out[scatters[0].path].points):
        if action=="add":
            sum = 0.0
            sumerrminus = 0.0
            sumerrplus = 0.0
            for scatter in scatters:
                tmppoint = scatter.points[i];
                sum += tmppoint.y
                sumerrminus += tmppoint.yErrs[0]
                sumerrplus += tmppoint.yErrs[1]
            point.y = sum
            point.yErrs = (sumerrminus, sumerrplus)
        elif action=="errsum":
            sumerrminus = 0.0
            sumerrplus = 0.0
            for scatter in scatters:
                tmppoint = scatter.points[i];
                sumerrminus += tmppoint.yErrs[0]
                sumerrplus += tmppoint.yErrs[1]
            point.yErrs = (sumerrminus, sumerrplus)
        elif action=="quaderrsum":
            sum = 0.0
            sumerr2minus = 0.0
            sumerr2plus = 0.0
            for scatter in scatters:
                tmppoint = scatter.points[i];
                sum += tmppoint.y
                sumerr2minus += tmppoint.yErrs[0]**2
                sumerr2plus += tmppoint.yErrs[1]**2
            point.yErrs = (sqrt(sumerr2minus), sqrt(sumerr2plus))
        elif action=="envelope":
            upper = float('-inf')
            lower = float('inf')
            for scatter in scatters:
                val = scatter.points[i].y;
                if val > upper:
                    upper = val
                if val < lower:
                    lower = val
            point.yErrs = (point.y-lower, upper-point.y)
        elif action=="transfererrors":
            point.y = scatters[0].points[i].y
            point.yErrs = scatters[1].points[i].yErrs
        else:
            print "Unknown action: ",action
            exit(1)

yoda.write(scatters_out.values(), opts.OUTPUT_FILE)
