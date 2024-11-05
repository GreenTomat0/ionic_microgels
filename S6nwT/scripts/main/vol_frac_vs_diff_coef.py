# Here we plot diffusion coefficient as a function of volume fraction


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import UnivariateSpline





def DC(x):

	return 0.15*(1. - 1.56*x)*(1. - 0.27*x) #0.0565 - from images #0.065 - from data




DIR = 'output_data/'
vf = pd.read_csv(DIR + 'volume_fraction.csv') # <-- temperature, volume_fraction 
dc = pd.read_csv(DIR + 'diffusion_coefficient.csv') # <-- temperature, diffusion_coefficient

vf.set_index('temperature', inplace=True)
dc.set_index('temperature', inplace=True)

merged_df = vf.merge(dc, on='temperature')

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


x_exper = merged_df.loc[:, 'volume_fraction']
y_exper = merged_df.loc[:, 'diffusion_coefficient']
plt.plot(x_exper, y_exper, linestyle='', marker='^', markersize=18, markerfacecolor='yellow', markeredgecolor='k')



# plt.xscale('log')
plt.yscale('log')

# plt.legend()

plt.xlabel(r'$\phi_{eff}$', fontsize=28) # Volume fraction
plt.ylabel(r'$D_s\; [\mu$m$^2 / s]$', fontsize=28) # Diffusion coef.

plt.title("Diffusion coefficient, S6", fontsize=20, fontweight='bold')


plt.show()
