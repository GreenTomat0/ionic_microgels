# Here we plot diffusion coefficient as a function of volume fraction


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import UnivariateSpline





def DC(x):

	return 0.25*(1. - 1.56*x)*(1. - 0.27*x) #0.0565 - from images #0.065 - from data




DIR = 'output_data/'
vf = pd.read_csv(DIR + 'volume_fraction.csv') # <-- sample, volume_fraction 
dc = pd.read_csv(DIR + 'diffusion_coefficient.csv') # <-- sample, diffusion_coefficient

vf.set_index('sample', inplace=True)
dc.set_index('sample', inplace=True)

merged_df = vf.merge(dc, on='sample')

# print(merged_df)




# # here we define diffusion coefficient from the formula for hard spheres (see DC(x) function)
dc_theory = []

for t in merged_df.index:

	cur_vf = merged_df['volume_fraction'][t]
	dc_theory.append(DC(cur_vf))
	
merged_df['diffusion_coefficient_THEORY'] = dc_theory

print(merged_df)





plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 20
plt.rcParams["figure.autolayout"] = True


# EXPERIMENTAL (flom MSD slopes)
x_exper = merged_df.loc[:, 'volume_fraction']
y_exper = merged_df.loc[:, 'diffusion_coefficient']
plt.plot(x_exper, y_exper, linestyle='', marker='^', markersize=18, markerfacecolor='yellow', markeredgecolor='k', label='Experiment')



# THEORETICAL (form DC(x) function)
x_theory = merged_df.loc[:, 'volume_fraction']
y_theory = merged_df.loc[:, 'diffusion_coefficient_THEORY']

# FITTING with polinom
x_fit = np.arange(min(x_theory), max(x_theory), 0.01)
p = np.polyfit(x_theory, y_theory, 2)
y_fit = np.polyval(p, x_fit)

plt.plot(x_fit, y_fit, linestyle='--', color='purple')
plt.plot(x_theory, y_theory, linestyle='', marker='v', markersize=18, markerfacecolor='purple', markeredgecolor='k', label='Theory')



# plt.xscale('log')
plt.yscale('log')

plt.legend()

plt.xlabel(r'$\phi_{eff}$', fontsize=28) # Volume fraction
plt.ylabel(r'$D_s\; [\mu$m$^2 / s]$', fontsize=28) # Diffusion coef.

plt.title("Diffusion coefficient", fontsize=20, fontweight='bold')


plt.show()
