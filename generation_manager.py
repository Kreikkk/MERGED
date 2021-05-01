import numpy as np
import pandas as pd
import time
import ROOT as root
import pickle

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from dataloader import dataset_gen
from sys import argv
from helpers import dump, clear
from config import *


def main():
	methodname, uploadfile = argv[1:3]
	params = argv[3:]

	clear(methodname, uploadfile)

	if methodname in ("TMVA_BDT", "TMVA_MLP"):
		TMVA_gen(params, methodname, uploadfile)

	elif methodname in ("SKL_BDT", "SKL_MLP"):
		SKL_gen(params, methodname, uploadfile)

	else:
		raise ValueError(f"No method: {methodname}")


def TMVA_gen(params, methodname, uploadfile):
	fout = root.TFile(f"TMVA_outputs/{methodname}/{uploadfile}.root", "RECREATE")
	# if methodname == "TMVA_MLP":
	# 	PARAMETERS.append("Transformations=G")
	# 	# PARAMETERS.append("Transformations=I;D;P;G,D")

	factory = root.TMVA.Factory(f"TMVAClassification_{methodname}_{uploadfile}", fout, ":".join(PARAMETERS))

	dataloader = root.TMVA.DataLoader("models/dataloader")

	SFile = root.TFile("source/"+SFILENAME)
	STree = SFile.Get(TREENAME)
	dataloader.AddSignalTree(STree)

	BFile1 = root.TFile("source/"+"ZgQCD.root")
	BFile2 = root.TFile("source/"+"ttgamma.root")
	BFile3 = root.TFile("source/"+"WenuDataDriven.root")
	BFile4 = root.TFile("source/"+"Wgam.root")
	BFile5 = root.TFile("source/"+"WgamEWK.root")

	BTree1 = BFile1.Get(TREENAME)
	BTree2 = BFile2.Get(TREENAME)
	BTree3 = BFile3.Get(TREENAME)
	BTree4 = BFile4.Get(TREENAME)
	BTree5 = BFile5.Get(TREENAME)

	dataloader.AddBackgroundTree(BTree1)
	dataloader.AddBackgroundTree(BTree2)
	dataloader.AddBackgroundTree(BTree3)
	dataloader.AddBackgroundTree(BTree4)
	dataloader.AddBackgroundTree(BTree5)

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

	if USE_W:
		dataloader.SetSignalWeightExpression("weightModified")
		dataloader.SetBackgroundWeightExpression("weightModified")

	if DROP_NEGATIVE_W:
		cut = root.TCut("(nJets > 1)&&(nLeptons == 0)&&(weightModified > 0)")
	else:
		cut = root.TCut("(nJets > 1)&&(nLeptons == 0)")

	dataloader.PrepareTrainingAndTestTree(cut, ":".join(["nTrain_Signal=0",
														 "nTrain_Background=0",
														 "SplitMode=Random",
														 "NormMode=NumEvents",
														 "!V"]))


	model = root.TMVA.Types.kBDT if methodname == "TMVA_BDT" else root.TMVA.Types.kMLP

	if methodname == "TMVA_MLP":
		settings = ["!H", "!V", "VarTransform=G", "NCycles=400", "BPMode=batch",
					"TestRate=5", "!UseRegulator", "NeuronType=sigmoid",
					"ConvergenceImprove=0.0025", "ConvergenceTests=5",
					f"LearningRate={params[0]}",
					f"HiddenLayers={params[1]}",
					f"BatchSize={params[2]}",]
	
	elif methodname == "TMVA_BDT":
		settings = ["!H", "!V", "MinNodeSize=5", "BoostType=Grad",
	     			f"NTrees={params[0]}",
	     			f"nCuts={params[1]}",
	     			f"MaxDepth={params[2]}",
	     			f"shrinkage={params[3]}",]
	
	else:
		raise ValueError(f"No method name {methodname}")

	method = factory.BookMethod(dataloader, model, methodname, ":".join(settings))

	t = time.time()
	factory.TrainAllMethods()
	factory.TestAllMethods()
	factory.EvaluateAllMethods()
	fout.Close()
	dump(methodname, uploadfile, "time:"+str(round(time.time() - t))+"\n")


def SKL_gen(params, methodname, uploadfile):
	TrainDF, _ = dataset_gen(datatype=0)
	if DROP_NEGATIVE_W:
		TrainDF = TrainDF[TrainDF["weightModified"] > 0]

	print((TrainDF["weightModified"] < 0).any())
	
	train_data = np.array(TrainDF.iloc[:,:11], dtype="float64")
	labels = np.array(TrainDF.iloc[:,14], dtype="float64")
	sample_weight = np.array(TrainDF.iloc[:,12], dtype="float64")

	if methodname == "SKL_BDT":
		classifier = GradientBoostingClassifier(n_estimators=int(params[0]),
										  		max_depth=float(params[1]),
										  		learning_rate=float(params[2]),
										  		random_state=1,
										  		verbose=1)
	
	elif methodname == "SKL_MLP":
		classifier = MLPClassifier(random_state=1, verbose=True, early_stopping=True, n_iter_no_change=10, tol=0.001,
							   	   solver=params[0],
							   	   activation=params[1],
							   	   batch_size=int(params[2]),
							   	   learning_rate_init=float(params[3]),
							   	   alpha=float(params[4]),
							   	   hidden_layer_sizes=[int(el) for el in params[5].split(":")],)

	else:
		raise ValueError(f"No method name {methodname}")

	t = time.time()
	if methodname == "SKL_BDT":
		if USE_W:
			classifier.fit(train_data, labels, sample_weight=sample_weight)
		else:
			classifier.fit(train_data, labels)
	else:
		classifier.fit(train_data, labels)

	dump(methodname, uploadfile, "time:"+str(round(time.time() - t))+"\n")

	with open(f"models/{methodname}/{uploadfile}.pickle", "wb") as file:
		pickle.dump(classifier, file)


if __name__ == "__main__":
	main()