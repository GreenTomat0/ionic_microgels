import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.optimize import curve_fit
from scipy.interpolate import splrep, BSpline
import statistics
from scipy.signal import savgol_filter

# import sys
# sys.path.append('../main/')
# import MSD

# print(MSD.samples)
# print("\n")


def read_NGP(series, frame_range):

	file_path = f"/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6nwT/S6T34to18/data_out/backup_{series}_{frame_range}/NGP_S6T34to18_{series}_{frame_range}.dat"

	tau = []
	ngp = []

	with open(file_path) as f:
		next(f)
		for row in f:
			tau.append(float(row.split(',')[0]))
			ngp.append(float(row.split(',')[1]))


	return tau, ngp



def read_MSD(series, frame_range):

	file_path = f"/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6nwT/S6T34to18/data_out/backup_{series}_{frame_range}/MSD_S6T34to18_{series}_{frame_range}.dat"

	tau = []
	msd = []

	with open(file_path) as f:
		next(f)
		for row in f:
			tau.append(float(row.split(',')[0]))
			msd.append(float(row.split(',')[1]))


	return tau, msd



def read_MSD_csv(series, frame_range):

	file_path = f"/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6nwT/S6T34to18/data_out/backup_{series}_{frame_range}/S6T34to18_EMSD_{series}_{frame_range}.csv"

	df = pd.read_csv(file_path)
	
	tau = df['lag time t']
	msd = df['dr^2']

	# tau = []
	# msd = []

	# with open(file_path) as f:
	# 	next(f)
	# 	for row in f:
	# 		tau.append(float(row.split(',')[0]))
	# 		msd.append(float(row.split(',')[1]))


	return tau, msd



# fit with Gaussian
def Gaussian(x, a, x0, sigma, h):

	return a * np.exp(-(x - x0)**2 / (2 * sigma**2)) + h



# # fit with Parabola
# def Parabola(x, a, b, c):

# 	return a * x**2 + b * x + c



# # fit with Cubic
def Cubic(x, a, b, c, d):

	return a * x**3 + b * x**2 + c * x + d



# # fit with Quadratic
# def Quadratic(x, a, b, c, d, e):

# 	return a * x*x*x*x + b * x*x*x + c * x*x + d * x + e



# nondimensionalization
def nondim_NGP(list_of_lists):

	new_list_of_lists = []
	for l in list_of_lists:
		elem_z = min(l)#max(A) #A[0] #max(A)
		new_l = [elem - elem_z for elem in l]
		new_list_of_lists.append(new_l)


	return new_list_of_lists



def min_tau(list_of_lists):

	mins = []
	for l in list_of_lists:
		mins.append( min(l) )


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



def reduce_noise(list_of_lists_tau, list_of_lists_NGP):

	new_list_of_lists = []
	for l_t, l_n in zip(list_of_lists_tau, list_of_lists_NGP):
		window = int( 0.1*len(l_t) )
		new_l = savgol_filter(l_n, window, 5)
		new_list_of_lists.append(new_l)


	return new_list_of_lists



def fitting(list_of_lists_tau, list_of_lists_NGP):

	new_lol_tau = []
	new_lol_NGP = []
	
	for t, n in zip(list_of_lists_tau, list_of_lists_NGP):
		x = np.arange(t[0], t[-1], 0.1)
		
		# smooth curves
		# tck = splrep(l_t, l_n, s=0)
		# y_spline = BSpline(*tck)(x)
		
		# popt, _ = curve_fit(Cubic, t, n)
		# y = Cubic(x, popt[0], popt[1], popt[2], popt[3])

		p = np.poly1d( np.polyfit(t, n, 6) )
		y = p(x)


		new_lol_tau.append(x)
		new_lol_NGP.append(y)


	return new_lol_tau, new_lol_NGP




def draw_NGP():

	fig, ax = plt.subplots(figsize=(12, 8))

	# common lists (contain lists of every frame_range from everu series)
	tau_c = []
	NGP_c = []

	# nof = 0 # number of frames

	series = {3: ['2000_5000'], 
			4: ['0_2000'],
			5: ['2000_5000'] }


	for s in series:

		frame_range = series[s]

		for fr in frame_range:
			# nof += 1
			tau, NGP = read_NGP(s, fr)
			
			if (s == 3) & (fr == '2000_5000'):
				rlim = 1.25
				# llim = 0.4
			if (s == 4) & (fr == '0_2000'):
				rlim = 1.25
				# llim = 0.4
			if (s == 5) & (fr == '2000_5000'):
				rlim = 20


			rindexes = [i for i in range(len(tau)) if tau[i] >= rlim]
			rindex = rindexes[0]
			# lindexes = [i for i in range(len(tau)) if tau[i] <= llim]
			# lindex = lindexes[-1]

			del tau[rindex:]
			del NGP[rindex:]
			# del tau[:lindex]
			# del NGP[:lindex]

			tau_c.append(tau)
			NGP_c.append(NGP)

			# plt.plot(tau_sp, NGP_sp, ls='none', marker='^', ms=10, label=f'{s}_{fr}')

			# FITTING
			# x = np.arange(tau_sparse[0], tau_sparse[-1], 0.1)

			# smooth curves
			# tck = splrep(tau, NGP_nd, s=0)
			# y_spline = BSpline(*tck)(x)
			# plt.plot(x, y_spline, c='k', ls='--', lw=1)

			# popt, _ = curve_fit(Gaussian, x, y_spline)

			# y = Gaussian(x, popt[0], popt[1], popt[2], popt[3])
			# plt.plot(x, y, c='k', ls='--', lw=1)

			# REDUCE THE NOISE
			# w = savgol_filter(NGP_sparse, len(tau_sparse), 3)
			# plt.plot(tau_sparse, w, c='k', ls='--', lw=1)




	# NONDIMENSIONALIZATION
	global_min = min_tau(tau_c)
	tau_nd = nondim_tau(tau_c, global_min)
	NGP_nd = nondim_NGP(NGP_c)


	tau_sp = tau_nd #sparse(tau_nd)
	NGP_sp = NGP_nd #sparse(NGP_nd)

	# REDUCE THE NOISE
	NGP_sp_rn = reduce_noise(tau_sp, NGP_sp)

	# FITTING
	tau_sp_fit, NGP_sp_fit = fitting(tau_sp, NGP_sp)



	# for i, (t, n) in enumerate(zip(tau_sp, NGP_sp_rn)):
	for i in range(len(tau_sp)):
		
		if i == 0:
			series = 3
			frame = '2000_5000'
			# time_label = [1.7, 2.2]
		if i == 1:
			series = 4 
			frame = '0_2000'
			# time_label = [2.2, 2.8]
		if i == 2:
			series = 5
			frame = '2000_5000'
			# time_label = [3.9, 4.4]



		# plt.plot(t, n, ls='-', marker='^', ms=10, markerfacecolor="None", markeredgewidth=2, label=f'{series}_{frame}') #label=str(time_label) + ' min'
		plt.plot(tau_sp[i], NGP_sp[i], ls='none', marker='^', ms=10, markerfacecolor="None", markeredgewidth=2, label=f'{series}_{frame}')
		plt.plot(tau_sp[i], NGP_sp_rn[i], ls='--', color='k', linewidth=1)
		# plt.plot(tau_sp_fit[i], NGP_sp_fit[i], ls='--', color='k', linewidth=1)


	plt.xticks(fontsize=20)
	plt.yticks(fontsize=20)

	plt.title('NGP, S6 (6.84 wt%), T = [34, 18]' + r'$^{\circ} C$', fontsize=20, fontweight='bold')

	plt.xlabel(r'$\tau$ [sec]', fontsize=28)
	plt.ylabel(r'$\alpha_2$', fontsize=28)

	plt.xscale('log')
	# plt.yscale('log')

	# plt.xlim(0, 5)
	# plt.ylim(0, 70)

	plt.legend(fontsize=16)




def draw_MSD():

	fig, ax = plt.subplots(figsize=(12, 8))

	px_to_micron = 0.06905

	
	series = {3: ['2000_5000'], 
			4: ['0_2000'],
			5: ['2000_5000'] }


	for s in series:

		frame_range = series[s]

		for fr in frame_range:

			tau, MSD = read_MSD(s, fr)
			# tau, MSD = read_MSD_csv(s, fr)


			# rindexes = [i for i in range(len(tau)) if tau[i] >= rlim]
			# rindex = rindexes[0]

			# del tau[rindex:]
			# del MSD[rindex:]

			MSD_micron = [i*px_to_micron*px_to_micron for i in MSD]

			plt.plot(tau, MSD_micron, ls='none', marker='^', ms=10, markerfacecolor="None", markeredgewidth=1, label=f'{s}_{fr}') #label=str(time_label) + ' min'


		plt.xticks(fontsize=20)
		plt.yticks(fontsize=20)

		plt.title('MSD, S6 (6.84 wt%), T = [34, 18]' + r'$^{\circ} C$', fontsize=20, fontweight='bold')

		plt.xlabel(r'$\tau$ [sec]', fontsize=28)
		plt.ylabel(r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]', fontsize=28)

		plt.xscale('log')
		plt.yscale('log')

		# plt.xlim(0, 5)
		# plt.ylim(0, 70)

		plt.legend(fontsize=16)






draw_NGP()
draw_MSD()

plt.show()