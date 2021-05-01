SFILENAME		= "ZgEWK.root"
BFILENAMES		= ["ZgQCD.root", "ttgamma.root", "SinglePhoton.root", "WenuDataDriven.root",
				   "Wgam.root", "WgamEWK.root", "Zllgam.root", "ZnunuFromQcd.root"]
BTRAINFILENAMES	= ["ZgQCD.root", "ttgamma.root", "WenuDataDriven.root",
			   	   "Wgam.root", "WgamEWK.root"]

TREENAME = "TMVA_input"

BDTSTEP = 0.005

PARAMETERS = ["!V", "!Silent", "Color", "DrawProgressBar", "AnalysisType=Classification"]

DROP_NEGATIVE_W = True
USE_W = True