import uproot

import ROOT as root
import numpy as np
import pandas as pd
import atlasplots as aplt

from config import *
from dataloader import build_dataframe
from helpers import setup


def selection(dataframe, region):
    dataframe = dataframe[dataframe["nJets"] > 1]
    if region == "CR1":
        dataframe = dataframe[dataframe["nLeptons"] == 0]
        dataframe = dataframe[dataframe["mJJ"] < 300]
    elif region == "CR2":
        dataframe = dataframe[dataframe["nLeptons"] == 0]
        dataframe = dataframe[dataframe["mJJ"] > 300]
        dataframe = dataframe[dataframe["phCentrality"] > 0.6]
    elif region == "Wgamma":
        dataframe = dataframe[dataframe["nLeptons"] > 0]

    return dataframe


def extractMC(region):
    backgounds = {}
    for name in HISTOS.keys():
        file = uproot.open(f"source/{name}.root")
        tree = file[TREENAME]
        dataframe = build_dataframe(tree)
        dataframe = selection(dataframe, region)
        print(name)
        backgounds.update({name: dataframe})

    return backgounds


def extractData(region):
    file = uproot.open("source/Data.root")
    tree = file[TREENAME]
    dataframe = build_dataframe(tree)
    dataframe = selection(dataframe, region)
    
    return dataframe


def plotter(region, variable, filename):

    left, right, _, maximum = VARIABLES[variable]["margins"][region]
    nbins = VARIABLES[variable]["nbins"][region]

    fig, (ax1, ax2) = aplt.ratio_plot(name="", figsize=(800, 900), hspace=0.01)

    hist_data = extractData(region)
    hist = root.TH1F("", "Data", nbins, left, right)
    hist.SetLineWidth(1)
    hist.Sumw2()

    for var, weight in zip(hist_data[variable], hist_data["weightModified"]):
        hist.Fill(var, weight)

    MC = extractMC(region)
    MC_sum = root.THStack("1", "")

    hist1_data = MC["Zllgam"]
    hist2_data = MC["ZnunuFromQcd"]
    hist3_data = MC["SinglePhoton"]
    hist4_data = MC["ttgamma"]
    hist5_data = MC["WenuDataDriven"]
    hist6_data = MC["WgamEWK"]
    hist7_data = MC["Wgam"]
    hist8_data = MC["ZgQCD"]
    hist9_data = MC["ZgEWK"]

    hist1 = root.TH1F("", "Zllgam", nbins, left, right)
    hist2 = root.TH1F("", "ZnunuFromQcd", nbins, left, right)
    hist3 = root.TH1F("", "SinglePhoton", nbins, left, right)
    hist4 = root.TH1F("", "ttgamma", nbins, left, right)
    hist5 = root.TH1F("", "WenuDataDriven", nbins, left, right)
    hist6 = root.TH1F("", "WgamEWK", nbins, left, right)
    hist7 = root.TH1F("", "Wgam", nbins, left, right)
    hist8 = root.TH1F("", "ZgQCD", nbins, left, right)
    hist9 = root.TH1F("", "ZgEWK", nbins, left, right)

    hist1.SetFillColor(root.kAzure + 3)
    hist2.SetFillColor(root.kCyan + 1)
    hist3.SetFillColor(root.kGreen + 3)
    hist4.SetFillColor(root.kViolet - 6)
    hist5.SetFillColor(root.kSpring - 5)
    hist6.SetFillColor(root.kOrange - 9)
    hist7.SetFillColor(root.kOrange + 1)
    hist8.SetFillColor(root.kPink - 1)

    # hist9.SetFillColor(root.kWhite)
    # hist9.SetLineWidth(5)
    # print(dir(hist9))

    hist1.SetLineWidth(0)
    hist2.SetLineWidth(0)
    hist3.SetLineWidth(0)
    hist4.SetLineWidth(0)
    hist5.SetLineWidth(0)
    hist6.SetLineWidth(0)
    hist7.SetLineWidth(0)
    hist8.SetLineWidth(0)
    hist9.SetLineWidth(0)

    hist1.Sumw2()
    hist2.Sumw2()
    hist3.Sumw2()
    hist4.Sumw2()
    hist5.Sumw2()
    hist6.Sumw2()
    hist7.Sumw2()
    hist8.Sumw2()
    hist9.Sumw2()

    for var, weight in zip(hist1_data[variable], hist1_data["weightModified"]):
        hist1.Fill(var, weight)
    for var, weight in zip(hist2_data[variable], hist2_data["weightModified"]):
        hist2.Fill(var, weight)
    for var, weight in zip(hist3_data[variable], hist3_data["weightModified"]):
        hist3.Fill(var, weight)
    for var, weight in zip(hist4_data[variable], hist4_data["weightModified"]):
        hist4.Fill(var, weight)
    for var, weight in zip(hist5_data[variable], hist5_data["weightModified"]):
        hist5.Fill(var, weight)
    for var, weight in zip(hist6_data[variable], hist6_data["weightModified"]):
        hist6.Fill(var, weight)
    for var, weight in zip(hist7_data[variable], hist7_data["weightModified"]):
        hist7.Fill(var, weight)
    for var, weight in zip(hist8_data[variable], hist8_data["weightModified"]):
        hist8.Fill(var, weight)
    for var, weight in zip(hist9_data[variable], hist9_data["weightModified"]):
        hist9.Fill(var, weight)


    hist2_coef = 43.9/0.307
    hist3_coef = 24.05/8.41

    for i in range(1, nbins+1):
        err2 = hist2.GetBinError(i)
        err3 = hist3.GetBinError(i)

        hist2.SetBinError(i, err2*hist2_coef)
        hist3.SetBinError(i, err3*hist3_coef)

    total_bin_errors = []
    bin_values = []
    bin_centers = []
    bin_widths = []
    bin_up, bin_low = [], []
    rel_error = []

    for i in range(nbins):
        bin_error = hist1.GetBinError(i+1)**2 + hist2.GetBinError(i+1)**2 + hist3.GetBinError(i+1)**2 +\
                    hist4.GetBinError(i+1)**2 + hist5.GetBinError(i+1)**2 + hist6.GetBinError(i+1)**2 +\
                    hist7.GetBinError(i+1)**2 + hist8.GetBinError(i+1)**2 + hist9.GetBinError(i+1)**2
        bin_error = bin_error**0.5

        bin_val = hist1.GetBinContent(i+1) + hist2.GetBinContent(i+1) + hist3.GetBinContent(i+1) +\
                  hist4.GetBinContent(i+1) + hist5.GetBinContent(i+1) + hist6.GetBinContent(i+1) +\
                  hist7.GetBinContent(i+1) + hist8.GetBinContent(i+1) + hist9.GetBinContent(i+1)

        total_bin_errors.append(bin_error)
        bin_values.append(bin_val)
        bin_centers.append(hist1.GetBinCenter(i+1))
        bin_widths.append(hist1.GetBinWidth(i+1)/2)

        rel_error.append(bin_error/bin_val)

    # print(total_bin_errors)
    # print(bin_values)

    # print(total_bin_errors)

    invisible_histogram = root.TH1F("", "", nbins, left, right)

    MC_sum.Add(hist1)
    MC_sum.Add(hist2)
    MC_sum.Add(hist3)
    MC_sum.Add(hist4)
    MC_sum.Add(hist5)
    MC_sum.Add(hist6)
    MC_sum.Add(hist7)
    MC_sum.Add(hist8)
    MC_sum.Add(hist9)
    true_errors = np.array(MC_sum.GetStack().Last().GetSumw2())

    # print(total_bin_errors)
    # total_bin_errors = true_errors[1:-1]**0.5
    # print(total_bin_errors)

    for i in range(nbins):
        invisible_histogram.SetBinContent(i+1, bin_values[i])
        invisible_histogram.SetBinError(i+1, total_bin_errors[i])
        bin_up.append(invisible_histogram.GetBinErrorUp(i+1))
        bin_low.append(invisible_histogram.GetBinErrorLow(i+1))

    invisible_histogram.SetLineWidth(1)
    invisible_histogram.SetLineColor(root.kAzure + 3)
    # print(dir(invisible_histogram))


    if nbins == 10:
        box1 = root.TBox(bin_centers[0]-bin_widths[0],bin_values[0]-bin_low[0],bin_centers[0]+bin_widths[0],bin_values[0]+bin_up[0])
        box2 = root.TBox(bin_centers[1]-bin_widths[1],bin_values[1]-bin_low[1],bin_centers[1]+bin_widths[1],bin_values[1]+bin_up[1])
        box3 = root.TBox(bin_centers[2]-bin_widths[2],bin_values[2]-bin_low[2],bin_centers[2]+bin_widths[2],bin_values[2]+bin_up[2])
        box4 = root.TBox(bin_centers[3]-bin_widths[3],bin_values[3]-bin_low[3],bin_centers[3]+bin_widths[3],bin_values[3]+bin_up[3]) 
        box5 = root.TBox(bin_centers[4]-bin_widths[4],bin_values[4]-bin_low[4],bin_centers[4]+bin_widths[4],bin_values[4]+bin_up[4])
        box6 = root.TBox(bin_centers[5]-bin_widths[5],bin_values[5]-bin_low[5],bin_centers[5]+bin_widths[5],bin_values[5]+bin_up[5])
        box7 = root.TBox(bin_centers[6]-bin_widths[6],bin_values[6]-bin_low[6],bin_centers[6]+bin_widths[6],bin_values[6]+bin_up[6])
        box8 = root.TBox(bin_centers[7]-bin_widths[7],bin_values[7]-bin_low[7],bin_centers[7]+bin_widths[7],bin_values[7]+bin_up[7])
        box9 = root.TBox(bin_centers[8]-bin_widths[8],bin_values[8]-bin_low[8],bin_centers[8]+bin_widths[8],bin_values[8]+bin_up[8])
        box10 =root.TBox(bin_centers[9]-bin_widths[9],bin_values[9]-bin_low[9],bin_centers[9]+bin_widths[9],bin_values[9]+bin_up[9])

        box1.SetFillStyle(3004)
        box2.SetFillStyle(3004)
        box3.SetFillStyle(3004)
        box4.SetFillStyle(3004)
        box5.SetFillStyle(3004)
        box6.SetFillStyle(3004)
        box7.SetFillStyle(3004)
        box8.SetFillStyle(3004)
        box9.SetFillStyle(3004)
        box10.SetFillStyle(3004)

        box1.SetFillColor(root.kAzure + 3)
        box2.SetFillColor(root.kAzure + 3)
        box3.SetFillColor(root.kAzure + 3)
        box4.SetFillColor(root.kAzure + 3)
        box5.SetFillColor(root.kAzure + 3)
        box6.SetFillColor(root.kAzure + 3)
        box7.SetFillColor(root.kAzure + 3)
        box8.SetFillColor(root.kAzure + 3)
        box9.SetFillColor(root.kAzure + 3)
        box10.SetFillColor(root.kAzure + 3)

        # print(rel_error)
        for i, val in enumerate(rel_error):
            if val > 0.3:
                rel_error[i] = 0.3
        # print(rel_error)

        box11 = root.TBox(bin_centers[0]-bin_widths[0],1-rel_error[0],bin_centers[0]+bin_widths[0],1+rel_error[0])
        box12 = root.TBox(bin_centers[1]-bin_widths[1],1-rel_error[1],bin_centers[1]+bin_widths[1],1+rel_error[1])
        box13 = root.TBox(bin_centers[2]-bin_widths[2],1-rel_error[2],bin_centers[2]+bin_widths[2],1+rel_error[2])
        box14 = root.TBox(bin_centers[3]-bin_widths[3],1-rel_error[3],bin_centers[3]+bin_widths[3],1+rel_error[3]) 
        box15 = root.TBox(bin_centers[4]-bin_widths[4],1-rel_error[4],bin_centers[4]+bin_widths[4],1+rel_error[4])
        box16 = root.TBox(bin_centers[5]-bin_widths[5],1-rel_error[5],bin_centers[5]+bin_widths[5],1+rel_error[5])
        box17 = root.TBox(bin_centers[6]-bin_widths[6],1-rel_error[6],bin_centers[6]+bin_widths[6],1+rel_error[6])
        box18 = root.TBox(bin_centers[7]-bin_widths[7],1-rel_error[7],bin_centers[7]+bin_widths[7],1+rel_error[7])
        box19 = root.TBox(bin_centers[8]-bin_widths[8],1-rel_error[8],bin_centers[8]+bin_widths[8],1+rel_error[8])
        box20 = root.TBox(bin_centers[9]-bin_widths[9],1-rel_error[9],bin_centers[9]+bin_widths[9],1+rel_error[9])

        box11.SetFillStyle(3004)
        box12.SetFillStyle(3004)
        box13.SetFillStyle(3004)
        box14.SetFillStyle(3004)
        box15.SetFillStyle(3004)
        box16.SetFillStyle(3004)
        box17.SetFillStyle(3004)
        box18.SetFillStyle(3004)
        box19.SetFillStyle(3004)
        box20.SetFillStyle(3004)

        box11.SetFillColor(root.kAzure + 3)
        box12.SetFillColor(root.kAzure + 3)
        box13.SetFillColor(root.kAzure + 3)
        box14.SetFillColor(root.kAzure + 3)
        box15.SetFillColor(root.kAzure + 3)
        box16.SetFillColor(root.kAzure + 3)
        box17.SetFillColor(root.kAzure + 3)
        box18.SetFillColor(root.kAzure + 3)
        box19.SetFillColor(root.kAzure + 3)
        box20.SetFillColor(root.kAzure + 3)

    if nbins == 3:
        box1 = root.TBox(bin_centers[0]-bin_widths[0],bin_values[0]-bin_low[0],bin_centers[0]+bin_widths[0],bin_values[0]+bin_up[0])
        box2 = root.TBox(bin_centers[1]-bin_widths[1],bin_values[1]-bin_low[1],bin_centers[1]+bin_widths[1],bin_values[1]+bin_up[1])
        box3 = root.TBox(bin_centers[2]-bin_widths[2],bin_values[2]-bin_low[2],bin_centers[2]+bin_widths[2],bin_values[2]+bin_up[2])

        box1.SetFillStyle(3004)
        box2.SetFillStyle(3004)
        box3.SetFillStyle(3004)

        box1.SetFillColor(root.kAzure + 3)
        box2.SetFillColor(root.kAzure + 3)
        box3.SetFillColor(root.kAzure + 3)


        if region == "CR1":
            for i, val in enumerate(rel_error):
                if val > 0.3:
                    rel_error[i] = 0.3
        elif region in ("CR2", "Wgamma"):
            for i, val in enumerate(rel_error):
                if val > 0.5:
                    rel_error[i] = 0.5

        box11 = root.TBox(bin_centers[0]-bin_widths[0],1-rel_error[0],bin_centers[0]+bin_widths[0],1+rel_error[0])
        box12 = root.TBox(bin_centers[1]-bin_widths[1],1-rel_error[1],bin_centers[1]+bin_widths[1],1+rel_error[1])
        box13 = root.TBox(bin_centers[2]-bin_widths[2],1-rel_error[2],bin_centers[2]+bin_widths[2],1+rel_error[2])

        box11.SetFillStyle(3004)
        box12.SetFillStyle(3004)
        box13.SetFillStyle(3004)

        box11.SetFillColor(root.kAzure + 3)
        box12.SetFillColor(root.kAzure + 3)
        box13.SetFillColor(root.kAzure + 3)

    # box = root.TBox(2, 80, 3, 120)
    # box.SetFillColorAlpha(root.kBlue, 0.2)
    



    ax1.plot(invisible_histogram, [left, right, 0, maximum], options="HIST")

    ax1.plot(MC_sum, [left, right, 0, maximum], options="SAME")
    ax1.plot(hist, [left, right, 0, maximum], options="SAME")
    # ax1.add_margins(top=0.16)

    ratio_hist = hist.Clone("ratio_hist")
    ratio_hist.Divide(MC_sum.GetStack().Last())


    if region == "CR1":
        ax2.plot(ratio_hist, [left, right, 0.701, 1.299])
        line1 = root.TLine(left, 1.2, right, 1.2)
        line2 = root.TLine(left, 1.1, right, 1.1)
        line3 = root.TLine(left, 1, right, 1)
        line4 = root.TLine(left, 0.9, right, 0.9)
        line5 = root.TLine(left, 0.8, right, 0.8)

    elif region in ("CR2", "Wgamma"):
        ax2.plot(ratio_hist, [left, right, 0.501, 1.499])
        line1 = root.TLine(left, 1.4, right, 1.4)
        line2 = root.TLine(left, 1.2, right, 1.2)
        line3 = root.TLine(left, 1, right, 1)
        line4 = root.TLine(left, 0.8, right, 0.8)
        line5 = root.TLine(left, 0.6, right, 0.6)



    bin_values = []
    uparrows, downarrows = [], []

    for i in range(nbins):
        bin_values.append(ratio_hist.GetBinContent(i+1))

    if region == "CR1":
        for i, val in enumerate(bin_values):
            if val < 0.701:
                downarrows.append(ratio_hist.GetBinCenter(i+1))
            elif val > 1.299:
                uparrows.append(ratio_hist.GetBinCenter(i+1))

    if region in ("CR2", "Wgamma"):
        for i, val in enumerate(bin_values):
            if val < 0.501:
                downarrows.append(ratio_hist.GetBinCenter(i+1))
            elif val > 1.499:
                uparrows.append(ratio_hist.GetBinCenter(i+1))



    if region == "CR1":
        uparrow_h = 1.035
        downarrow_h = 0.965
    elif region in ("CR2", "Wgamma"):
        uparrow_h = 1.065
        downarrow_h = 0.94

    if len(uparrows) == 1:
        arrow1_up = root.TMarker(uparrows[0], uparrow_h, 22)
        arrow1_up.SetMarkerSize(2)
        ax2.plot(arrow1_up, option="SAME")
    elif len(uparrows) == 2:
        arrow1_up = root.TMarker(uparrows[0], uparrow_h, 22)
        arrow2_up = root.TMarker(uparrows[1], uparrow_h, 22)
        arrow1_up.SetMarkerSize(2)
        arrow2_up.SetMarkerSize(2)
        ax2.plot(arrow1_up, option="SAME")
        ax2.plot(arrow2_up, option="SAME")
    elif len(uparrows) == 3:
        arrow1_up = root.TMarker(uparrows[0], uparrow_h, 22)
        arrow2_up = root.TMarker(uparrows[1], uparrow_h, 22)
        arrow3_up = root.TMarker(uparrows[2], uparrow_h, 22)
        arrow1_up.SetMarkerSize(2)
        arrow2_up.SetMarkerSize(2)
        arrow3_up.SetMarkerSize(2)
        ax2.plot(arrow1_up, option="SAME")
        ax2.plot(arrow2_up, option="SAME")
        ax2.plot(arrow3_up, option="SAME")
    elif len(uparrows) == 4:
        arrow1_up = root.TMarker(uparrows[0], uparrow_h, 22)
        arrow2_up = root.TMarker(uparrows[1], uparrow_h, 22)
        arrow3_up = root.TMarker(uparrows[2], uparrow_h, 22)
        arrow4_up = root.TMarker(uparrows[3], uparrow_h, 22)
        arrow1_up.SetMarkerSize(2)
        arrow2_up.SetMarkerSize(2)
        arrow3_up.SetMarkerSize(2)
        arrow4_up.SetMarkerSize(2)
        ax2.plot(arrow1_up, option="SAME")
        ax2.plot(arrow2_up, option="SAME")
        ax2.plot(arrow3_up, option="SAME")
        ax2.plot(arrow4_up, option="SAME")
    elif len(uparrows) == 5:
        arrow1_up = root.TMarker(uparrows[0], uparrow_h, 22)
        arrow2_up = root.TMarker(uparrows[1], uparrow_h, 22)
        arrow3_up = root.TMarker(uparrows[2], uparrow_h, 22)
        arrow4_up = root.TMarker(uparrows[3], uparrow_h, 22)
        arrow5_up = root.TMarker(uparrows[4], uparrow_h, 22)
        arrow1_up.SetMarkerSize(2)
        arrow2_up.SetMarkerSize(2)
        arrow3_up.SetMarkerSize(2)
        arrow4_up.SetMarkerSize(2)
        arrow5_up.SetMarkerSize(2)
        ax2.plot(arrow1_up, option="SAME")
        ax2.plot(arrow2_up, option="SAME")
        ax2.plot(arrow3_up, option="SAME")
        ax2.plot(arrow4_up, option="SAME")
        ax2.plot(arrow5_up, option="SAME")


    if len(downarrows) == 1:
        arrow1_down = root.TMarker(downarrows[0], downarrow_h, 23)
        arrow1_down.SetMarkerSize(2)
        ax2.plot(arrow1_down, option="SAME")
    elif len(downarrows) == 2:
        # print("!"*10)
        arrow1_down = root.TMarker(downarrows[0], downarrow_h, 23)
        arrow2_down = root.TMarker(downarrows[1], downarrow_h, 23)
        arrow1_down.SetMarkerSize(2)
        arrow2_down.SetMarkerSize(2)
        ax2.plot(arrow1_down, option="SAME")
        ax2.plot(arrow2_down, option="SAME")
    elif len(downarrows) == 3:
        arrow1_down = root.TMarker(downarrows[0], downarrow_h, 23)
        arrow2_down = root.TMarker(downarrows[1], downarrow_h, 23)
        arrow3_down = root.TMarker(downarrows[2], downarrow_h, 23)
        arrow1_down.SetMarkerSize(2)
        arrow2_down.SetMarkerSize(2)
        arrow3_down.SetMarkerSize(2)
        ax2.plot(arrow1_down, option="SAME")
        ax2.plot(arrow2_down, option="SAME")
        ax2.plot(arrow3_down, option="SAME")
    elif len(downarrows) == 4:
        arrow1_down = root.TMarker(downarrows[0], downarrow_h, 22)
        arrow2_down = root.TMarker(downarrows[1], downarrow_h, 22)
        arrow3_down = root.TMarker(downarrows[2], downarrow_h, 22)
        arrow4_down = root.TMarker(downarrows[3], downarrow_h, 22)
        arrow1_down.SetMarkerSize(2)
        arrow2_down.SetMarkerSize(2)
        arrow3_down.SetMarkerSize(2)
        arrow4_down.SetMarkerSize(2)
        ax2.plot(arrow1_down, option="SAME")
        ax2.plot(arrow2_down, option="SAME")
        ax2.plot(arrow3_down, option="SAME")
        ax2.plot(arrow4_down, option="SAME")
    elif len(downarrows) == 5:
        arrow1_down = root.TMarker(downarrows[0], downarrow_h, 22)
        arrow2_down = root.TMarker(downarrows[1], downarrow_h, 22)
        arrow3_down = root.TMarker(downarrows[2], downarrow_h, 22)
        arrow4_down = root.TMarker(downarrows[3], downarrow_h, 22)
        arrow5_down = root.TMarker(downarrows[4], downarrow_h, 22)
        arrow1_down.SetMarkerSize(2)
        arrow2_down.SetMarkerSize(2)
        arrow3_down.SetMarkerSize(2)
        arrow4_down.SetMarkerSize(2)
        arrow5_down.SetMarkerSize(2)
        ax2.plot(arrow1_down, option="SAME")
        ax2.plot(arrow2_down, option="SAME")
        ax2.plot(arrow3_down, option="SAME")
        ax2.plot(arrow4_down, option="SAME")
        ax2.plot(arrow5_down, option="SAME")




    line1.SetLineStyle(3)
    line2.SetLineStyle(3)
    line4.SetLineStyle(3)
    line5.SetLineStyle(3)

    ax2.plot(line1)
    ax2.plot(line2)
    ax2.plot(line3)
    ax2.plot(line4)
    ax2.plot(line5)

    ax2.set_xlabel(VARIABLES[variable]["label"])
    ax2.set_ylabel("Data/Pred.")
    ax1.set_ylabel("Events")

    ax1.frame.GetYaxis().SetTitleOffset(1.7)
    ax2.frame.GetYaxis().SetTitleOffset(1.7)

    ax1.cd()
    ax1.text(0.45, 0.90, "#sqrt{s} = 13 TeV, 139 fb^{-1}", size=25, align=13)
    ax1.text(0.45, 0.84, GRAPHING_LABEL[region], size=25, align=13)


    # legend = root.TLegend(0.73, 0.60, 0.93, 0.90)

    if VARIABLES[variable]["legpos"][region] == "left":
        shift = 0.53
    elif VARIABLES[variable]["legpos"][region] == "right":
        shift = 0

    legend = root.TLegend(0.73 - shift, 0.60, 0.93 - shift, 0.90)
    legend.SetFillColorAlpha(0, 0)
    legend.SetTextSize(17)


    legend.AddEntry(hist, "Data", "EP")
    legend.AddEntry(invisible_histogram, "Z(#nu#nu)#gamma EWK", "F")
    legend.AddEntry(hist8, "Z(#nu#nu)#gamma QCD", "F")
    legend.AddEntry(hist7, "W#gamma QCD", "F")
    legend.AddEntry(hist6, "W#gamma EWK", "F")
    legend.AddEntry(hist5, "W(e#nu), top, t#bar{t}", "F")
    legend.AddEntry(hist4, "tt#gamma", "F")
    legend.AddEntry(hist3, "#gamma + j", "F")
    legend.AddEntry(hist2, "Zj, jj", "F")
    legend.AddEntry(hist1, "Z(ll)#gamma", "F")
    legend.AddEntry(box1, "Pred. Stat. Err.", "F")
    
    legend.Draw()

    
    if nbins == 10:
        ax1.plot(box1, options="SAME")
        ax1.plot(box2, options="SAME")
        ax1.plot(box3, options="SAME")
        ax1.plot(box4, options="SAME")
        ax1.plot(box5, options="SAME")
        ax1.plot(box6, options="SAME")
        ax1.plot(box7, options="SAME")
        ax1.plot(box8, options="SAME")
        ax1.plot(box9, options="SAME")
        ax1.plot(box10, options="SAME")

        ax2.plot(box11, options="SAME")
        ax2.plot(box12, options="SAME")
        ax2.plot(box13, options="SAME")
        ax2.plot(box14, options="SAME")
        ax2.plot(box15, options="SAME")
        ax2.plot(box16, options="SAME")
        ax2.plot(box17, options="SAME")
        ax2.plot(box18, options="SAME")
        ax2.plot(box19, options="SAME")
        ax2.plot(box20, options="SAME")

    if nbins == 3:
        ax1.plot(box1, options="SAME")
        ax1.plot(box2, options="SAME")
        ax1.plot(box3, options="SAME")

        ax2.plot(box11, options="SAME")
        ax2.plot(box12, options="SAME")
        ax2.plot(box13, options="SAME")

    fig.savefig(f"./MC_data_compare_results/{region}/{filename}.pdf")




if __name__ == "__main__":
    setup()

    region = "Wgamma"

    for var in VARIABLES.keys():
        plotter(region, var, region+var)

    # var = "leadJetPt"
    # plotter(region, var, var)