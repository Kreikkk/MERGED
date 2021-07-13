from sys import argv


methodname = argv[1]

time_file = open(f"results/no_weights_{methodname}_time.txt", "w")

SChi_file = open(f"results/no_weights_{methodname}_SChi.txt", "w")
BChi_file = open(f"results/no_weights_{methodname}_BChi.txt", "w")
SChi_over_ndof_file = open(f"results/no_weights_{methodname}_SChi_over_ndof.txt", "w")
BChi_over_ndof_file = open(f"results/no_weights_{methodname}_BChi_over_ndof.txt", "w")
SPval_file = open(f"results/no_weights_{methodname}_SPval.txt", "w")
BPval_file = open(f"results/no_weights_{methodname}_BPval.txt", "w")

sig_max_file = open(f"results/no_weights_{methodname}_sig_max.txt", "w")
optimal_cut_file = open(f"results/no_weights_{methodname}_optimal_cut.txt", "w")
sig_err_file = open(f"results/no_weights_{methodname}_sig_err.txt", "w")
roc_area_file = open(f"results/no_weights_{methodname}_roc_area.txt", "w")

for i in range(1, 289):
	with open(f"{methodname}/no_weights_out{i}.txt") as readfile:
		time 			= readfile.readline().split(":")[1]

		SChi 			= readfile.readline().split(":")[1]
		BChi 			= readfile.readline().split(":")[1]
		SChi_over_ndof 	= readfile.readline().split(":")[1]
		BChi_over_ndof 	= readfile.readline().split(":")[1]
		SPval 			= readfile.readline().split(":")[1]
		BPval 			= readfile.readline().split(":")[1]

		sig_max 		= readfile.readline().split(":")[1]
		optimal_cut 	= readfile.readline().split(":")[1]
		sig_err 		= readfile.readline().split(":")[1]
		roc_area 		= readfile.readline().split(":")[1]


		time_file.write(time)

		SChi_file.write(SChi)
		BChi_file.write(BChi)
		SChi_over_ndof_file.write(SChi_over_ndof)
		BChi_over_ndof_file.write(BChi_over_ndof)
		SPval_file.write(SPval)
		BPval_file.write(BPval)

		sig_max_file.write(sig_max)
		optimal_cut_file.write(optimal_cut)
		sig_err_file.write(sig_err)
		roc_area_file.write(roc_area)


time_file.close()
SChi_file.close()
BChi_file.close()
SChi_over_ndof_file.close()
BChi_over_ndof_file.close()
SPval_file.close()
BPval_file.close()
sig_max_file.close()
optimal_cut_file.close()
sig_err_file.close()
roc_area_file.close()