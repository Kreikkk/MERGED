import numpy as np
import matplotlib.pyplot as plt



def func(method, use_weights):
	if use_weights:
		prefix = ""
	else:
		prefix = "no_weights_"

	print(f"{prefix}TMVA_{method}_sig_max.txt", "r")
	weights_file = open(f"{prefix}TMVA_{method}_sig_max.txt", "r")
	weights_err_file = open(f"{prefix}TMVA_{method}_sig_err.txt", "r")

	weights, weights_err = [], []

	for line in weights_file.readlines():
		weights.append(float(line))
	for line in weights_err_file.readlines():
		weights_err.append(float(line))


	weights = np.array(weights)
	weights_err = np.array(weights_err)

	model_id = np.arange(0, len(weights))

	mask = ~np.isnan(weights)
	x_vals = model_id[mask]
	y_vals = weights[mask]
	y_errs = weights_err[mask]



	# print("Mean: ", ws.mean(), " +- ", ((es**2).sum()**0.5)/len(es))

	# imax = ws.argmax()

	# print(imax+1)
	# print("Max: ", ws[imax], " +- ", es[imax])
	# print("N: ", len(ws))
	return x_vals, y_vals, y_errs


if __name__ == "__main__":
	# method = "MLP"
	# use_weights = False

	x1, y1, e1 = func("MLP", True)
	x2, y2, e2 = func("MLP", False)

	plt.title("MLP")

	plt.ylabel("Significance")
	plt.xlabel("Model ID")
	plt.errorbar(x1, y1, yerr=e1, label="with W")
	plt.errorbar(x2, y2, yerr=e2, label="without W")
	plt.legend()
	plt.show()


