import numpy as np
import matplotlib.pyplot as plt



def func(method, use_weights):
	if use_weights:
		prefix = ""
	else:
		prefix = "no_weights_"


	weights_file = open(f"{prefix}TMVA_{method}_sig_max.txt", "r")
	weights_err_file = open(f"{prefix}TMVA_{method}_sig_err.txt", "r")
	p_signal_file = open(f"{prefix}TMVA_{method}_SPval.txt", "r")
	p_bkg_file = open(f"{prefix}TMVA_{method}_BPval.txt", "r")

	weights, weights_err, p_signal, p_bkg = [], [], [], []

	for line in weights_file.readlines():
		weights.append(float(line))
	for line in weights_err_file.readlines():
		weights_err.append(float(line))
	for line in p_signal_file.readlines():
		p_signal.append(float(line))
	for line in p_bkg_file.readlines():
		p_bkg.append(float(line))

	weights = np.array(weights)
	weights_err = np.array(weights_err)
	p_signal = np.array(p_signal)
	p_bkg = np.array(p_bkg)

	weights = weights[~np.isnan(weights)]
	weights_err = weights_err[~np.isnan(weights_err)]
	p_signal = p_signal[~np.isnan(p_signal)]
	p_bkg = p_bkg[~np.isnan(p_bkg)]



	ws, es = [], []
	for w, w_err, p_s, p_b in zip(weights, weights_err, p_signal, p_bkg):
		if (p_s > 0.05 and p_b > 0.05):
			ws.append(w)
			es.append(w_err)

	ws = np.array(ws)
	es = np.array(es)


	print("Mean: ", ws.mean(), " +- ", ((es**2).sum()**0.5))

	imax = ws.argmax()

	print(imax+1)
	print("Max: ", ws[imax], " +- ", es[imax])
	print("N: ", len(ws))
	return ws, es


if __name__ == "__main__":
	method = "BDT"
	use_weights = False

	ws, es = func(method, use_weights)

