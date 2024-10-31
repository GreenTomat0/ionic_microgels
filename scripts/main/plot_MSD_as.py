import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MSD
# from scipy.signal import savgol_filter
# from scipy.ndimage.filters import gaussian_filter1d
from scipy.optimize import curve_fit
# from scipy.interpolate import splrep, BSpline




def read_vol_fr():

	df = pd.read_csv("/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/scripts/main/output_data/volume_fraction.csv")

	VF_dict = {}
	for row in df.iterrows():
		VF_dict[int(row[1]['sample'])] = row[1]['volume_fraction']

	return VF_dict



# def reduce_noise(msd, weight):

# 	# for t, m in zip(tau, msd):
# 	# 	window = int( 0.9 * len(t) )
# 	# 	new_msd = savgol_filter(m, window, 2)


# 	# for m in msd:
# 	# window = int( 0.3 * len(msd) )
# 	# new_msd = savgol_filter(msd, window, 3)

# 	# msd_smoothed = gaussian_filter1d(msd, sigma=3)

#     last = msd[0]  # First value in the plot (first timestep)
#     smoothed = list()

#     for point in msd:
#         smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
#         smoothed.append(smoothed_val)                        # Save it
#         last = smoothed_val                                  # Anchor the last smoothed value
        
#     return smoothed


# 	# return msd_smoothed

# fit with polinomial function
def fitting_func(x, a, b, c, d):

	# return a * x**2 + b * x + c
	# return a * x + b
	# return a * np.exp(-b * x) + c
	# return a + b * np.log(x)
	# return (a * x) / (x + b)
	return a * np.log( b * x + c ) + d




# concentration = {5: 0.6698, 4: 1.339, 34: 1.674, 3: 2, 32: 2.344, 2: 2.679, 9: 2.958, 8: 4.218, 7: 5.276, 6: 6.84}  # number_of_sample: concentration
# a_s  = {2: 1.58,  3: 1.597, 4: 1.7, 5: 1.83, 6: 1.28, 7: 1.336, 8: 1.485, 9: 1.503}  # number_of_sample: a_s_(micron) (a_s is the first peack of g(r))
concentration = pd.read_csv('input_data/Concentrations.csv')


plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 20
plt.rcParams["figure.autolayout"] = True

# print(MSD.samples)
MSD_samples = MSD.samples
MSD_samples.remove(5)
MSD_samples.remove(34)
MSD_samples.remove(32)
# print(MSD_samples)

vol_frac = read_vol_fr()

markers = ['o', 'v', '*', '.', 'h', '<', 's']
colors = ['black', 'dimgray', 'gray', 'darkgray', 'gray', 'dimgray', 'black']

counter = 0

for s in MSD_samples:

	data_cond = MSD.data[MSD.data['sample'] == s]

	rlim = 3
	tau = data_cond.loc[data_cond['lag time t'] < rlim, 'lag time t']
	MSD_ = data_cond.loc[data_cond['lag time t'] < rlim, 'dr^2']

	
	conc = concentration.loc[concentration['sample'] == s, 'concentration'].item()
	# plt.plot(tau[:-1000], MSD_[:-1000], lw=3, label=f'{conc} wt% (S{s})')
	phi = vol_frac[s]


	# FITTING
	tau_list = tau.tolist()
	MSD_list = MSD_.tolist()
	
	if s in [6, 7]:

		x = np.arange(tau_list[0], tau_list[-1], 0.01)

		sigma = np.ones(len(tau_list))
		sigma[[0, -1]] = 0.01
		popt, _ = curve_fit(fitting_func, tau_list, MSD_list, sigma=sigma)#, absolute_sigma=True)
		# print(*popt)
		y = fitting_func(x, *popt)
		# plt.plot(x, y, ls='--', marker='o', lw=1, color='black')

	else:
		x = tau_list
		y = MSD_list

	plt.plot(x, y, ls='none', ms=10, markerfacecolor="None", markeredgewidth=2, marker=markers[counter], color=colors[counter],
		label=r"$\varphi = $" + f'{"{:.2f}".format(phi)}') # + f'(S{s})' 
	# markevery=5, 

	
	counter += 1


	# divide by a_s
	# MSD_a_s = [ item/(a_s[s]**2) for item in MSD_ ]

	# plt.plot(tau, MSD_a_s, lw=3, label=f'S{s}, {concentration[s]} wt%')


plt.xscale('log')
plt.yscale('log')


plt.xlabel(r'$\tau$ (s)', fontsize=28) # Lag time
plt.ylabel(r'$\langle \Delta r^2 \rangle$ ($\mu$m$^2$)', fontsize=28)
# plt.ylabel(r'$\langle \Delta r^2 \rangle / a_s^2$', fontsize=16)



plt.legend(fontsize=18)

# plt.title("MSD", fontsize=20, fontweight='bold')

# plt.savefig("/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/our_article/images/MSD_concentrations.svg", format='svg')
# plt.savefig("/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/our_article/images/MSD_concentrations.png", format='png')



plt.show()