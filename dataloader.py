import uproot

import numpy as np
import pandas as pd

from config import *


def build_dataframe(tree):
	dataframe = pd.DataFrame({"mJJ":			pd.Series(np.array(tree["mJJ"].array())),
							  "deltaYJJ":		pd.Series(np.array(tree["deltaYJJ"].array())),
							  "metPt":			pd.Series(np.array(tree["metPt"].array())),
							  "ptBalance":		pd.Series(np.array(tree["ptBalance"].array())),
							  "subleadJetEta":	pd.Series(np.array(tree["subleadJetEta"].array())),
							  "leadJetPt":		pd.Series(np.array(tree["leadJetPt"].array())),
							  "photonEta":		pd.Series(np.array(tree["photonEta"].array())),
							  "ptBalanceRed":	pd.Series(np.array(tree["ptBalanceRed"].array())),
							  "nJets":			pd.Series(np.array(tree["nJets"].array())),
							  "sinDeltaPhiJJOver2": pd.Series(np.array(tree["sinDeltaPhiJJOver2"].array())),
							  "deltaYJPh":		pd.Series(np.array(tree["deltaYJPh"].array())),
							  "phCentrality":	pd.Series(np.array(tree["phCentrality"].array())),
							  "weightModified":	pd.Series(np.array(tree["weightModified"].array())),
							  "nLeptons":		pd.Series(np.array(tree["nLeptons"].array())),
							 })

	return dataframe


def build_output_dataframe(tree):
	dataframe = pd.DataFrame({"mJJ":			pd.Series(np.array(tree["mJJ"].array())),
							  "deltaYJJ":		pd.Series(np.array(tree["deltaYJJ"].array())),
							  "metPt":			pd.Series(np.array(tree["metPt"].array())),
							  "ptBalance":		pd.Series(np.array(tree["ptBalance"].array())),
							  "subleadJetEta":	pd.Series(np.array(tree["subleadJetEta"].array())),
							  "leadJetPt":		pd.Series(np.array(tree["leadJetPt"].array())),
							  "photonEta":		pd.Series(np.array(tree["photonEta"].array())),
							  "ptBalanceRed":	pd.Series(np.array(tree["ptBalanceRed"].array())),
							  "nJets":			pd.Series(np.array(tree["nJets"].array())),
							  "sinDeltaPhiJJOver2": pd.Series(np.array(tree["sinDeltaPhiJJOver2"].array())),
							  "deltaYJPh":		pd.Series(np.array(tree["deltaYJPh"].array())),
							  "weightModified":	pd.Series(np.array(tree["weightModified"].array())),
							  "classID":		pd.Series(np.array(tree["classID"].array())),
							 })
	return dataframe


def selection(dataframe, datatype):
	dataframe = dataframe[dataframe["nJets"] > 1]
	dataframe = dataframe[dataframe["nLeptons"] == 0]

	if datatype == 1:
		dataframe = dataframe[dataframe["mJJ"] > 300]
		dataframe = dataframe[dataframe["phCentrality"] < 0.6]

	return dataframe


def extract_from_output(methodname, uploadfile):
	file 		= uproot.open(f"TMVA_outputs/{methodname}/{uploadfile}.root")
	directory 	= file["models/dataloader"]

	tree 		= directory["TrainTree"]
	TrainDF 	= build_output_dataframe(tree)
	TrainDF.loc[:, "classID"] = np.array(tree["classID"].array())

	tree 		= directory["TestTree"]
	TestDF 		= build_output_dataframe(tree)
	TestDF.loc[:, "classID"] = np.array(tree["classID"].array())

	return TrainDF, TestDF


def dataset_gen(datatype):
	dataframe = extract(datatype)
	SDataframe, BDataframe = dataframe[dataframe["classID"]==0], dataframe[dataframe["classID"]==1]

	SDataframe = SDataframe.sample(frac=1, random_state=1).reset_index(drop=True)
	BDataframe = BDataframe.sample(frac=1, random_state=1).reset_index(drop=True)

	STrainLen, BTrainLen = round(0.5*len(SDataframe)), round(0.5*len(BDataframe))

	STrainDF = SDataframe.iloc[:STrainLen]
	BTrainDF = BDataframe.iloc[:BTrainLen]

	STestDF = SDataframe.iloc[STrainLen:]
	BTestDF = BDataframe.iloc[BTrainLen:]

	TrainDF	= pd.concat((STrainDF, BTrainDF), ignore_index=True).sample(frac=1, random_state=1).reset_index(drop=True)
	TestDF	= pd.concat((STestDF, BTestDF), ignore_index=True).sample(frac=1, random_state=1).reset_index(drop=True)

	return TrainDF, TestDF


def extract(datatype):
	SFile = uproot.open("source/"+SFILENAME)
	STree = SFile[TREENAME]
	SDataframe = build_dataframe(STree)

	if datatype == 0:
		filenames = BTRAINFILENAMES
	elif datatype == 1:
		filenames = BFILENAMES
	else:
		raise ValueError("Wrong datatype")

	BDataframe = pd.DataFrame(columns=["mJJ", "deltaYJJ", "metPt", "ptBalance", "subleadJetEta",
									   "leadJetPt", "photonEta", "ptBalanceRed", "nJets",
									   "sinDeltaPhiJJOver2", "deltaYJPh", "phCentrality", 
									   "weightModified", "nLeptons"])

	for filename in filenames:
		BFile 	= uproot.open("source/"+filename)
		BTree 	= BFile[TREENAME]
		BDataframe = BDataframe.append(build_dataframe(BTree), ignore_index=True)

	SDataframe = selection(SDataframe, datatype)
	BDataframe = selection(BDataframe, datatype)

	SDataframe.loc[:,"classID"] = 0.0
	BDataframe.loc[:,"classID"] = 1.0
	dataframe = pd.concat((SDataframe, BDataframe), ignore_index=True).sample(frac=1, random_state=1).reset_index(drop=True)

	return dataframe
