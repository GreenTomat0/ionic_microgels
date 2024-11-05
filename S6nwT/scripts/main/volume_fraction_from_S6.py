# volume fraction determined from S6 (15 C)
# Here we are reading an average radius of S5 particles, determined from extrapolation of S6. 


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# read an average value of volume fraction of S6 sample. This value is calculated for 15 C
def read_S6_15():

	DIR = f'/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/scripts/main/output_data/volume_fraction.csv'
	df = pd.read_csv(DIR)

	vf = df.loc[df['sample'] == 6, 'volume_fraction'].item()


	return vf



# extrapolate the value of radius for temperatures differ from 15 C
def volume_fractions():

	temperature = [15, 18, 25, 27, 29, 31, 33] # temperature in C
	radius = [0.957, 0.9192, 0.851, 0.834, 0.821, 0.6617, 0.449] # radii in micrometer

	S6_15_vf = read_S6_15()
	S6_15_rad = radius[0]

	vol_frac = [S6_15_vf]

	for R in radius[1:]:
		vol_frac.append( S6_15_vf * R / S6_15_rad )


	return temperature, vol_frac



def write_to_file():

	T, VF = volume_fractions()

	df = pd.DataFrame({'temperature': T, 'volume_fraction': VF})

	df.set_index('temperature', inplace=True) # inplace=True to make changes in current df, otherwise df will not change

	print(df)	

	df.to_csv("output_data/volume_fraction.csv")




write_to_file()



# T, VF = volume_fractions()

# print("temp\tvol_frac")
# for t, vf in zip(T, VF):
# 	print(f"{t}\t{vf}")