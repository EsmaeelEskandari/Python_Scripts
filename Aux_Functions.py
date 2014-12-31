import ROOT
import math
from collections import Counter

#--------------Atlas Style---------------------------------------------------
class AtlasStyle( ROOT.TStyle ):

    ##
    # @short Object constructor
    #
    # The constructor just initializes the underlying TStyle object, and
    # calls the configure() function to set up the ATLAS style.
    #
    # The parameters of the constructor should just be ignored in 99.9%
    # of the cases.
    #
    # @param name The name given to the style
    # @param title The title given to the style
    def __init__( self, name = "AtlasStyle", title = "ATLAS style object" ):

	# Initialise the base class:
	ROOT.TStyle.__init__( self, name, title )
	self.SetName( name )
	self.SetTitle( title )

	# Call the configure function for setting up the style:
	self.configure()

	return

    ##
    # @short Configure the object for the ATLAS style
    #
    # This function actually takes care of setting up the ATLAS style.
    # I implemented it based on a C++ TStyle object, which in turn was
    # implemented based on a central piece of CINT macro.
    def configure( self ):

	# Tell the user what we're doing:
	self.Info( "configure", "Configuring default ATLAS style" )

	# Use plain black on white colors:
	icol = 0
	self.SetFrameBorderMode( 0 )
	self.SetFrameFillColor( icol )
	self.SetFrameFillStyle( 0 )
	self.SetCanvasBorderMode( 0 )
	self.SetPadBorderMode( 0 )
	self.SetPadColor( icol )
	self.SetCanvasColor( icol )
	self.SetStatColor( icol )

	# Set the paper and margin sizes:
	#self.SetPaperSize(20, 26)
	self.SetPadTopMargin(0.10)	#0.05
	self.SetPadRightMargin(0.025)	#0.05
	self.SetPadBottomMargin(0.10)	#0.16
	self.SetPadLeftMargin(0.12)	#0.16

	# set title offsets (for axis label)
	self.SetTitleXOffset(1.1)	#1.4
	self.SetTitleYOffset(1.3)	#1.4
	self.SetTitleStyle(0)
	self.SetTitleBorderSize(0)
	self.SetTitleX(0.2)

	# Use large fonts:
	font_type = 42
	font_size = 0.04
	self.SetTextFont( font_type )
	self.SetTextSize( font_size )
	self.SetLabelFont( font_type, "x" )
	self.SetLabelSize( font_size, "x" )
	self.SetTitleFont( font_type, "x" )
	self.SetTitleSize( font_size, "x" )
	self.SetLabelFont( font_type, "y" )
	self.SetLabelSize( font_size, "y" )
	self.SetTitleFont( font_type, "y" )
	self.SetTitleSize( font_size, "y" )
	self.SetLabelFont( font_type, "z" )
	self.SetLabelSize( font_size, "z" )
	self.SetTitleFont( font_type, "z" )
	self.SetTitleSize( font_size, "z" )

	# Use bold lines and markers:
	#self.SetMarkerStyle( 20 )
	#self.SetMarkerSize( 1.2 )
	#self.SetHistLineWidth( 2 )
	#self.SetLineStyleString( 2, "[12 12]" )

	# Do not display any of the standard histogram decorations:
	#self.SetOptTitle(0)
	self.SetOptStat(0)
	#self.SetOptFit(0)

	# Put tick marks on top and rhs of the plots:
	self.SetPadTickX(1)
	self.SetPadTickY(1)

	return

#--------------Create_Hists.py-----------------------------------------------
def DivideBinWidth(h1):
    for bin in range(h1.GetNbinsX()):
        bin_width = h1.GetBinWidth(bin)
        bin_cont = h1.GetBinContent(bin)/bin_width
        bin_err = h1.GetBinError(bin)/bin_width
        h1.SetBinContent(bin_cont)
        h1.SetBinError(bin_err)
    return h1

def MakeLegend(h1,h2):
    leg = ROOT.TLegend(0.2,0.77,0.5,0.87)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    #leg.AddEntry(h1,"min_n_tchannels (signal)","f")
    #leg.AddEntry(h2,"W+jets","f")
    leg.AddEntry(h1,"min_n_tchannels (signal)","l")
    leg.AddEntry(h2,"W+jets","l")
    return leg
      
def SetHistStyle(h1,h2,max_1,max_2,min_1,min_2):
    #h1.SetFillColor(ROOT.TAttFill.kYellow)
    h1.SetLineColor(ROOT.TAttLine.kBlue)
    h1.SetLineWidth(3)
    #h1.GetYaxis().SetTitleOffset(1.5)
    #h2.SetFillColor(ROOT.TAttFill.kGreen-8)
    h2.SetLineColor(ROOT.TAttLine.kRed)
    h2.SetLineWidth(3)
    #h2.GetYaxis().SetTitleOffset(1.5)
    if max_1 > max_2 and max_1 != 0:
	    h1.SetMaximum(10*max_1)
	    if min_1 < min_2:
		    h1.SetMinimum(min_1/5)
	    else:
		    h1.SetMinimum(min_2/5)
    elif max_2 > max_1 and max_2 != 0:
	    h2.SetMaximum(10*max_2)
	    if min_1 < min_2:
		    h2.SetMinimum(min_1/5)
	    else:
		    h2.SetMinimum(min_2/5)
    return h1, h2
      
#--------------Find_Error_Band.py-------------------------------------------------
def MakeErrorBandLegend(h1,h2):
    leg = ROOT.TLegend(0.55,0.77,0.75,0.87)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    leg.AddEntry(h1,"Nominal Sherpa","l")
    leg.AddEntry(h2,"Systematic Error","f")
    return leg
      
def FindErrorBands(datasets,root_file,hist,isPowheg):
    rebin_to = 0	# Set this to how many bins you would like (0 -> no change)
    nom_hist = root_file.Get(datasets[0]+"/Normalized_XS/"+hist+'_norm')
    nom_hist = nom_hist.Clone()
    numb_of_bins = nom_hist.GetNbinsX()
    print numb_of_bins
    if rebin_to > 0.0: rebin = numb_of_bins/rebin_to
    else: rebin = 1
    #rebin = 5
    nom_hist.Rebin(rebin)
    nom_graph = ROOT.TGraphAsymmErrors(nom_hist)
    nom_graph.SetLineColor(ROOT.TAttFill.kGreen)
    nbins = nom_hist.GetNbinsX()

    upper_error = []
    lower_error = []
    tot_stat_errors = []
    sequence = datasets[1:]
    for bin in range(1,nbins+1):
      positive_shifts2 = []
      negative_shifts2 = []
      shifts = []
      shift_times_unc = []
      nom_bin_val = nom_hist.GetBinContent(bin)
      nom_bin_err = nom_hist.GetBinError(bin)

      for dataset in sequence:
        if root_file.GetDirectory(dataset) == None:
          print dataset+" does not exist!"
          continue
        hist_to_clone = root_file.Get(dataset+"/Normalized_XS/"+hist+'_norm')
        hist_to_comp = hist_to_clone.Clone(dataset)
        hist_to_comp.Rebin(rebin)
        hist_bin_num = hist_to_comp.GetNbinsX()
        if hist_bin_num != numb_of_bins and bin == 1:
            print "{0} has {1} bins and Nominal has {2} bins".format(dataset,hist_bin_num,numb_of_bins)
            print "Should check that bins are properly aligned between Nominal and Varied samples."

        comp_bin_val = hist_to_comp.GetBinContent(bin)
        comp_bin_err = hist_to_comp.GetBinError(bin)

        diff = comp_bin_val - nom_bin_val
        
        if (diff >= 0.0):
          positive_shifts2.append(diff*diff)
          negative_shifts2.append(0.0)
        else:
          positive_shifts2.append(0.0)
          negative_shifts2.append(diff*diff)
      
      if isPowheg:
          upper_error.append(math.sqrt(max(positive_shifts2)))
          lower_error.append(math.sqrt(max(negative_shifts2)))
          #upper_error.append(math.sqrt(math.fsum(positive_shifts2)))
          #lower_error.append(math.sqrt(math.fsum(negative_shifts2)))
      else:
          upper_error.append(math.sqrt(math.fsum(positive_shifts2)))
          lower_error.append(math.sqrt(math.fsum(negative_shifts2)))
		
      nom_graph.SetPointEYhigh(bin-1,upper_error[bin-1])
      nom_graph.SetPointEYlow(bin-1,lower_error[bin-1])

    return nom_hist, nom_graph, tot_stat_errors
      
def MakeRatioPlot(nom_hist,nom_graph,tot_stat_errors):
    npoints = nom_hist.GetNbinsX()
    ratio_plot = ROOT.TGraphAsymmErrors(npoints)
    stat_plot = ROOT.TGraphErrors(npoints)
    for point in range(npoints):
	Error_High = nom_graph.GetErrorYhigh(point)
	Error_Low = nom_graph.GetErrorYlow(point)
	Y_point = nom_hist.GetBinContent(point+1)
	X_point = nom_hist.GetBinCenter(point+1)
	X_Axis = nom_hist.GetXaxis()
	if Y_point == 0.0:
	    ratio_up = 0.0
	    ratio_down = 0.0
	else:
	    ratio_up = Error_High/Y_point
	    ratio_down = Error_Low/Y_point
	ratio_plot.SetPoint(point, X_point, 1.0)
	ratio_plot.SetPointEXhigh(point, nom_hist.GetBinWidth(point)/2.0)
	ratio_plot.SetPointEXlow(point, nom_hist.GetBinWidth(point)/2.0)
	ratio_plot.SetPointEYhigh(point, ratio_up)
	ratio_plot.SetPointEYlow(point, ratio_down)
#	stat_plot.SetPoint(point,nom_hist.GetBinWidth(point)/2.0,tot_stat_errors[point])
#	stat_plot.SetPointError(point,nom_hist.GetBinWidth(point)/2.0,tot_stat_errors[point])

    return ratio_plot, stat_plot
    
#-----------Cut Flow and Acceptance Plot----------------------------------------

def MakeCutFlow(datasets,root_file,pdf_name,gen_accept=True,save_as_pdf=True,tolerance=0.05):
    # datasets: list of datasets to retrieve cut flow from
    # root_file: root file to get the data from (must already be opened)
    # pdf_name: name to save the plot as (in .pdf format)
    # gen_accept: boolean to decide whether to produce acceptance plot or not
    # save_as_pdf: boolean to decide whether to save pdfs or not
    # tolerance: how far the first bin can stray from the mode before being scaled
    # TODO: Add the ability to create Acceptance plots here
    hist = "CutFlow_1" # Or CutFlow_2 for 20GeV pT threshold
    dataset_names = GetListDataset('dataset_names')
    cross_sections = GetListDataset('cross_sections')
    Colors = ["ROOT.TAttFill.kBlack", "ROOT.TAttFill.kOrange", "ROOT.TAttFill.kRed", 
            "ROOT.TAttFill.kOrange+7", "ROOT.TAttFill.kGreen+3", "ROOT.TAttFill.kViolet-6",
            "ROOT.TAttFill.kMagenta-3", "ROOT.TAttFill.kTeal+4", "ROOT.TAttFill.kBlue"]
    if len(datasets) > len(Colors): print "Need to define more colors!"
    root_file = ROOT.TFile("VBF_Systematics.root")
    c1 = ROOT.TCanvas('c1','Cut_Flow',0,0,640,640)
    c1.SetLogy()
    leg = ROOT.TLegend(0.2,0.2,0.5,0.4)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.02)
    
    events_passed = []
    events_in_first_bin = []
    for folder in datasets:
        new_histo = root_file.Get(folder+"/"+hist)
        events_in_first_bin.append(new_histo.GetBinContent(2))
        del new_histo
    count = Counter(events_in_first_bin)
    mode = count.most_common(1)[0][0]    
    for index,folder in enumerate(datasets):
        xs_index = dataset_names.index(folder)
        xsec = cross_sections[xs_index][0]
        new_histo = root_file.Get(folder+"/"+hist)
        new_histo.GetYaxis().SetTitle("Events")
        first_bin = new_histo.GetBinContent(2)
        last_bin = new_histo.GetBinContent(11)
        # Check that the histograms are scaled such that the first are within 5% of the mode.
        # Add the scale factor to the legend.
        if (abs(first_bin - mode) > mode*tolerance):
            new_histo.Scale(mode/first_bin)
            leg_string = " x "+str(mode/first_bin)
        else: leg_string = ""
        new_histo.SetLineColor(eval(Colors[index]))
        leg.AddEntry(new_histo,folder+leg_string,"l")
        new_histo.Draw("hist same")
        events_passed.append(last_bin/first_bin*xsec) # Acceptance Calculation
        del new_histo
    leg.Draw()
    if save_as_pdf: c1.SaveAs(pdf_name+".pdf")
    c1.Clear()
    
    # Returns Acceptance for each dataset
    return events_passed
    
#def MakeAcceptancePlots():

#-----------Used by all---------------------------------------------------------
def GetListDataset(list_name):
    # This function returns the list that is associated with the string 'list_name'.
    # i.e., GetListDataset('datasets') returns the list datasets
    # Names of new lists must be put in the list_of_lists list.

    datasets = 	['mc12_8TeV.129916.Sherpa_CT10_Wmunu2JetsEW1JetQCD15GeV_min_n_tchannels.evgen.EVNT.e1557/',
          'mc12_8TeV.129930.Sherpa_CT10_Wmunu_MjjFiltered.evgen.EVNT.e1538/',
	  'mc12_8TeV.147294.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_CKKW30.evgen.EVNT.e1805/',
	  'mc12_8TeV.147295.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_CKKW30_MjjFilt.evgen.EVNT.e1805/',
	  'mc12_8TeV.147296.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFdown.evgen.EVNT.e2355/',
	  'mc12_8TeV.147297.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFdown_MjjFilt.evgen.EVNT.e2355/',
	  'mc12_8TeV.147298.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFup.evgen.EVNT.e2355/',
	  'mc12_8TeV.147299.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFup_MjjFilt.evgen.EVNT.e2355/',
	  'mc12_8TeV.147300.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi1.evgen.EVNT.e1805/',
	  'mc12_8TeV.147301.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi1_MjjFilt.evgen.EVNT.e1805/',
	  'mc12_8TeV.147302.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi2.evgen.EVNT.e1805/',
	  'mc12_8TeV.147303.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi2_MjjFilt.evgen.EVNT.e1805/',
	  'mc12_8TeV.147304.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_Shower1.evgen.EVNT.e1805/',
	  'mc12_8TeV.147305.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_Shower1_MjjFilt.evgen.EVNT.e1805/',
	  'mc12_8TeV.147306.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRdown.evgen.EVNT.e2355/',
	  'mc12_8TeV.147307.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRdown_MjjFilt.evgen.EVNT.e2355/',
	  'mc12_8TeV.147308.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRup.evgen.EVNT.e2355/',
	  'mc12_8TeV.147309.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRup_MjjFilt.evgen.EVNT.e2355/',
	  'mc12_8TeV.147310.Sherpa_CT10_Wmunu_CKKW30.evgen.EVNT.e1805/',
	  'mc12_8TeV.147311.Sherpa_CT10_Wmunu_CKKW30_MjjFilt.evgen.EVNT.e1805/',
	  'mc12_8TeV.147312.Sherpa_CT10_Wmunu_MuFdown.evgen.EVNT.e2355/',
	  'mc12_8TeV.147313.Sherpa_CT10_Wmunu_MuFdown_MjjFilt.evgen.EVNT.e2355/',
	  'mc12_8TeV.147314.Sherpa_CT10_Wmunu_MuFup.evgen.EVNT.e2355/',
	  'mc12_8TeV.147315.Sherpa_CT10_Wmunu_MuFup_MjjFilt.evgen.EVNT.e2355/',
	  'mc12_8TeV.147316.Sherpa_CT10_Wmunu_mpi1.evgen.EVNT.e1805/',
	  'mc12_8TeV.147317.Sherpa_CT10_Wmunu_mpi1_MjjFilt.evgen.EVNT.e1805/',
	  'mc12_8TeV.147318.Sherpa_CT10_Wmunu_mpi2.evgen.EVNT.e1805/',
	  'mc12_8TeV.147319.Sherpa_CT10_Wmunu_mpi2_MjjFilt.evgen.EVNT.e1805/',
	  'mc12_8TeV.147320.Sherpa_CT10_Wmunu_Shower1.evgen.EVNT.e1805/',
	  'mc12_8TeV.147321.Sherpa_CT10_Wmunu_Shower1_MjjFilt.evgen.EVNT.e1805/',
	  'mc12_8TeV.147322.Sherpa_CT10_Wmunu_MuRdown.evgen.EVNT.e2355/',
	  'mc12_8TeV.147323.Sherpa_CT10_Wmunu_MuRdown_MjjFilt.evgen.EVNT.e2355/',
	  'mc12_8TeV.147324.Sherpa_CT10_Wmunu_MuRup.evgen.EVNT.e2355/',
	  'mc12_8TeV.147325.Sherpa_CT10_Wmunu_MuRup_MjjFilt.evgen.EVNT.e2355/',
	  'mc12_8TeV.147775.Sherpa_CT10_Wmunu.evgen.EVNT.e1434/',
      'mc12_7TeV.185930.PowhegPythia8_AU2_CT10_W2Jets_Wm_el_Nominal.evgen.EVNT.e3254/',
      'mc12_7TeV.185931.PowhegPythia8_AU2_CT10_W2Jets_Wp_el_Nominal.evgen.EVNT.e3254/',
      'mc12_7TeV.185932.PowhegPythia8_AU2_CT10_W2Jets_Wm_mu_Nominal.evgen.EVNT.e3254/',
      'mc12_7TeV.185933.PowhegPythia8_AU2_CT10_W2Jets_Wm_mu_MuFdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185934.PowhegPythia8_AU2_CT10_W2Jets_Wm_mu_MuFup.evgen.EVNT.e3254/',
      'mc12_7TeV.185935.PowhegPythia8_AU2_CT10_W2Jets_Wm_mu_MuRdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185936.PowhegPythia8_AU2_CT10_W2Jets_Wm_mu_MuRup.evgen.EVNT.e3254/',
      'mc12_7TeV.185937.PowhegPythia8_AU2_CT10_W2Jets_Wm_mu_MuRFdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185938.PowhegPythia8_AU2_CT10_W2Jets_Wm_mu_MuRFup.evgen.EVNT.e3254/',
      'mc12_7TeV.185939.PowhegPythia8_AU2_CT10_W2Jets_Wp_mu_Nominal.evgen.EVNT.e3254/',
      'mc12_7TeV.185940.PowhegPythia8_AU2_CT10_W2Jets_Wp_mu_MuFdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185941.PowhegPythia8_AU2_CT10_W2Jets_Wp_mu_MuFup.evgen.EVNT.e3254/',
      'mc12_7TeV.185942.PowhegPythia8_AU2_CT10_W2Jets_Wp_mu_MuRdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185943.PowhegPythia8_AU2_CT10_W2Jets_Wp_mu_MuRup.evgen.EVNT.e3254/',
      'mc12_7TeV.185944.PowhegPythia8_AU2_CT10_W2Jets_Wp_mu_MuRFdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185945.PowhegPythia8_AU2_CT10_W2Jets_Wp_mu_MuRFup.evgen.EVNT.e3254/',
      'mc12_7TeV.185946.PowhegPythia8_AU2_CT10_VBF_Wm_el_Nominal.evgen.EVNT.e3254/',
      'mc12_7TeV.185947.PowhegPythia8_AU2_CT10_VBF_Wp_el_Nominal.evgen.EVNT.e3254/',
      'mc12_7TeV.185948.PowhegPythia8_AU2_CT10_VBF_Wm_mu_Nominal.evgen.EVNT.e3254/',
      'mc12_7TeV.185949.PowhegPythia8_AU2_CT10_VBF_Wm_mu_MuFdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185950.PowhegPythia8_AU2_CT10_VBF_Wm_mu_MuFup.evgen.EVNT.e3254/',
      'mc12_7TeV.185951.PowhegPythia8_AU2_CT10_VBF_Wm_mu_MuRdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185952.PowhegPythia8_AU2_CT10_VBF_Wm_mu_MuRup.evgen.EVNT.e3254/',
      'mc12_7TeV.185953.PowhegPythia8_AU2_CT10_VBF_Wm_mu_MuRFdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185954.PowhegPythia8_AU2_CT10_VBF_Wm_mu_MuRFup.evgen.EVNT.e3254/',
      'mc12_7TeV.185955.PowhegPythia8_AU2_CT10_VBF_Wp_mu_Nominal.evgen.EVNT.e3254/',
      'mc12_7TeV.185956.PowhegPythia8_AU2_CT10_VBF_Wp_mu_MuFdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185957.PowhegPythia8_AU2_CT10_VBF_Wp_mu_MuFup.evgen.EVNT.e3254/',
      'mc12_7TeV.185958.PowhegPythia8_AU2_CT10_VBF_Wp_mu_MuRdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185959.PowhegPythia8_AU2_CT10_VBF_Wp_mu_MuRup.evgen.EVNT.e3254/',
      'mc12_7TeV.185960.PowhegPythia8_AU2_CT10_VBF_Wp_mu_MuRFdown.evgen.EVNT.e3254/',
      'mc12_7TeV.185961.PowhegPythia8_AU2_CT10_VBF_Wp_mu_MuRFup.evgen.EVNT.e3254/',
      'mc12_8TeV.185696.PowhegPythia8_AU2_CT10_W2Jets_Wm_Nominal.evgen.EVNT.e2965/',
      'mc12_8TeV.185697.PowhegPythia8_AU2_CT10_W2Jets_Wm_MuFdown.evgen.EVNT.e2965/',
      'mc12_8TeV.185698.PowhegPythia8_AU2_CT10_W2Jets_Wm_MuFup.evgen.EVNT.e2965/',
      'mc12_8TeV.185699.PowhegPythia8_AU2_CT10_W2Jets_Wm_MuRdown.evgen.EVNT.e2965/',
      'mc12_8TeV.185700.PowhegPythia8_AU2_CT10_W2Jets_Wm_MuRup.evgen.EVNT.e2965/',
      'mc12_8TeV.185701.PowhegPythia8_AU2_CT10_W2Jets_Wm_MuRFdown.evgen.EVNT.e2965/',
      'mc12_8TeV.185702.PowhegPythia8_AU2_CT10_W2Jets_Wm_MuRFup.evgen.EVNT.e2965/',
      'mc12_8TeV.185703.PowhegPythia8_AU2_CT10_W2Jets_Wp_Nominal.evgen.EVNT.e2965/',
      'mc12_8TeV.185704.PowhegPythia8_AU2_CT10_W2Jets_Wp_MuFdown.evgen.EVNT.e2973/',
      'mc12_8TeV.185705.PowhegPythia8_AU2_CT10_W2Jets_Wp_MuFup.evgen.EVNT.e2965/',
      'mc12_8TeV.185706.PowhegPythia8_AU2_CT10_W2Jets_Wp_MuRdown.evgen.EVNT.e2965/',
      'mc12_8TeV.185707.PowhegPythia8_AU2_CT10_W2Jets_Wp_MuRup.evgen.EVNT.e2965/',
      'mc12_8TeV.185708.PowhegPythia8_AU2_CT10_W2Jets_Wp_MuRFdown.evgen.EVNT.e3118/',
      'mc12_8TeV.185709.PowhegPythia8_AU2_CT10_W2Jets_Wp_MuRFup.evgen.EVNT.e2965/',
      'mc12_8TeV.185836.PowhegPythia8_AU2_CT10_W2Jets_Wm_Nominal.evgen.EVNT.e3115',
      'mc12_8TeV.185837.PowhegPythia8_AU2_CT10_W2Jets_Wp_Nominal.evgen.EVNT.e3115/',
      'mc12_8TeV.185847.PowhegPythia8_AU2_CT10_VBF_Wm_Nominal.evgen.EVNT.e3163/',
      'mc12_8TeV.185848.PowhegPythia8_AU2_CT10_VBF_Wp_Nominal.evgen.EVNT.e3163/',
      'mc12_8TeV.185849.PowhegPythia8_AU2_CT10_VBF_Wm_Nominal.evgen.EVNT.e3163/',
      'mc12_8TeV.185850.PowhegPythia8_AU2_CT10_VBF_Wm_MuFdown.evgen.EVNT.e3163/',
      'mc12_8TeV.185851.PowhegPythia8_AU2_CT10_VBF_Wm_MuFup.evgen.EVNT.e3163/',
      'mc12_8TeV.185852.PowhegPythia8_AU2_CT10_VBF_Wm_MuRdown.evgen.EVNT.e3163/',
      'mc12_8TeV.185853.PowhegPythia8_AU2_CT10_VBF_Wm_MuRup.evgen.EVNT.e3163/',
      'mc12_8TeV.185854.PowhegPythia8_AU2_CT10_VBF_Wm_MuRdownMuFdown.evgen.EVNT.e3163/',
      'mc12_8TeV.185855.PowhegPythia8_AU2_CT10_VBF_Wm_MuRupMuFup.evgen.EVNT.e3163/',
      'mc12_8TeV.185856.PowhegPythia8_AU2_CT10_VBF_Wp_Nominal.evgen.EVNT.e3163/',
      'mc12_8TeV.185857.PowhegPythia8_AU2_CT10_VBF_Wp_MuFdown.evgen.EVNT.e3163/',
      'mc12_8TeV.185858.PowhegPythia8_AU2_CT10_VBF_Wp_MuFup.evgen.EVNT.e3163/',
      'mc12_8TeV.185859.PowhegPythia8_AU2_CT10_VBF_Wp_MuRdown.evgen.EVNT.e3163/',
      'mc12_8TeV.185860.PowhegPythia8_AU2_CT10_VBF_Wp_MuRup.evgen.EVNT.e3163/',
      'mc12_8TeV.185861.PowhegPythia8_AU2_CT10_VBF_Wp_MuRdownMuFdown.evgen.EVNT.e3163/',
      'mc12_8TeV.185862.PowhegPythia8_AU2_CT10_VBF_Wp_MuRupMuFup.evgen.EVNT.e3163/',
      'mc12_8TeV.147550.Sherpa_CT10_Wenu2JetsEW1JetQCD15GeV_filt.evgen.EVNT.e2030/',        # Diboson Sample
      'mc12_8TeV.147774.Sherpa_CT10_Wenu.evgen.EVNT.e1434/',
      'mc12_8TeV.129915.Sherpa_CT10_Wenu2JetsEW1JetQCD15GeV_min_n_tchannels.evgen.EVNT.e1557/',
      'mc12_8TeV.129929.Sherpa_CT10_Wenu_MjjFiltered.evgen.EVNT.e1538/',
      'mc12_valid.200900.Sherpa_CT10_Wenu.evgen.EVNT.e2505/']
	      
    dataset_number = ['129916','129930','147294','147295','147296',
              '147297','147298','147299','147300','147301','147302',
              '147303','147304','147305','147306','147307','147308',
              '147309','147310','147311','147312','147313','147314',
              '147315','147316','147317','147318','147319','147320',
              '147321','147322','147323','147324','147325','147775',
              '185930','185931','185932','185933','185934','185935','185936',
              '185937','185938','185939','185940','185941','185942','185943',
              '185944','185945','185946','185947','185948','185949','185950',
              '185951','185952','185953','185954','185955','185956','185957',
              '185958','185959','185960','185961',
              '185696','185697','185698','185699','185700','185701','185702',
              '185703','185704','185705','185706','185707','185708','185709',
              '185836','185837','185847','185848','185849','185850','185851',
              '185852','185853','185854','185855','185856','185857','185858',
              '185859','185860','185861','185862',
              '147550','147774','129915','129929','200900',
              '000001','000002','000003','000004','000005','000006','000007',
              '000008','000009','000010','000011','000012','000013','000014',
              '000015','000016','000017','000018','000019','000020','000021',
              '000022','000023','000024','000025','000026','000027','000028',
              '000029','000030','000031','000032','000033','000034']
    
    # List of Cross-sections and Generator Filter Efficiencies (xsec,effic)          
    cross_sections = [(4.2128, 1.0), (11866.0, 0.41371), (4.0071, 1.0), (4.0065, 0.54318), 
                      (4.3523, 1.0), (4.3563, 0.54952), (4.0461, 1.0), (4.0593, 0.53842),
                      (4.2188, 1.0), (4.2135, 0.54688), (4.2072, 1.0), (4.2148, 0.54514),
                      (4.2158, 1.0), (4.2201, 0.54904), (4.7407, 1.0), (4.75, 0.54916),
                      (3.8679, 1.0), (3.8726, 0.54682), (11711.0, 1.0), (11705.0, 0.3935),
                      (11215.0, 1.0), (11208.0, 0.42849), (12308.0, 1.0), (12303.0, 0.45837),
                      (11864.0, 1.0), (11866.0, 0.4209), (11871.0, 1.0), (11864.0, 0.43504),
                      (11865.0, 1.0), (11865.0, 0.43722), (12985.0, 1.0), (12977.0, 0.41737),
                      (11971.0, 1.0), (11964.0, 0.42458), (11867.0, 1.0),
                      
                      (2019.1, 1.0), (2630.5, 1.0), (1479.5, 1.0), (1391.1, 1.0),
                      (1501.0, 1.0), (1704.4, 1.0), (1512.7, 1.0), (1167.6, 1.0),
                      (1576.9, 1.0), (3136.7, 1.0), (3107.3, 1.0), (3688.3, 1.0),
                      (3456.8, 1.0), (2929.0, 1.0), (3672.5, 1.0), (3075.8, 1.0),
                      (1.0440, 1.0), (1.6810, 1.0), (1.0440, 1.0), (1.0474, 1.0),
                      (1.0466, 1.0), (1.0446, 1.0), (1.0433, 1.0), (1.0437, 1.0),
                      (1.0420, 1.0), (1.6810, 1.0), (1.6870, 1.0), (1.6839, 1.0),
                      (1.6800, 1.0), (1.6809, 1.0), (1.6784, 1.0), (1.6774, 1.0),
                      
                      (2612.8, 1.0), (2463.5, 1.0), (2633.8, 1.0), (2708.8, 1.0),
                      (2233.6, 1.0), (2652.3, 1.0), (2391.0, 1.0),
                      (2895.8, 1.0), (2909.5, 1.0), (2932.0, 1.0), (3024.7, 1.0),
                      (2708.5, 1.0), (3004.3, 1.0), (2703.5,1.0),
                      (2440.0, 1.0), (2899.8, 1.0),
                      (1.3378, 1.0), (2.1100, 1.0), (1.3378, 1.0), (1.3411, 1.0),
                      (1.3418, 1.0), (1.3381, 1.0), (1.3372, 1.0), (1.3369, 1.0),
                      (1.3369, 1.0), (2.1100, 1.0), (2.1166, 1.0), (2.1154, 1.0),
                      (2.1089, 1.0), (2.1110, 1.0), (2.1069, 1.0), (2.1087, 1.0),
                      
                      (11.641, 0.51349), (11866.0,1.0), (4.2114,1.0), (11866.0,1.0), (11506.0,1.0), 
                      
                      (2612.8+2895.8, 1.0), (2463.5+2909.5, 1.0), (2633.8+2932.0, 1.0), (2708.8+3024.7, 1.0),
                      (2233.6+2708.5, 1.0), (2652.3+3004.3, 1.0), (2391.0+2703.5, 1.0),
                      
                      (1479.5+3136.7, 1.0), (1391.1+3107.3, 1.0), (1501.0+3688.3, 1.0), (1704.4+3456.8, 1.0),
                      (1512.7+2929.0, 1.0), (1167.6+3672.5, 1.0), (1576.9+3075.8, 1.0),
                      
                      (1.3378+2.1100, 1.0), (1.3411+2.1166, 1.0), (1.3418+2.1154, 1.0), (1.3381+2.1089, 1.0),
                      (1.3372+2.1110, 1.0), (1.3369+2.1069, 1.0), (1.3369+2.1087, 1.0),
                  
                      (1.0440+1.6810, 1.0), (1.0474+1.6870, 1.0), (1.0466+1.6839, 1.0), (1.0446+1.6800, 1.0),
                      (1.0433+1.6809, 1.0), (1.0437+1.6784, 1.0), (1.0420+1.6774, 1.0),
                  
                      (2440.0+2899.8, 1.0), (1.3378+2.1100, 1.0), (2019.1+2630.5, 1.0), (1.0440+1.6810, 1.0),
                      (3539.20+3652.67, 1.0), (2.11001+1.33757, 1.0)]
                      
                      # (2.628075, 1.0), (2.628075, 1.0), (7191.86534513, 1.0),
                      # (6648.65296181, 1.0), (7296.62835667, 1.0), (7410.79316717, 1.0), (7407.27818743, 1.0),
                      # (7191.86534513, 1.0), (7095.81150725, 1.0), (7285.89654071, 1.0), (2440.0+2899.8, 1.0),
                      # (3.44758708752, 1.0), (1.3378+2.1100, 1.0)

    dataset_names = ["129916.Nominal_Sherpa_Signal", "129930.Nominal_Sherpa_Background_MjjFilt",
              "147294.min_n_tchannels_CKKW30", "147295.min_n_tchannels_CKKW30_MjjFilt",
	      "147296.min_n_tchannels_MuFdown", "147297.min_n_tchannels_MuFdown_MjjFilt",
	      "147298.min_n_tchannels_MuFup", "147299.min_n_tchannels_MuFup_MjjFilt",
	      "147300.min_n_tchannels_mpi1", "147301.min_n_tchannels_mpi1_MjjFilt",
	      "147302.min_n_tchannels_mpi2", "147303.min_n_tchannels_mpi2_MjjFilt",
	      "147304.min_n_tchannels_Shower1", "147305.min_n_tchannels_Shower1_MjjFilt",
	      "147306.min_n_tchannels_MuRdown", "147307.min_n_tchannels_MuRdown_MjjFilt",
	      "147308.min_n_tchannels_MuRup", "147309.min_n_tchannels_MuRup_MjjFilt",
	      "147310.CKKW30", "147311.CKKW30_MjjFilt", "147312.MuFdown", "147313.MuFdown_MjjFilt",
	      "147314.MuFup", "147315.MuFup_MjjFilt", "147316.mpi1", "147317.mpi1_MjjFilt",
	      "147318.mpi2", "147319.mpi2_MjjFilt", "147320.Shower1", "147321.Shower1_MjjFilt",
	      "147322.MuRdown", "147323.MuRdown_MjjFilt", "147324.MuRup", "147325.MuRup_MjjFilt", 
          "147775.Nominal_Sherpa_Background",
          
          "185930.PowhegPythia8_W2Jets_Wm_el_Nominal.7TeV", "185931.PowhegPythia8_W2Jets_Wp_el_Nominal.7TeV",
          "185932.PowhegPythia8_W2Jets_Wm_mu_Nominal.7TeV", "185933.PowhegPythia8_W2Jets_Wm_mu_MuFdown.7TeV",
          "185934.PowhegPythia8_W2Jets_Wm_mu_MuFup.7TeV", "185935.PowhegPythia8_W2Jets_Wm_mu_MuRdown.7TeV",
          "185936.PowhegPythia8_W2Jets_Wm_mu_MuRup.7TeV", "185937.PowhegPythia8_W2Jets_Wm_mu_MuRFdown.7TeV",
          "185938.PowhegPythia8_W2Jets_Wm_mu_MuRFup.7TeV", "185939.PowhegPythia8_W2Jets_Wp_mu_Nominal.7TeV",
          "185940.PowhegPythia8_W2Jets_Wp_mu_MuFdown.7TeV", "185941.PowhegPythia8_W2Jets_Wp_mu_MuFup.7TeV",
          "185942.PowhegPythia8_W2Jets_Wp_mu_MuRdown.7TeV", "185943.PowhegPythia8_W2Jets_Wp_mu_MuRup.7TeV",
          "185944.PowhegPythia8_W2Jets_Wp_mu_MuRFdown.7TeV", "185945.PowhegPythia8_W2Jets_Wp_mu_MuRFup.7TeV",
          "185946.PowhegPythia8_VBF_Wm_el_Nominal.7TeV", "185947.PowhegPythia8_VBF_Wp_el_Nominal.7TeV",
          "185948.PowhegPythia8_VBF_Wm_mu_Nominal.7TeV", "185949.PowhegPythia8_VBF_Wm_mu_MuFdown.7TeV",
          "185950.PowhegPythia8_VBF_Wm_mu_MuFup.7TeV", "185951.PowhegPythia8_VBF_Wm_mu_MuRdown.7TeV",
          "185952.PowhegPythia8_VBF_Wm_mu_MuRup.7TeV", "185953.PowhegPythia8_VBF_Wm_mu_MuRFdown.7TeV",
          "185954.PowhegPythia8_VBF_Wm_mu_MuRFup.7TeV", "185955.PowhegPythia8_VBF_Wp_mu_Nominal.7TeV",
          "185956.PowhegPythia8_VBF_Wp_mu_MuFdown.7TeV", "185957.PowhegPythia8_VBF_Wp_mu_MuFup.7TeV",
          "185958.PowhegPythia8_VBF_Wp_mu_MuRdown.7TeV", "185959.PowhegPythia8_VBF_Wp_mu_MuRup.7TeV",
          "185960.PowhegPythia8_VBF_Wp_mu_MuRFdown.7TeV", "185961.PowhegPythia8_VBF_Wp_mu_MuRFup.7TeV",
          
          "185696.PowhegPythia8_Wm_Nominal", "185697.PowhegPythia8_Wm_MuFdown", "185698.PowhegPythia8_Wm_MuFup",
          "185699.PowhegPythia8_Wm_MuRdown", "185700.PowhegPythia8_Wm_MuRup", "185701.PowhegPythia8_Wm_MuRFdown",
          "185702.PowhegPythia8_Wm_MuRFup", "185703.PowhegPythia8_Wp_Nominal", "185704.PowhegPythia8_Wp_MuFdown",
          "185705.PowhegPythia8_Wp_MuFup", "185706.PowhegPythia8_Wp_MuRdown", "185707.PowhegPythia8_Wp_MuRup",
          "185708.PowhegPythia8_Wp_MuRFdown", "185709.PowhegPythia8_Wp_MuRFup",
          "185836.PowhegPythia8_Wm_Nominal_elec", "185837.PowhegPythia8_Wp_Nominal_elec",
          "185847.PowhegPythia8.VBF_Wm_Nominal_elec", "185848.PowhegPythia8.VBF_Wp_Nominal_elec",
          "185849.PowhegPythia8.VBF_Wm_Nominal", "185850.PowhegPythia8.VBF_Wm_MuFdown",
          "185851.PowhegPythia8.VBF_Wm_MuFup", "185852.PowhegPythia8.VBF_Wm_MuRdown",
          "185853.PowhegPythia8.VBF_Wm_MuRup","185854.PowhegPythia8.VBF_Wm_MuRdownMuFdown",
          "185855.PowhegPythia8.VBF_Wm_MuRupMuFup", "185856.PowhegPythia8.VBF_Wp_Nominal",
          "185857.PowhegPythia8.VBF_Wp_MuFdown", "185858.PowhegPythia8.VBF_Wp_MuFup",
          "185859.PowhegPythia8.VBF_Wp_MuRdown", "185860.PowhegPythia8.VBF_Wp_MuRup",
          "185861.PowhegPythia8.VBF_Wp_MuRdownMuFdown", "185862.PowhegPythia8.VBF_Wp_MuRupMuFup",
          
          "147550.Wenu2JetsEW1JetQCD15GeV_filt", "147774.Nominal_Sherpa_Bkgd_enu", "129915.Nominal_Sherpa_Sgnl_enu",
          "129929.Nominal_Sherpa_Bkgd_enu_MjjFilt", "200900.Nominal_Sherpa_NLO_Bkgd_enu",
          
          "000001.Powheg.W2jets.Nominal.bornsuppfact", "000002.Powheg.W2jets.MuFdown.bornsuppfact", 
          "000003.Powheg.W2jets.MuFup.bornsuppfact", "000004.Powheg.W2jets.MuRdown.bornsuppfact", 
          "000005.Powheg.W2jets.MuRup.bornsuppfact", "000006.Powheg.W2jets.MuRdownMuFdown.bornsuppfact", 
          "000007.Powheg.W2jets.MuRupMuFup.bornsuppfact",
          
          "000008.Powheg.W2jets.Nominal.7TeV", "000009.Powheg.W2jets.MuFdown.7TeV",
          "000010.Powheg.W2jets.MuFup.7TeV", "000011.Powheg.W2jets.MuRdown.7TeV",
          "000012.Powheg.W2jets.MuRup.7TeV", "000013.Powheg.W2jets.MuRdownMuFdown.7TeV",
          "000014.Powheg.W2jets.MuRupMuFup.7TeV",
          
          "000015.Powheg.VBF.Nominal.ptj_gencut", "000016.Powheg.VBF.MuFdown.ptj_gencut",
          "000017.Powheg.VBF.MuFup.ptj_gencut", "000018.Powheg.VBF.MuRdown.ptj_gencut",
          "000019.Powheg.VBF.MuRup.ptj_gencut", "000020.Powheg.VBF.MuRdownMuFdown.ptj_gencut",
          "000021.Powheg.VBF.MuRupMuFup.ptj_gencut",
      
          "000022.Powheg.VBF.Nominal.7TeV", "000023.Powheg.VBF.MuFdown.7TeV",
          "000024.Powheg.VBF.MuFup.7TeV", "000025.Powheg.VBF.MuRdown.7TeV",
          "000026.Powheg.VBF.MuRup.7TeV", "000027.Powheg.VBF.MuRdownMuFdown.7TeV",
          "000028.Powheg.VBF.MuRupMuFup.7TeV",
      
          "000029.Powheg.W2jets.Nominal.electron", "000030.Powheg.VBFW.electron",
          "000031.Powheg.W2jets.Nominal.electron.7TeV", "000032.Powheg.VBFW.electron.7TeV",
          "000033.Powheg.W2jets.Hpp", "000034.Powheg.VBF.Hpp"]
          
          # "000022.Powheg.VBF.Nominal.ptj_gencut_7TeV", "000023.Powheg.VBF.Nominal.7TeV_noshower", "000024.Powheg.W2jets.Nominal.bornsuppfact.Hpp",
          # "000025.Powheg.W2jets.Nominal.CT10as", "000026.Powheg.W2jets.Nominal.NNPDF23_as_118", "000027.Powheg.W2jets.Nominal.MSTW2008nlo68cl",
          # "000028.Powheg.W2jets.Nominal.MSTW2008nlo90cl", "000029.Powheg.W2jets.Nominal.CT10", "000030.Powheg.W2jets.Nominal.CT10117",
          # "000031.Powheg.W2jets.Nominal.CT10119", "000032.Powheg.W2jets.Nominal.electron", "000033.Powheg.VBF.Nominal.Hpp",
          # "000034.Powheg.VBFW.electron"

    dataset_names_1 = ["147294.min_n_tchannels_CKKW30", "147295.min_n_tchannels_CKKW30_MjjFilt",
			"147296.min_n_tchannels_MuFdown", "147297.min_n_tchannels_MuFdown_MjjFilt",
			"147298.min_n_tchannels_MuFup", "147299.min_n_tchannels_MuFup_MjjFilt",
			"147300.min_n_tchannels_mpi1", "147301.min_n_tchannels_mpi1_MjjFilt",
			"147302.min_n_tchannels_mpi2", "147303.min_n_tchannels_mpi2_MjjFilt",
			"147304.min_n_tchannels_Shower1", "147305.min_n_tchannels_Shower1_MjjFilt",
			"147306.min_n_tchannels_MuRdown", "147307.min_n_tchannels_MuRdown_MjjFilt",
			"147308.min_n_tchannels_MuRup", "147309.min_n_tchannels_MuRup_MjjFilt"]

    dataset_names_2 = ["147775.Nominal_Sherpa_Background", "129930.Nominal_Sherpa_Background_MjjFilt","147310.CKKW30",
            "147311.CKKW30_MjjFilt", "147312.MuFdown", "147313.MuFdown_MjjFilt",
			"147314.MuFup", "147315.MuFup_MjjFilt", "147316.mpi1", "147317.mpi1_MjjFilt",
			"147318.mpi2", "147319.mpi2_MjjFilt", "147320.Shower1", "147321.Shower1_MjjFilt",
			"147322.MuRdown", "147323.MuRdown_MjjFilt", "147324.MuRup", "147325.MuRup_MjjFilt"]

    datasets_sig = 	["129916.Nominal_Sherpa_Signal", "147294.min_n_tchannels_CKKW30","147296.min_n_tchannels_MuFdown",
		      "147298.min_n_tchannels_MuFup", "147300.min_n_tchannels_mpi1","147302.min_n_tchannels_mpi2",
		      "147304.min_n_tchannels_Shower1", "147306.min_n_tchannels_MuRdown","147308.min_n_tchannels_MuRup"]
		
    datasets_sig_MjjFilt = ["129916.Nominal_Sherpa_Signal", "147295.min_n_tchannels_CKKW30_MjjFilt","147297.min_n_tchannels_MuFdown_MjjFilt","147299.min_n_tchannels_MuFup_MjjFilt",
			    "147301.min_n_tchannels_mpi1_MjjFilt","147303.min_n_tchannels_mpi2_MjjFilt","147305.min_n_tchannels_Shower1_MjjFilt",
			    "147307.min_n_tchannels_MuRdown_MjjFilt","147309.min_n_tchannels_MuRup_MjjFilt"]

    datasets_back_MjjFilt = ["129930.Nominal_Sherpa_Background_MjjFilt", "147311.CKKW30_MjjFilt","147313.MuFdown_MjjFilt","147315.MuFup_MjjFilt","147317.mpi1_MjjFilt",
			      "147319.mpi2_MjjFilt","147321.Shower1_MjjFilt","147323.MuRdown_MjjFilt","147325.MuRup_MjjFilt"]

    datasets_back = ["147775.Nominal_Sherpa_Background", "147310.CKKW30", "147312.MuFdown", "147314.MuFup", 
		          "147316.mpi1", "147318.mpi2", "147320.Shower1", "147322.MuRdown", "147324.MuRup"]
                  
    pwhg_sig_ptjgencut = ["000015.Powheg.VBF.Nominal.ptj_gencut", "000016.Powheg.VBF.MuFdown.ptj_gencut", "000017.Powheg.VBF.MuFup.ptj_gencut",
                         "000018.Powheg.VBF.MuRdown.ptj_gencut", "000019.Powheg.VBF.MuRup.ptj_gencut", "000020.Powheg.VBF.MuRdownMuFdown.ptj_gencut",
                         "000021.Powheg.VBF.MuRupMuFup.ptj_gencut", "000022.Powheg.VBF.Nominal.ptj_gencut_7TeV", "000023.Powheg.VBF.Nominal.7TeV_noshower"]
    
    pwhg_sig_bornsupp = ["000008.Powheg.VBF.Nominal.bornsuppfact", "000009.Powheg.VBF.MuFdown.bornsuppfact", "000010.Powheg.VBF.MuFup.bornsuppfact",
                         "000011.Powheg.VBF.MuRdown.bornsuppfact", "000012.Powheg.VBF.MuRup.bornsuppfact", "000013.Powheg.VBF.MuRdownMuFdown.bornsuppfact",
                         "000014.Powheg.VBF.MuRupMuFup.bornsuppfact"]
                          
    pwhg_back_bornsupp = ["000001.Powheg.W2jets.Nominal.bornsuppfact", "000002.Powheg.W2jets.MuFdown.bornsuppfact", 
                          "000003.Powheg.W2jets.MuFup.bornsuppfact", "000004.Powheg.W2jets.MuRdown.bornsuppfact", "000005.Powheg.W2jets.MuRup.bornsuppfact", 
                          "000006.Powheg.W2jets.MuRdownMuFdown.bornsuppfact", "000007.Powheg.W2jets.MuRupMuFup.bornsuppfact",
                          "000024.Powheg.W2jets.Nominal.bornsuppfact.Hpp", "000025.Powheg.W2jets.Nominal.CT10as", "000026.Powheg.W2jets.Nominal.NNPDF23_as_118",
                          "000027.Powheg.W2jets.Nominal.MSTW2008nlo68cl", "000028.Powheg.W2jets.Nominal.MSTW2008nlo90cl"]

    exp_hist_list = ["d01-x01-y01", "d01-x01-y02", "d02-x01-y01", "d02-x01-y02",
		      "d03-x01-y01", "d03-x01-y02", "d04-x01-y01", "d04-x01-y02",
		      "d05-x01-y01", "d05-x01-y02", "d06-x01-y01", "d06-x01-y02",
		      "d07-x01-y01", "d07-x01-y02", "d08-x01-y01", "d08-x01-y02",
		      "d09-x01-y01", "d09-x01-y02", "d10-x01-y01", "d10-x01-y02",
		      "d11-x01-y01", "d11-x01-y02", "d12-x01-y01", "d12-x01-y02",
		      "d13-x01-y01", "d13-x01-y02", "d14-x01-y01", "d14-x01-y02",
		      "d15-x01-y01", "d15-x01-y02", "d16-x01-y01", "d16-x01-y02",
		      "d17-x01-y01", "d17-x01-y02", "d18-x01-y01", "d18-x01-y02",
		      "d19-x01-y01", "d19-x01-y02", "d20-x01-y01", "d20-x01-y02",
		      "d21-x01-y01", "d21-x01-y02", "d22-x01-y01", "d22-x01-y02",
		      "d23-x01-y01", "d23-x01-y02", "d24-x01-y01", "d24-x01-y02",
		      "d25-x01-y01", "d25-x01-y02"]

    hist_list = ["NJetExcl_1", "FirstJetPt_2jet_1", "FirstJetPt_3jet_1", "FirstJetPt_4jet_1", "SecondJetPt_2jet_1",
		  "SecondJetPt_3jet_1", "SecondJetPt_4jet_1", "ThirdJetPt_3jet_1","ThirdJetPt_4jet_1", "FourthJetPt_4jet_1",
          "Ht_2jet_1", "Ht_3jet_1", "Ht_4jet_1", "Minv_2jet_1", "Minv_3jet_1", "Minv_4jet_1", "JetRapidity_1", "DeltaYElecJet_1",
          "SumYElecJet_1", "DeltaR_2jet_1", "DeltaY_2jet_1", "DeltaPhi_2jet_1", "DijetMass_2jet_1", "DijetMass_3jet_1",
		  "DijetMass_4jet_1", "AntiDijetMass_2jet_1", "AntiDijetMass_3jet_1", "AntiDijetMass_4jet_1", "ThirdZep_3jet_1", "ThirdZep_4jet_1",
          "FourthZep_4jet_1", "AntiDijetEtaDiff_2jet_1", "AntiDijetEtaDiff_3jet_1", "AntiDijetEtaDiff_4jet_1", "AntiDijetPhiDiff_2jet_1",
		  "AntiDijetPhiDiff_3jet_1", "AntiDijetPhiDiff_4jet_1", "CutFlow_1", "DeltaR13_3jet_1", "DeltaR23_3jet_1", "NJetsNoCuts",
          "Mjj_Excl_00_Jet_1", "Mjj_Excl_01_Jet_1", "Mjj_Excl_02_Jet_1", "Mjj_Excl_03_Jet_1", "Mjj_Excl_04_Jet_1", "Mjj_Excl_05_Jet_1",
          "Mjj_Excl_06_Jet_1", "Mjj_Excl_07_Jet_1", "Mjj_Excl_08_Jet_1", "Mjj_Excl_09_Jet_1", "Mjj_Excl_10_Jet_1",
          "Weight_vs_pT1", "Weight_vs_pT2", "Weight_vs_Mjj", "DijetMass_nocuts", "FirstJetPt_nocuts", "SecondJetPt_nocuts",
          "BosonPt_nocuts", "WBosonPt_1", "DijetMass_CR_antiJ3C_1", "DijetMass_CR_LC_1", "DijetMass_CR_antiLC_1",
  		  "DijetMass_CR_njetgap1_1", "DijetMass_CR_njetgap2_1", "DijetMass_CR_njetgap_g2_1", "DijetMass_CR_njetgap2_1in_1",
  		  "DijetMass_CR_njetgap_g3_1in_1", "WeightCutFlow_1"]
          # "NJetExcl_2", "FirstJetPt_2jet_2", "FirstJetPt_3jet_2", "FirstJetPt_4jet_2", "SecondJetPt_2jet_2",
          # "SecondJetPt_3jet_2", "SecondJetPt_4jet_2", "ThirdJetPt_3jet_2","ThirdJetPt_4jet_2", "FourthJetPt_4jet_2",
          # "Ht_2jet_2", "Ht_3jet_2", "Ht_4jet_2", "Minv_2jet_2", "Minv_3jet_2", "Minv_4jet_2", "JetRapidity_2", "DeltaYElecJet_2",
          # "SumYElecJet_2", "DeltaR_2jet_2", "DeltaY_2jet_2", "DeltaPhi_2jet_2", "DijetMass_2jet_2", "DijetMass_3jet_2",
          # "DijetMass_4jet_2", "AntiDijetMass_2jet_2", "AntiDijetMass_3jet_2", "AntiDijetMass_4jet_2", "ThirdZep_3jet_2", "ThirdZep_4jet_2",
          # "FourthZep_4jet_2", "AntiDijetEtaDiff_2jet_2", "AntiDijetEtaDiff_3jet_2", "AntiDijetEtaDiff_4jet_2", "AntiDijetPhiDiff_2jet_2",
          # "AntiDijetPhiDiff_3jet_2", "AntiDijetPhiDiff_4jet_2", "CutFlow_2", "DeltaR13_3jet_2", "DeltaR23_3jet_2", "NJetsNoCuts",
          # "Mjj_Excl_00_Jet_2", "Mjj_Excl_01_Jet_2", "Mjj_Excl_02_Jet_2", "Mjj_Excl_03_Jet_2", "Mjj_Excl_04_Jet_2", "Mjj_Excl_05_Jet_2",
          # "Mjj_Excl_06_Jet_2", "Mjj_Excl_07_Jet_2", "Mjj_Excl_08_Jet_2", "Mjj_Excl_09_Jet_2", "Mjj_Excl_10_Jet_2",
          # "Weight_vs_pT1", "Weight_vs_pT2", "Weight_vs_Mjj", "DijetMass_nocuts", "FirstJetPt_nocuts", "SecondJetPt_nocuts",
          # "BosonPt_nocuts", "WBosonPt_2", "DijetMass_CR_antiJ3C_2", "DijetMass_CR_LC_2", "DijetMass_CR_antiLC_2"]

    title_list = ["Jet Multiplicity (W+#geq 2 jets)", "First Jet p_{T} (W+#geq 2 jets)", "First Jet p_{T} (W+#geq 3 jets)", "First Jet p_{T} (W+#geq 4 jets)",
		  "Second Jet p_{T}", "Second Jet p_{T} (W+#geq 3 jets)", "Second Jet p_{T} (W+#geq 4 jets)", "Third Jet p_{T}", "Third Jet p_{T} (W+#geq 4 jets)",
		  "Fourth Jet p_{T}", "H_{T} (W+#geq 2 jets)", "H_{T} (W+#geq 3 jets)", "H_{T} (W+#geq 4 jets)", "Jet Invariant Mass (W+ #geq 2 jets)",
		  "Jet Invariant Mass (W+ #geq 3 jets)", "Jet Invariant Mass (W+ #geq 4 jets)", "First Jet Rapidity", "Lepton-Jet Rapidity Difference", "Lepton-Jet Rapidity Sum", 
		  "#Delta R Distance of Leading Jets", "Rapidity Distance of Leading Jets", "Azimuthal Distance of Leading Jets","Dijet Mass (W+#geq 2 jets)",
		  "Dijet Mass (W+#geq 3 jets)", "Dijet Mass (W+#geq 4 jets)", "Most Forward/Rearward Dijet Mass (W+#geq 2 jets)","Most Forward/Rearward Dijet Mass (W+#geq 3 jets)",
		  "Most Forward/Rearward Dijet Mass (W+#geq 4 jets)", "Third Jet Pseudorapidity in Dijet CM (W+#geq 3 jets)", "Third Jet Pseudorapidity in Dijet CM (W+#geq 4 jets)",
		  "Fourth Jet Pseudorapidity in Dijet CM (W+#geq 4 jets)", "Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 2 jets)",
		  "Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 3 jets)", "Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 4 jets)",
		  "cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 2 jets)", "cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 3 jets)",
		  "cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 4 jets)", "Cut Flow", "Rapidity Diff b/w Jets 1 and 3", "Rapidity Diff b/w Jets 2 and 3",
          "Number of Jets in Event (No Cuts)", "Dijet Mass (#jets = 0)", "Dijet Mass (#jets = 1)", "Dijet Mass (#jets = 2)", "Dijet Mass (#jets = 3)", "Dijet Mass (#jets = 4)",
          "Dijet Mass (#jets = 5)", "Dijet Mass (#jets = 6)", "Dijet Mass (#jets = 7)", "Dijet Mass (#jets = 8)", "Dijet Mass (#jets = 9)", "Dijet Mass (#jets = 10)",
          "Weight vs Leading Jet pT", "Weight vs Second Jet pT", "Weight vs Dijet Mass", "Dijet Mass with no cuts",
          "Leading Jet pT with no cuts", "Second Jet pT no cuts", "Boson pT no cuts", "W Boson pT",
          "Dijet Mass Control Region - !J3C", "Dijet Mass Control Region - LC", "Dijet Mass Control Region - !LC",
  		  "DijetMass_CR_njetgap1_1", "DijetMass_CR_njetgap2_1", "DijetMass_CR_njetgap_g2_1", "DijetMass_CR_njetgap2_1in_1",
  		  "DijetMass_CR_njetgap_g3_1in_1", "Weigted Cut Flow"]

    x_axis_list = 	["N_{jet}", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]",
		      "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "H_{T} [GeV]", "H_{T} [GeV]", "H_{T} [GeV]",
		      "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "y", "y(Lepton)-y(First Jet)", "y(Lepton)+y(First Jet)",
		      "#Delta R(First Jet, Second Jet)", "#Delta y(First Jet, Second Jet)", "#Delta#phi(First Jet, Second Jet)",
		      "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]",
		      "#eta_{3} (Third Jet)", "#eta_{3} (Third Jet)", "#eta_{4} (Fourth Jet)","#Delta#eta_{j_1j_2}", "#Delta#eta_{j_1j_2}", 
              "#Delta#eta_{j_1j_2}", "cos|#phi_{j_1}-#phi_{j_2}|", "cos|#phi_{j_1}-#phi_{j_2}|", "cos|#phi_{j_1}-#phi_{j_2}|",
		      "Cut", "#Delta R_{1,3}", "#Delta R_{2,3}", "N_{jet}", "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]",
              "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]",
              "m(jets) [GeV]", "m(jets) [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "m(jets) [GeV]", "m(jets) [GeV]",
              "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]",
              "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "Cut"]

    y_axis_list = 	["#sigma (W+#geq N_{jet} jets) [pb]",
		      "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
		      "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
		      "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
		      "d#sigma/dH_{T} [pb/GeV]", "d#sigma/dH_{T} [pb/GeV]", "d#sigma/dH_{T} [pb/GeV]",
		      "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]",
		      "d#sigma/d#it{y} [pb]", "d#sigma/d#Delta#it{y} [pb]", "d#sigma/d#Sigma#it{y} [pb]",
		      "d#sigma/d#Delta#it{R} [pb]", "d#sigma/d#Delta#it{y} [pb]", "d#sigma/d#Delta#phi [pb]",
		      "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
		      "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
		      "d#sigma/d#eta_{3} [pb]", "d#sigma/d#eta_{3} [pb]", "d#sigma/d#eta_{4} [pb]",
		      "d#sigma/d#eta_{j_1j_2} [pb]", "d#sigma/d#eta_{j_1j_2} [pb]", "d#sigma/d#eta_{j_1j_2} [pb]",
		      "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]",
		      "[events/cut]", "[pb]", "[pb]", "[events]", "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]",
              "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]",
              "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]","d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]",
              "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
              "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
              "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
              "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
              "Weight"]

    y_axis_list_norm = ["#sigma (W+#geq N_{jet} jets)",
			"d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
			"d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
			"d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
			"d#sigma/dH_{T} [events/GeV]", "d#sigma/dH_{T} [events/GeV]", "d#sigma/dH_{T} [events/GeV]",
			"d#sigma/d#it{m} [events/GeV]","d#sigma/d#it{m} [events/GeV]", "d#sigma/d#it{m} [events/GeV]",
			"d#sigma/d#it{y} [events]", "d#sigma/d#Delta#it{y} [events]", "d#sigma/d#Sigma#it{y} [events]",
			"d#sigma/d#Delta#it{R} [events]", "d#sigma/d#Delta#it{y} [events]", "d#sigma/d#Delta#phi [events]",
			"d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]",
			"d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]",
			"d#sigma/d#eta_{3} [events]", "d#sigma/d#eta_{3} [events]", "d#sigma/d#eta_{4} [events]",
			"d#sigma/d#eta_{j_1j_2} [events]", "d#sigma/d#eta_{j_1j_2} [events]", "d#sigma/d#eta_{j_1j_2} [events]",
			"d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]",
			"[events/cut]", "[events]", "[events]", "[events]","d#sigma/d#it{m} [events/GeV]","d#sigma/d#it{m} [events/GeV]", "d#sigma/d#it{m} [events/GeV]",
            "d#sigma/d#it{m} [events/GeV]","d#sigma/d#it{m} [events/GeV]", "d#sigma/d#it{m} [events/GeV]", "d#sigma/d#it{m} [events/GeV]",
            "d#sigma/d#it{m} [events/GeV]", "d#sigma/d#it{m} [events/GeV]","d#sigma/d#it{m} [events/GeV]","d#sigma/d#it{m} [events/GeV]",
            "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]","d#sigma/dm_{jj} [events/GeV]",
            "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
            "d#sigma/dm_{jj} [events/GeV]","d#sigma/dm_{jj} [events/GeV]","d#sigma/dm_{jj} [events/GeV]",
            "d#sigma/dm_{jj} [events/GeV]","d#sigma/dm_{jj} [events/GeV]","d#sigma/dm_{jj} [events/GeV]","d#sigma/dm_{jj} [events/GeV]","d#sigma/dm_{jj} [events/GeV]",
            "Arb. Units"]

    list_of_lists = ['datasets', 'dataset_names', 'dataset_names_1', 'dataset_names_2', 'datasets_sig','datasets_sig_MjjFilt',
		             'datasets_back', 'datasets_back_MjjFilt', 'exp_hist_list', 'hist_list', 'title_list', 'x_axis_list',
		             'y_axis_list', 'y_axis_list_norm', 'dataset_number', 'cross_sections', 'pwhg_back_bornsupp', 'pwhg_sig_bornsupp',
                     'pwhg_sig_ptjgencut']

    if list_name in list_of_lists: return eval(list_name)
    else: print 'The given list is not defined.'
