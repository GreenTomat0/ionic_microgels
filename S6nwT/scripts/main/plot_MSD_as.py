# Here we plot MSD vs. tau (lag time) or MSD/(a_s)^2, where a_s is first peak of g(r)


import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MSD





# # read a_s
# def read_a_s():

# 	t = []
# 	a_s = []
# 	with open('input_data/a_s.dat') as f:
# 		next(f)
# 		for row in f:
# 			t.append( int(row.split('\t')[0]) )
# 			a_s.append( float(row.split('\t')[1]) )

# 	df_a_s = pd.DataFrame({'temperature': t, 'a_s': a_s})


# 	return df_a_s



# df_a_s = read_a_s()



# plot msd/a_s
plt.figure(figsize=(11,7))
plt.rcParams.update({'font.size': 14})



#--- PLOT S5 FOR 15 C ---#
S6_15 = pd.read_csv('/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6/data_out/backup/feb20_S6_EMSD.csv')



tau_15 = S6_15['lag time t']
MSD_15 = list(S6_15['dr^2'])

# a_s_15 = df_a_s.loc[df_a_s.temperature == 15, 'a_s'].item()
# MSD_a_s_15 = [x/(a_s_15**2) for x in MSD_15] 


plt.plot(tau_15[:1000], MSD_15[:1000], lw=3, label='15' + r'$^{\circ}C$')



#--- PLOT S5 FOR DIFFERENT TEMPERATURES ---#
for t in MSD.temperature:

	data_cond = MSD.data[MSD.data['temperature'] == t]

	tau = data_cond['lag time t']
	MSD_ = data_cond['dr^2']

	# a_s = df_a_s.loc[df_a_s.temperature == t, 'a_s'].item()
	# MSD_a_s = [x/(a_s**2) for x in MSD_] 


	plt.plot(tau[:1000], MSD_[:1000], lw=3, label=f'{t}' + r'$^{\circ}C$')





plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 20
plt.rcParams["figure.autolayout"] = True


plt.xlabel(r'$\tau$ [sec]', fontsize=28) # Lag time
plt.ylabel(r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]', fontsize=28)
# plt.ylabel(r'$\langle \Delta r^2 \rangle / a_s^2$', fontsize=16)

plt.xscale('log')
plt.yscale('log')

plt.legend(fontsize=16)

plt.title("MSD, S6", fontsize=20, fontweight='bold')



plt.show()