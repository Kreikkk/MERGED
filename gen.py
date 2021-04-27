import numpy as np
import ROOT as root

from sys import argv
from config import *

import time
from plotters import dump


def main(params, outputfile="output"):
	fout = root.TFile(f"outputs/{outputfile}.root", "RECREATE")
	factory = root.TMVA.Factory(f"TMVAClassification{outputfile}", fout,
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=I;D;P;G,D",
                                          "AnalysisType=Classification"]))

	dataloader = root.TMVA.DataLoader("dataloader")

	SFile = root.TFile("source/"+SFILENAME)
	STree = SFile.Get(TREENAME)
	dataloader.AddSignalTree(STree)

	BFile1 = root.TFile("source/"+"ZgQCD.root")
	BFile2 = root.TFile("source/"+"ttgamma.root")
	BFile4 = root.TFile("source/"+"WenuDataDriven.root")
	BFile5 = root.TFile("source/"+"Wgam.root")
	BFile6 = root.TFile("source/"+"WgamEWK.root")

	BTree1 = BFile1.Get(TREENAME)
	BTree2 = BFile2.Get(TREENAME)
	BTree4 = BFile4.Get(TREENAME)
	BTree5 = BFile5.Get(TREENAME)
	BTree6 = BFile6.Get(TREENAME)

	dataloader.AddBackgroundTree(BTree1)
	dataloader.AddBackgroundTree(BTree2)
	dataloader.AddBackgroundTree(BTree4)
	dataloader.AddBackgroundTree(BTree5)
	dataloader.AddBackgroundTree(BTree6)

	dataloader.AddVariable("mJJ","F")
	dataloader.AddVariable("deltaYJJ","F")
	dataloader.AddVariable("metPt","F")
	dataloader.AddVariable("ptBalance","F")
	dataloader.AddVariable("subleadJetEta","F")
	dataloader.AddVariable("leadJetPt","F")
	dataloader.AddVariable("photonEta","F")
	dataloader.AddVariable("ptBalanceRed","F")
	dataloader.AddVariable("nJets","F")
	dataloader.AddVariable("sinDeltaPhiJJOver2","F")
	dataloader.AddVariable("deltaYJPh","F")
	dataloader.AddSpectator("weightModified", "F")

	cut = root.TCut("(nJets > 1)&&(nLeptons == 0)")

	dataloader.PrepareTrainingAndTestTree(cut, ":".join(["nTrain_Signal=0",
														 "nTrain_Background=0",
														 "SplitMode=Random",
														 "NormMode=NumEvents",
														 "!V"]))

	# method = factory.BookMethod(dataloader, root.TMVA.Types.kBDT, "BDTG",
 #                            ":".join([ "!H",
 #                                       "!V",
 #                                       f"NTrees={params[0]}",
 #                                       "nEventsMin=150",
 #                                       f"MaxDepth={params[2]}",
 #                                       "BoostType=Grad",
 #                                       "SeparationType=GiniIndex",
 #                                       f"nCuts={params[1]}",
 #                                       "PruneMethod=NoPruning",
 #                                       f"shrinkage={params[3]}"
 #                                       ]))

	method = factory.BookMethod(dataloader, root.TMVA.Types.kBDT, "BDTG",
                            ":".join([ "!H",
                                       "!V",
                                       "NTrees=600",
                                       "MinNodeSize=5",
                                       "MaxDepth=3",
                                       "BoostType=Grad",
                                       "nCuts=20",
                                       "shrinkage=0.05"
                                       ]))
	# t = time.time()
	factory.TrainAllMethods()
	factory.TestAllMethods()
	factory.EvaluateAllMethods()
	fout.Close()
	# dump(outputfile, str(round(time.time() - t, 3)))


if __name__ == "__main__":
	root.TMVA.Tools.Instance()
	params = argv[2:]
	main(params, outputfile=argv[1])