from PowhegUtils import PowhegConfig_base
import os,sys,time,subprocess,shutil
from AthenaCommon import Logging
mglog = Logging.logging.getLogger('PowhegUtils')

#Test job options to see how things work.

class PowhegConfig_VBF_W_Z(PowhegConfig_base):
	# These are user configurable - put generic properties in PowhegConfig_base
	# Adjust this to resemble the powheg.input for VBF_W-Z
	#xupbound = 2d0		# increase upper bound for radiation generation
	#ptsupp = 0d0		# (default 0d0)  mass param for Born suppression factor (generation cut) If < 0 suppfact = 1
	#bornonly = 1		# (default 0) if 1 do Born only
	withdamp = 1		# (default 0, do not use) use Born-zero damping factor
	testplots = 0		# (default 0, do not) do NLO and PWHG distributions
	mll_gencut = 20.0	# Generation cut for mll
	ptj_gencut = 0.0	# Generation cut for pt of tagging jets
	bornsuppfact = 1	# use Born suppression factor
	ptsuppfact = 10.0	# Lambda_ptj for Born suppression factor
	fakevirt = 0		# (default 0.0) If 1 use Born*0.2 for generation of the grid for ncall2 = 0	

	# Set process-dependent paths in the constructor
	def __init__(self,runArgs=None):
		PowhegConfig_base.__init__(self,runArgs)
		self.executablePath += '/VBF_W-Z/pwhg_main'

	def generateRunCard(self):
		self.generateRunCardSharedOptions()

		TestArea = os.environ['TestArea']
		with open( str(TestArea)+'/powheg.input','a') as f:
			f.write( "withdamp "+str(self.withdamp)+"	! (default 0, do not use) use Born-zero damping factor\n" )
			f.write( "testplots "+str(self.testplots)+"		! (default 0, do not) do NLO and PWHG distributions\n" )
			f.write( "mll_gencut "+str(self.mll_gencut)+"	! Generation cut for mll\n" )
			f.write( "ptj_gencut "+str(self.ptj_gencut)+"	! Generation cut for pt of tagging jets\n" )
			f.write( "bornsuppfact "+str(self.bornsuppfact)+"	! use Born suppression factor\n" )
			f.write( "ptsuppfact "+str(self.ptsuppfact)+"	! Lambda_ptj for Born suppression factor\n" )
			f.write( "fakevirt "+str(self.fakevirt)+"	! (default 0.0) If 1 use Born*0.2 for generation of the grid for ncall2 = 0\n" )
			f.write( "!#---------------- CUTS FOR PLOTS ------------------------------")
			f.write( "activate_cuts = 1" )
			f.write( "ptalljetmin = 20.0" )
			f.write( "ptjetmin = 30.0" )
			f.write( "mjjmin = 500.0" )
			f.write( "deltay_jjmin = 4.0" )
			f.write( "yjetmax = 4.5" )
			f.write( "ylepmax = 2.5" )
			f.write( "ptlepmin = 20.0" )
			f.write( "mllmin = 20.0" )
			f.write( "Rllmin = 0.1" )
			f.write( "Rsep_jjmin = 0.4" )
			f.write( "Rsep_jlmin = 0.4" )
			f.write( "dely_jl = 0.2" )
			f.write( "ylep_between_jets = 1" )
			f.write( "jet_opphem = 1" )
			
		# Make the vbfnlo.input card
		with open( str(TestArea)+'/vbfnlo.input','w') as v:
			v.write( "PROC_ID   130		! pp -> Wp + 2 jets" )
			v.write( "DECAYMODE 13		! Decay into a muon" )
			v.write( "!   Physics parameters" )
			v.write( "!------------------------ " )
			v.write( "HMASS        126.0d0         ! Higgs mass" )
			v.write( "HWIDTH       -999d0          ! Higgs width" )
			v.write( "EWSCHEME     3               ! Choose scheme for electroweak parameters (1,2,3,4,5,6)" )
			v.write( "ANOM_CPL     0               ! Anomalous couplings " )
			v.write( "TOPMASS      172.4d0         ! Top mass" )
			v.write( "TAU_MASS     1.77684         ! Tau mass" )
			v.write( "BOTTOMMASS   4.855d0         ! Bottom Pole mass" )
			v.write( "CHARMMASS    1.65d0          ! Charm Pole mass " )
			v.write( "FERMI_CONST  1.16637d-5      ! Fermi Constant" )
			v.write( "INVALFA      128.944341122D0 ! 1/fine-structure constant" )
			v.write( "SIN2W        0.222646d0      ! Weak mixing angle" )
			v.write( "WMASS        80.398d0        ! W mass" )
			v.write( "ZMASS        91.1876d0       ! Z mass" )

#--------------------------------------------------------------

if 'runArgs' in dir() : 
	PowhegConfig = PowhegConfig_VBF_W_Z(runArgs)
else :
	PowhegConfig = PowhegConfig_VBF_W_Z()

#--------------------------------------------------------------

PowhegConfig.ncall1 = 1000000					# This is how I would vary the parameters from PowhegConfig_base (e.g. muF, muR)
PowhegConfig.itmx1 = 4
PowhegConfig.ncall2 = 50000
PowhegConfig.itmx2 = 3
PowhegConfig.nubound = 100000
PowhegConfig.foldy = 5
PowhegConfig.foldphi = 5
PowhegConfig.muF = 1.0
PowhegConfig.muR = 1.0
PowhegConfig.generateRunCard()
PowhegConfig.generateEvents()

#--------------------------------------------------------------
# General MC12 configuration
#--------------------------------------------------------------
from AthenaCommon.AlgSequence import AlgSequence
topAlg = AlgSequence("TopAlg")
include("MC12JobOptions/PowhegPythia8_AU2_CT10_Common.py")
include("MC12JobOptions/Pythia8_LHEF.py")

#from MC12JobOptions.EvgenConfig import evgenConfig
#evgenConfig.generators += ["lhef", "Pythia8"]
evgenConfig.description = 'POWHEG VBF_W-Z + Pythia 8 test jobs'
evgenConfig.keywords = ["SM","VBF-W"]
evgenConfig.minevents = 10

