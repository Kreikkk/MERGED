import uproot

import ROOT as root
import numpy as np
import pandas as pd
import atlasplots as aplt

from config import *
from dataloader import extract
from helpers import setup
from application_manager import TMVA_reader


data = extract(datatype=1)


SDF_raw = data[data["classID"] == 0]
BDF_raw = data[data["classID"] == 1]


print("SNum = ", len(SDF_raw), " +- ", len(SDF_raw)**0.5)
print("BNum = ", len(BDF_raw), " +- ", len(BDF_raw)**0.5)

print("SSum = ", SDF_raw["weightModified"].sum(), " +- ", ((SDF_raw["weightModified"]**2).sum()**0.5))
print("BSum = ", BDF_raw["weightModified"].sum(), " +- ", ((BDF_raw["weightModified"]**2).sum()**0.5))


print("-"*30)

# cut = 0.771
# SDF, BDF = TMVA_reader(data, "TMVA_MLP", uploadfile="no_weights_out198")

# SRes = SDF[SDF["response"]>cut]
# BRes = BDF[BDF["response"]>cut]

# print("SNum = ", len(SRes), " +- ", len(SRes)**0.5)
# print("BNum = ", len(BRes), " +- ", len(BRes)**0.5)

# print("SSum = ", SRes["weightModified"].sum(), " +- ", ((SRes["weightModified"]**2).sum()**0.5))
# print("BSum = ", BRes["weightModified"].sum(), " +- ", ((BRes["weightModified"]**2).sum()**0.5))

# print(SRes["weightModified"].sum()/(SRes["weightModified"].sum()+BRes["weightModified"].sum())**0.5)



SDF = SDF_raw
BDF = BDF_raw

SDF = SDF[SDF["phCentrality"]<0.455]
BDF = BDF[BDF["phCentrality"]<0.455]
SDF = SDF[SDF["mJJ"]>697]
BDF = BDF[BDF["mJJ"]>697]
SDF = SDF[SDF["ptBalance"]<0.064]
BDF = BDF[BDF["ptBalance"]<0.064]
SDF = SDF[SDF["deltaYJJ"]>2.227]
BDF = BDF[BDF["deltaYJJ"]>2.227]
SRes = SDF
BRes = BDF

print("SNum = ", len(SRes), " +- ", len(SRes)**0.5)
print("BNum = ", len(BRes), " +- ", len(BRes)**0.5)

print("SSum = ", SRes["weightModified"].sum(), " +- ", ((SRes["weightModified"]**2).sum()**0.5))
print("BSum = ", BRes["weightModified"].sum(), " +- ", ((BRes["weightModified"]**2).sum()**0.5))

print(SRes["weightModified"].sum()/(SRes["weightModified"].sum()+BRes["weightModified"].sum())**0.5)