import numpy as np
import ROOT as root

from array import array

from config import *
from dataloader import extract_from_output, extract
from helpers import setup, clear_file
from plotters import BDT_output_hist_plot, significance_plot

from sys import argv


def build_reader(SDataframe, BDataframe, uploadfile="output"):
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

	reader.BookMVA(METHODNAME, f"dataloader/weights/TMVAClassification{uploadfile}_BDTG.weights.xml")

	output = []
	for i, row in SDataframe.iterrows():
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
		output.append(reader.EvaluateMVA("BDTgrad"))
	SDataframe["BDToutput"] = output

	output = []
	for i, row in BDataframe.iterrows():
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
		output.append(reader.EvaluateMVA("BDTgrad"))
	BDataframe["BDToutput"] = output

	return SDataframe, BDataframe


def main():
	setup()
	uploadfile = argv[1]
	clear_file(uploadfile)

	STestDataframe, BTestDataframe		= extract_from_output("test", uploadfile)
	STrainDataframe, BTrainDataframe	= extract_from_output("train", uploadfile)
	SDataframe, BDataframe				= extract("signal")

	STestDataframe, BTestDataframe 		= build_reader(STestDataframe, BTestDataframe, uploadfile)
	STrainDataframe, BTrainDataframe 	= build_reader(STrainDataframe, BTrainDataframe, uploadfile)
	SDataframe, BDataframe 				= build_reader(SDataframe, BDataframe, uploadfile)

	BDT_output_hist_plot(STestDataframe, BTestDataframe,
						 STrainDataframe, BTrainDataframe, model_id=uploadfile)
	significance_plot(SDataframe, BDataframe, ratio=1, model_id=uploadfile)


if __name__ == "__main__":
	main()

	







