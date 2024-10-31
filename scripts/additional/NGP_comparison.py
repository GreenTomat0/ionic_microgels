import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys
sys.path.append('../main/')
import MSD

# print(MSD.samples)
# print("\n")


def read_NGP(s):

	file_path = f"/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S{s}/data_out/backup/NGP_S{s}.dat"


	tau = []
	ngp = []

	with open(file_path) as f:
		next(f)
		for row in f:
			tau.append(float(row.split(',')[0]))
			ngp.append(float(row.split(',')[1]))


	return tau, ngp



def read_MSD(s):

	file_path = f"/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S{s}/data_out/backup/MSD_S{s}.dat"

	
	tau = []
	msd = []

	with open(file_path) as f:
		next(f)
		for row in f:
			tau.append(float(row.split(',')[0]))
			msd.append(float(row.split(',')[1]))


	return tau, msd



def cut_right(tau, rlim):

	rindexes = [i for i in range(len(tau)) if tau[i] >= rlim] 
	rindex = rindexes[0]

	# del tau[rindex:]
	# del MSD[rindex:]

	# tau_new = tau[:rindex]
	# MSD_new = MSD[:rindex]


	return rindex #tau_new, MSD_new



def cut_left(tau, llim):

	lindexes = [i for i in range(len(tau)) if tau[i] <= llim]
	lindex = lindexes[-1]

	# del tau[:lindex]
	# del NGP[:lindex]


	return lindex #tau, MSD



def reduce_noise(tau, NGP):

	window = int( 0.7 * len(tau) )
	new_NGP = savgol_filter(NGP, window, 3)


	return new_NGP



# nondimensionalization
def nondim_NGP(list_of_lists):

	new_list_of_lists = []
	for l in list_of_lists:
		elem_z = min(l) #max(A) #A[0] #max(A)
		new_l = [elem - elem_z for elem in l]
		new_list_of_lists.append(new_l)


	return new_list_of_lists



def min_tau(list_of_lists):

	mins = []
	for l in list_of_lists:
		mins.append( np.min(l) )


	return min(mins)



def nondim_tau(list_of_lists, global_min):

	new_list_of_lists = []
	for l in list_of_lists:
		elem_z = l[0] - global_min
		new_l = [elem - elem_z for elem in l]
		new_list_of_lists.append(new_l)


	return new_list_of_lists



def sparse(list_of_lists):

	new_list_of_lists = []
	for l in list_of_lists:
		new_l = [elem for i, elem in enumerate(l) if i % 5 == 0]
		new_list_of_lists.append(new_l)


	return new_list_of_lists




def draw_NGP(MSD_samples):

	fig, ax = plt.subplots(figsize=(12, 8))

	concentration = pd.read_csv('../main/input_data/Concentrations.csv')

	tau_c = []
	NGP_c = []
	conc_c = []

	for s in MSD_samples:
		tau, NGP = read_NGP(s)
		

		# if s == 32:
		# 	rlim = 8.3
		# 	llim = 0.2
		# 	rindex = cut_right(tau, rlim)
		# 	lindex = cut_left(tau, llim)
		# 	del tau[rindex:]
		# 	del NGP[rindex:]
		# 	del tau[:lindex]
		# 	del NGP[:lindex]

		if s == 2:
			rlim = 5.4
			llim = 0.8
			rindex = cut_right(tau, rlim)
			lindex = cut_left(tau, llim)
			del tau[rindex:]
			del NGP[rindex:]
			del tau[:lindex]
			del NGP[:lindex]

		# if s == 9:
		# 	rlim = 3.7
		# 	llim = 0.2
		# 	rindex = cut_right(tau, MSD, rlim)
		# 	lindex = cut_left(tau, MSD, llim)
		# 	del tau[rindex:]
		# 	del NGP[rindex:]
		# 	del tau[:lindex]
		# 	del NGP[:lindex]

		if s == 8:
			# rlim = 6.29
			llim = 6.29
			# rindex = cut_right(tau, rlim)
			lindex = cut_left(tau, llim)
			# del tau[rindex:]
			# del NGP[rindex:]
			del tau[:lindex]
			del NGP[:lindex]

		if s == 7:
			rlim = 19
			llim = 3.4
			rindex = cut_right(tau, rlim)
			lindex = cut_left(tau, llim)
			del tau[rindex:]
			del NGP[rindex:]
			del tau[:lindex]
			del NGP[:lindex]


		# rindexes = [i for i in range(len(tau)) if tau[i] >= rlim]
		# rindex = rindexes[0]
		# lindexes = [i for i in range(len(tau)) if tau[i] <= llim]
		# lindex = lindexes[-1]

		# del tau[rindex:]
		# del NGP[rindex:]
		# del tau[:lindex]
		# del NGP[:lindex]


		conc = concentration.loc[concentration['sample'] == s, 'concentration'].item()
		# plt.plot(tau, NGP, ls='-', marker='o', ms=5, label=f'{conc} wt% (S{s})')
		# plt.plot(MSD, NGP, marker='*', ms=5, ls='-', label=f'S{s}')


		# reduce noise
		NGP_rn = reduce_noise(tau, NGP)
		# plt.plot(tau, NGP_rn, ls='--', c='k')


		tau_c.append(tau)
		NGP_c.append(NGP_rn)
		conc_c.append(conc)


	# # REDUCE THE NOISE
	# NGP_rn = reduce_noise(tau_c, NGP_c)

	# NONDIMENSIONALIZATION
	global_min = min_tau(tau_c)
	tau_nd = nondim_tau(tau_c, global_min)
	NGP_nd = nondim_NGP(NGP_c)


	tau_sp = sparse(tau_nd)
	NGP_sp = sparse(NGP_nd)


	for i, (t, n) in enumerate(zip(tau_sp, NGP_sp)):

		phi = conc_c[i]
		s_cur = MSD_samples[i]

		plt.plot(t, n, ls='none', marker='^', ms=10, markerfacecolor="None", markeredgewidth=2, label=r"$\varphi = $" + f'{"{:.2f}".format(phi)}' + f'(S{s_cur})')


	plt.title('NGP', fontsize=20, fontweight='bold')

	plt.xscale('log')

	plt.xlabel(r'$\tau$ [sec]', fontsize=28)
	plt.ylabel(r'$\alpha_2$', fontsize=28)

	plt.legend(fontsize=16)




def draw_MSD(MSD_samples):

	fig, ax = plt.subplots(figsize=(12, 8))

	concentration = pd.read_csv('../main/input_data/Concentrations.csv')

	px_to_micron = 0.06905

	for s in MSD_samples:
		tau, MSD = read_MSD(s)


		# if s == 32:
		# 	rlim = 8.3
		# 	rindex = cut_right(tau, rlim)
		# 	del tau[rindex:]
		# 	del MSD[rindex:]

		if s == 2:
			rlim = 5.4
			rindex = cut_right(tau, rlim)
			del tau[rindex:]
			del MSD[rindex:]

		if s == 9:
			rlim = 3.7
			rindex = cut_right(tau, rlim)
			del tau[rindex:]
			del MSD[rindex:]

		if s == 7:
			rlim = 19
			rindex = cut_right(tau, rlim)
			del tau[rindex:]
			del MSD[rindex:]


		# rindexes = [i for i in range(len(tau)) if tau[i] >= rlim]
		# rindex = rindexes[0]

		# del tau[rindex:]
		# del MSD[rindex:]


		MSD_micron = [i*px_to_micron*px_to_micron for i in MSD]

		conc = concentration.loc[concentration['sample'] == s, 'concentration'].item()
		# plt.plot(tau, MSD_micron, ls='-', marker='o', ms=5, label=f'{conc} wt% (S{s})')
		plt.plot(tau, MSD, ls='none', marker='^', ms=10, markerfacecolor="None", markeredgewidth=2, label=r"$\varphi = $" + f'{"{:.2f}".format(conc)}' + f'(S{s})')


	plt.title('MSD', fontsize=20, fontweight='bold')

	plt.xscale('log')
	plt.yscale('log')

	plt.xlabel(r'$\tau$ [sec]', fontsize=28)
	plt.ylabel(r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]', fontsize=28)

	plt.legend(fontsize=16)





plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 20
plt.rcParams["figure.autolayout"] = True



# draw_NGP(MSD.samples)
samples = [2, 8, 7] # 32, 9
draw_NGP(samples)
draw_MSD(samples)



plt.show()