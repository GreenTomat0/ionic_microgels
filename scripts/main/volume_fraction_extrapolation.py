# volume fraction determined from high magnificent S6 sample
# vol. frac. for all other samples are determined as proportional to their concentrations



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# volume fraction of S6 (concentrated)

def V_sphere_segment(h, r1, r2):

	return np.pi*h*(3.*r1*r1 + 3.*r2*r2 + h*h)/6



def read_file():

	slices = []
	count = [] # number of particles on the slice

	input_dir = f'input_data/slice_count_S6.dat'
	with open(input_dir) as f:
		next(f)
		for rows in f:
			slices.append(int(rows.split(' ')[0]))
			count.append(int(rows.split(' ')[1]))


	return slices, count



def volume_fraction_S6(slice_volume, one_microgel_volume):

	slices, count = read_file()
	volume_fraction = []

	for i in range(len(slices)):
		
		all_microgels_volume = count[i] * one_microgel_volume

		volume_fraction.append(all_microgels_volume / slice_volume)

	vol_fr_S6 = sum(volume_fraction) / len(volume_fraction)

	# print(f'vol_fr_S6 = {vol_fr_S6}')


	return vol_fr_S6




# volume fraction of other samples

def volume_fraction_S(conc, vf_S6):

	s_s = list(conc.loc[:, 'sample'].values) # samples
	conc_s = list(conc.loc[:, 'concentration'].values) # concentrations

	conc_S6 = conc.loc[conc['sample'] == 6, 'concentration'].item() # concentration of S6

	
	vf = []
	for c in conc_s:
		vf.append( c * vf_S6 / conc_S6 )


	return s_s, vf





width = 7.04 # width of the slice in micron
height = 6.66 # height of the slice in micron



# UPPER LIMIT of volume fraction S6 (when only the centers of particles are on the slide )
h = 0.05 # thickness of segment
R = 0.95743 

r_low = R # average radius of microgels in micron
r_top = np.sqrt(r_low*r_low - h*h)

slice_volume = width * height * (2 * h)
one_microgel_volume = 2.*V_sphere_segment(h, r_low, r_top)

vf_S6_max = volume_fraction_S6(slice_volume, one_microgel_volume)
# vf_max = volume_fraction_S(vol_fr_S6_max)



# LOWER LIMIT of volume fraction S6 (when only the tops of particles are on the slide )
h = 0.1 # thickness of a sphere segment
h_to_top = R - 0.01 # distance from the center to the top radius
h_to_low = h_to_top - h

r_low = np.sqrt(R*R - h_to_low*h_to_low)
r_top = np.sqrt(R*R - h_to_top*h_to_top) # this radius is radius of the microgel at the distance 0.899 micron from the center (almost top. top is 0.9 micron)

slice_volume = width * height * h
one_microgel_volume = V_sphere_segment(h, r_low, r_top)

vf_S6_min = volume_fraction_S6(slice_volume, one_microgel_volume)
# vf_min = volume_fraction_S(vol_fr_S6_min)



# MEAN VALUE of volume fraction S6
vf_S6 = 0.5*(vf_S6_max - vf_S6_min)


# VOLUME FRACTIONS OF OTHER SAMPLES
concentration = pd.read_csv('input_data/Concentrations.csv')

S, VF = volume_fraction_S(concentration, vf_S6)


# WRITE TO FILE volume_fraction.csv
df = pd.DataFrame({'sample': S, 'volume_fraction': VF})
df.set_index('sample', inplace=True) # inplace=True to make changes in current df, otherwise df will not change

print(df)	

df.to_csv("output_data/volume_fraction.csv")
