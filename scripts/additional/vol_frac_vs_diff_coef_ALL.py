# Here we plot diffusion coefficient as a function of volume fraction for ALL samples, including temperature dependence S5 and S6


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import UnivariateSpline





def DC(x):

	return 0.25*(1. - 1.56*x)*(1. - 0.27*x) #0.0565 - from images #0.065 - from data



def diffCoef_volFrac(DIR, ID):

	# ID is 'sample' (for different concentrations) of 'temperature' (for different temperatures, i.e. S5 and S6)

	# DIR = 'output_data/'
	vf = pd.read_csv(DIR + 'volume_fraction.csv') # <-- sample, volume_fraction 
	dc = pd.read_csv(DIR + 'diffusion_coefficient.csv') # <-- sample, diffusion_coefficient

	vf.set_index(ID, inplace=True)
	dc.set_index(ID, inplace=True)

	merged_df = vf.merge(dc, on=ID)


	return merged_df



merged_df_MAIN = diffCoef_volFrac('../main/output_data/', 'sample')
merged_df_S5 = diffCoef_volFrac('/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S5nwT/scripts/main/output_data/', 'temperature')
merged_df_S6 = diffCoef_volFrac('/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6nwT/scripts/main/output_data/', 'temperature')



# here we define diffusion coefficient from the formula for hard spheres (see DC(x) function)
def diffCoef_theory(merged_df):
	dc_theory = []

	for t in merged_df.index:

		cur_vf = merged_df['volume_fraction'][t]
		dc_theory.append(DC(cur_vf))
		
	merged_df['diffusion_coefficient_THEORY'] = dc_theory

	print(merged_df)


	return merged_df



merged_df_MAIN = diffCoef_theory(merged_df_MAIN)
merged_df_S5 = diffCoef_theory(merged_df_S5)
merged_df_S6 = diffCoef_theory(merged_df_S6)



plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 20
plt.rcParams["figure.autolayout"] = True


def plot_diffCoef_vs_volFrac(merged_df, label):

	if label == True:
		label1 = 'Experiment'
		label2 = 'Theory'
	else:
		label1 = ''
		label2 = ''

	# EXPERIMENTAL (flom MSD slopes)
	x_exper = merged_df.loc[:, 'volume_fraction']
	y_exper = merged_df.loc[:, 'diffusion_coefficient']
	plt.plot(x_exper, y_exper, linestyle='', marker='^', markersize=18, markerfacecolor='yellow', markeredgecolor='k', label=label1)


	# THEORETICAL (form DC(x) function)
	x_theory = merged_df.loc[:, 'volume_fraction']
	y_theory = merged_df.loc[:, 'diffusion_coefficient_THEORY']


	# FITTING with polinom
	x_fit = np.arange(min(x_theory), max(x_theory), 0.01)
	p = np.polyfit(x_theory, y_theory, 2)
	y_fit = np.polyval(p, x_fit)

	plt.plot(x_fit, y_fit, linestyle='--', color='purple')
	plt.plot(x_theory, y_theory, linestyle='', marker='v', markersize=18, markerfacecolor='purple', markeredgecolor='k', label=label2)



plot_diffCoef_vs_volFrac(merged_df_MAIN, True)
plot_diffCoef_vs_volFrac(merged_df_S5, False)
plot_diffCoef_vs_volFrac(merged_df_S6, False)


# plt.xscale('log')
plt.yscale('log')

plt.legend()

plt.xlabel(r'$\phi_{eff}$', fontsize=28) # Volume fraction
plt.ylabel(r'$D_s\; [\mu$m$^2 / s]$', fontsize=28) # Diffusion coef.

plt.title("Diffusion coefficient, all samples", fontsize=20, fontweight='bold')


plt.show()