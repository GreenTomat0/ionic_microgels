# Here we difine diffusion coefficient from the slopes of MSD
# The slopes of MSD are defined in "slope_MSD.py"



import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from slope_MSD import slopes_MSD
import MSD





# diffusion coef. D = slope_of_MSD/4 (for 2D), D = slope_of_MSD/6 (for 3D)


diff_coef = pd.DataFrame(columns=['sample', 'diffusion_coefficient'])

for s in MSD.samples:

	slope_row = slopes_MSD()[slopes_MSD()['sample'] == s]
	# diffusion coef.
	D = slope_row.slope / 4.

	new_row = pd.DataFrame({'sample': [s], 'diffusion_coefficient': [D.values[0]]})
	diff_coef = pd.concat([diff_coef, new_row], ignore_index=True)



diff_coef.set_index('sample', inplace=True)

print(diff_coef)


# write DataFrame to file
diff_coef.to_csv('output_data/diffusion_coefficient.csv')