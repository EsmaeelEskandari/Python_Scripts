###############################################################
##  Author:   David Hall
##  Email:    David(dot)Hall(at)physics(dot)ox(dot)ac(dot)uk
##  Date:     8th April 2013
##  Program:  top2root
##
##  This program reads in a topdrawer file and converts the
##  plots contained within to the ROOT histogram format.
##  It assumes that you have a copy of PyROOT installed and
##  the appropriate environment variables set.
###############################################################
 
class DataPoint:
    def __init__(self, x, y, dy):
        self.x  = x
        self.y  = y
        self.dy = dy
    def __str__(self):
        return "x=%f, y=%f, dy=%f" % (self.x, self.y, self.dy)
 
class Graph:
    def __init__(self):
        import ROOT
        self.data = []
    def SetTitle(self, title):
        self.title = title
    def SetXaxisTitle(self, title):
        self.xaxistitle = title
    def SetYaxisTitle(self, title):
        self.yaxistitle = title
    def SetXaxisLimits(self, low, high):
        self.xaxislowbound  = low
        self.xaxishighbound = high
    def AddDataPoint(self, x, y, dy):
        datum = DataPoint(x, y, dy)
        self.data.append(datum)
    def GetDx(self):
        sumbins = 0.0
        for datum in self.data:
            sumbins += datum.y
        return self.integral / sumbins
    def GetTH1(self):
        nBins = int(round((self.xaxishighbound - self.xaxislowbound) / self.GetDx()))
        hist = ROOT.TH1F(self.title, self.title, nBins, self.xaxislowbound, self.xaxishighbound)
        hist.GetXaxis().SetTitle(self.xaxistitle)
        hist.GetYaxis().SetTitle(self.yaxistitle)
        for datum in self.data:
            hist.SetBinContent(hist.FindBin(datum.x), datum.y)
            hist.SetBinError  (hist.FindBin(datum.x), datum.dy)
        return hist
    def GetTGraph(self):
        graph = ROOT.TGraphErrors()
        graph.SetNameTitle(self.title + " (TGraph)", self.title)
        graph.GetXaxis().SetTitle(self.xaxistitle)
        graph.GetYaxis().SetTitle(self.yaxistitle)
        counter = 0
        for datum in self.data:
            graph.SetPoint(counter, datum.x, datum.y)
            graph.SetPointError(counter, self.GetDx(), datum.dy)
            counter += 1
        return graph
 
def GetTitle(string):
    title = string.split("\"")[-2]
    return " ".join(title.split())
 
if __name__ == "__main__":
    import sys
    tmpargv = sys.argv[:]
    sys.argv = []
    try:
        import ROOT
    except ImportError:
        print "Please ensure PYTHONPATH is set correctly before using top2root"
        exit(1)
    sys.argv = tmpargv
    from optparse import OptionParser
    ROOT.gROOT.SetBatch()
 
    ##############################
    #  Parse command line input  #
    ##############################
    usage = "usage: %prog [-g] infile.top"
    parser = OptionParser(usage=usage)
    parser.add_option("-g", "--graph",
                      action="store_true", dest="isGraph", default=False,
                      help="Output TGraph (TH1 is default)")
 
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    inFilename  = args[0]
    if len(inFilename.rsplit(".")) < 2 or not inFilename.rsplit(".", 1)[1]:
        parser.error("Input filename does not have an extension")
    outFilename = inFilename.rsplit(".", 1)[0] + ".root"
 
    ##############################
    #   Read-in topdrawer file   #
    ##############################
    inFile = open(inFilename, "r")
    top_plots = []
    newPlot = True
    dataFlag = False
    for line in inFile:
        # Instantiate a new plot when appropriate
        if newPlot:
            plot = Graph()
            newPlot = False
 
        # Retrieve metadata
        if not dataFlag:
            if "NEW PLOT" in line:    # Plots end with this
                top_plots.append(plot)
                newPlot = True
                continue
            elif "TITLE TOP" in line:
                plot.SetTitle(GetTitle(line))
            elif "TITLE BOTTOM" in line:
                plot.SetXaxisTitle(GetTitle(line))
            elif "TITLE LEFT" in line:
                plot.SetYaxisTitle(GetTitle(line))
            elif "SET LIMITS X" in line:
                words = line.split()
                plot.SetXaxisLimits(float(words[-2]), float(words[-1]))
            elif "INTGRL" in line:
                integral = line.split("INTGRL = ")[1].split()[0]
                plot.SetIntegral(float(integral))
            elif "SET ORDER X Y DY" in line:
                dataFlag = True
                continue
 
        # Retrieve data points
        if dataFlag:
            if "PLOT" in line:
                dataFlag = False
            else:
                words = line.split()
                plot.AddDataPoint(float(words[0]), float(words[1]), float(words[2]))
 
    print "Read in " + str(len(top_plots)) + " plots"
    ##############################
    #   Write out to ROOT file   #
    ##############################
    outFile = ROOT.TFile(outFilename, "recreate")
    root_plots = []
    for plot in top_plots:
        if options.isGraph:
            root_plots.append(plot.GetTGraph())
        else:
            root_plots.append(plot.GetTH1())
 
    for plot in root_plots:
        plot.Write()
    outFile.Close()