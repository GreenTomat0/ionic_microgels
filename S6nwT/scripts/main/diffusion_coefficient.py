# Here we difine diffusion coefficient from the slopes of MSD
# The slopes of MSD are defined in "slope_MSD.py"



import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from slope_MSD import slopes_MSD
import MSD





diff_coef = pd.DataFrame(columns=['temperature', 'diffusion_coefficient'])

for t in MSD.temperature:

	slope_row = slopes_MSD()[slopes_MSD()['temperature'] == t]
	# diffusion coef.
	D = slope_row.slope / 4.

	new_row = pd.DataFrame({'temperature': [t], 'diffusion_coefficient': [D.values[0]]})
	diff_coef = pd.concat([diff_coef, new_row], ignore_index=True)



# read 15C from file
diff_coef_T15 = pd.read_csv('/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/scripts/main/output_data/diffusion_coefficient.csv')


S5_row = diff_coef_T15[diff_coef_T15['sample'] == 6 ]

# create new row for output DataFrame
T15_row = pd.DataFrame({'temperature': [15], 'diffusion_coefficient': [S5_row['diffusion_coefficient'].values[0]]})

# add T15_row as a first string in diff_coef DataFrame
diff_coef = pd.concat([pd.DataFrame(T15_row, index=[0]), diff_coef]).reset_index(drop=True)

diff_coef.set_index('temperature', inplace=True)

print(diff_coef)


# write DataFrame to file
diff_coef.to_csv('output_data/diffusion_coefficient.csv')
