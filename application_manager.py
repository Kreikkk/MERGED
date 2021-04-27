import numpy as np
import pandas as pd
import ROOT as root
import pickle

from array import array
from plotters import output_hist_plot, significance_plot
from dataloader import extract_from_output, extract, dataset_gen
from helpers import setup
from sys import argv


def main():
	methodname, uploadfile = argv[1:]

	if methodname in ("TMVA_BDT", "TMVA_MLP"):
		TrainDataframe, TestDataframe		= extract_from_output(methodname, uploadfile)
		Dataframe							= extract(datatype=1)

		STrainDataframe, BTrainDataframe 	= TMVA_reader(TrainDataframe, methodname, uploadfile)
		STestDataframe, BTestDataframe 		= TMVA_reader(TestDataframe, methodname, uploadfile)
		SDataframe, BDataframe 				= TMVA_reader(Dataframe, methodname, uploadfile)

	elif methodname in ("SKL_BDT", "SKL_MLP"):
		TrainDataframe, TestDataframe		= dataset_gen(datatype=0)
		Dataframe							= extract(datatype=1)

		STrainDataframe, BTrainDataframe 	= SKL_reader(TrainDataframe, methodname, uploadfile)
		STestDataframe, BTestDataframe 	 	= SKL_reader(TestDataframe, methodname, uploadfile)
		SDataframe, BDataframe 			 	= SKL_reader(Dataframe, methodname, uploadfile)

	else:
		raise ValueError(f"No method: {methodname}")

	output_hist_plot(STestDataframe, BTestDataframe,
					 STrainDataframe, BTrainDataframe, methodname=methodname, uploadfile=uploadfile)
	significance_plot(SDataframe, BDataframe, methodname=methodname, uploadfile=uploadfile)


def TMVA_reader(dataframe, methodname, uploadfile="output"):
	var_mJJ 				= array('f',[0])
	var_deltaYJJ 			= array('f',[0])
	var_metPt 				= array('f',[0])
	var_ptBalance 			= array('f',[0])
	var_subleadJetEta 		= array('f',[0])
	var_leadJetPt 			= array('f',[0])
	var_photonEta 			= array('f',[0])
	var_ptBalanceRed 		= array('f',[0])
	var_nJets 				= array('f',[0])
	var_sinDeltaPhiJJOver2 	= array('f',[0])
	var_deltaYJPh 			= array('f',[0])
	var_weightModified 		= array('f',[0])

	reader = root.TMVA.Reader("reader")
	reader.AddVariable("mJJ",				var_mJJ)
	reader.AddVariable("deltaYJJ",			var_deltaYJJ)
	reader.AddVariable("metPt",				var_metPt)
	reader.AddVariable("ptBalance",			var_ptBalance)
	reader.AddVariable("subleadJetEta",		var_subleadJetEta)
	reader.AddVariable("leadJetPt",			var_leadJetPt)
	reader.AddVariable("photonEta",			var_photonEta)
	reader.AddVariable("ptBalanceRed",		var_ptBalanceRed)
	reader.AddVariable("nJets",				var_nJets)
	reader.AddVariable("sinDeltaPhiJJOver2",var_sinDeltaPhiJJOver2)
	reader.AddVariable("deltaYJPh",			var_deltaYJPh)
	reader.AddSpectator("weightModified",	var_weightModified)

	reader.BookMVA(methodname, f"models/dataloader/weights/TMVAClassification_{methodname}_{uploadfile}_{methodname}.weights.xml")

	response = []
	for i, row in dataframe.iterrows():
		var_mJJ[0]					= row["mJJ"]
		var_deltaYJJ[0]				= row["deltaYJJ"]
		var_metPt[0]				= row["metPt"]
		var_ptBalance[0]			= row["ptBalance"]
		var_subleadJetEta[0]		= row["subleadJetEta"]
		var_leadJetPt[0]			= row["leadJetPt"]
		var_photonEta[0]			= row["photonEta"]
		var_ptBalanceRed[0]			= row["ptBalanceRed"]
		var_nJets[0]				= row["nJets"]
		var_sinDeltaPhiJJOver2[0]	= row["sinDeltaPhiJJOver2"]
		var_deltaYJPh[0]			= row["deltaYJPh"]
		response.append(reader.EvaluateMVA(methodname))
	dataframe.loc[:,"response"] = response

	SDataframe, BDataframe = dataframe[dataframe["classID"] == 0], dataframe[dataframe["classID"] == 1]

	return SDataframe, BDataframe


def SKL_reader(dataframe, methodname, uploadfile):
	with open(f"models/{methodname}/{uploadfile}.pickle", "rb") as file:
		reader = pickle.load(file)

	response = reader.predict_proba(dataframe.values[:,:11])[:,0]
	dataframe.loc[:,"response"] = response

	SDataframe, BDataframe = dataframe[dataframe["classID"] == 0], dataframe[dataframe["classID"] == 1]

	return SDataframe, BDataframe


if __name__ == "__main__":
	setup()
	main()