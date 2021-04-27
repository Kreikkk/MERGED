import numpy as np
import ROOT as root
import atlasplots as aplt


def normalized_hist_to_array(hist, nbins, include_error=True):
	arr = []
	if include_error:
		for index in range(1, nbins+1):
			arr.append(hist.GetBinContent(index) + hist.GetBinErrorUp(index))
	else:
		for index in range(1, nbins+1):
			arr.append(hist.GetBinContent(index))

	sum_of_weights = hist.GetSumOfWeights()

	return np.array(arr)/sum_of_weights


def get_hist_max(hist, nbins, include_error=True):
	arr = normalized_hist_to_array(hist, nbins, include_error)
	return np.max(arr)


def error(signal_events, bg_events):
	S = np.sum(signal_events)
	B = np.sum(bg_events)

	SErr = np.sum(signal_events**2)**0.5
	BErr = np.sum(bg_events**2)**0.5

	SPart = (S + B)**(-0.5) - 0.5*S*((S + B)**(-1.5))
	BPart = -0.5*S*((S + B)**(-1.5))

	return ((SPart*SErr)**2 + (BPart*BErr)**2)**0.5


def get_contour_ys(hist, nbins):
	ylow, yup = [], []
	for index in range(1, nbins+1):
		val = hist.GetBinContent(index)
		err = hist.GetBinError(index)
		try:
			ylow.append(1 - err/val)
			yup.append(1 + err/val)
		except ZeroDivisionError:
			ylow.append(1 - 1)
			yup.append(1 + 1)

	return ylow, yup


def setup(fontsize=27):
	root.TMVA.Tools.Instance()
	aplt.set_atlas_style(fontsize)
	root.gStyle.SetErrorX(0.5)
	root.gStyle.SetEndErrorSize(0.1)


def chisq(hist_true, hist_exp, tp):
	chisq = hist_true.Chi2Test(hist_exp, option="WW CHI2")
	p_val = hist_true.Chi2Test(hist_exp, option="WW")
	chisq_over_ndof = hist_true.Chi2Test(hist_exp, option="WW CHI2/NDF")

	return chisq, chisq_over_ndof, p_val


def viewer(filename):
	root.TMVA.Tools.Instance()
	root.TMVA.TMVAGui(f"{filename}.root")
	root.gApplication.Run()


def dump(methodname, uploadfile, data):
	with open(f"results/data/{methodname}/{uploadfile}.txt", "a") as file:
		file.write(data)


def clear(methodname, uploadfile):
	with open(f"results/data/{methodname}/{uploadfile}.txt", "w") as _:
		pass