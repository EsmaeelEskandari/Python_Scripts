import ROOT

# Open input files (one per decay final state)
f_ee    = ROOT.TFile.Open("hist-ee.root")
f_mumu  = ROOT.TFile.Open("hist-mumu.root")
f_emu   = ROOT.TFile.Open("hist-emu.root")

# Output file that will have merged cross-section distributions
f_out   = ROOT.TFile("hist-AllChannels.root","RECREATE")

# Cross-sections per decay channel
# Universality says xs for W->enu = W->munu
WWee_xs   = 0.024605
WWmumu_xs = WWee_xs
WWemu_xs  = 2.0*WWee_xs

# List of all histogram keys in input file
#   should be the same for each input file
histKeys = f_ee.GetListOfKeys()

# Loop over all histogram keys
# This will likely include some Cut Flows (These would inevitably be wrong
# after being scaled by cross-sections and merged)
for key in histKeys:
    # Gets the histogram name of the hist Key
    histName = key.GetName()
    
    # Gets the histogram from each input file
    hist_ee   = f_ee.Get(histName)
    hist_mumu = f_mumu.Get(histName)
    hist_emu  = f_emu.Get(histName)
    
    # Ensures that each hist does errors properly
    # Not sure if this is needed...Should already be set in RootCore
    # hist_ee.SetDefaultSumw2(1)
    # hist_mumu.SetDefaultSumw2(1)
    # hist_emu.SetDefaultSumw2(1)
    
    # Scales each histogram by ( xsec/numEvents )
    # Histograms need to be Event Distributions
    hist_ee.Scale( WWee_xs/hist_ee.Integral("width") )
    hist_mumu.Scale( WWmumu_xs/hist_mumu.Integral("width") )
    hist_emu.Scale( WWemu_xs/hist_emu.Integral("width") )
    
    # Make a clone of one histogram
    histMerged = hist_ee.Clone()
    # Add the other histograms to the clone
    histMerged.Add(hist_mumu)
    histMerged.Add(hist_emu)
    
    # Write out the xsec distribution that corresponds to all three decay channels
    histMerged.Write()
    
# Write out and close output root file
f_out.Write()
f_out.Close()

# This cross-section is to be used to normalize the distributions
# for shape comparisons
print "Total cross-section is {0} pb".format(WWee_xs+WWmumu_xs+WWemu_xs)