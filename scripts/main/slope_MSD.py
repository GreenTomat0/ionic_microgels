import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import MSD




# define the true objective function for approximation a curve by line
def objective(x, a, b):

	return a * x + b



def slopes_MSD():

	slopes = pd.DataFrame(columns=['slope', 'sample'])

	point = 0.3 #1.
	eps = 0.2 #0.2

	for s in MSD.samples:

		data_cond = MSD.data[MSD.data['sample'] == s]

		tau = data_cond['lag time t']
		MSD_ = data_cond['dr^2']

		# plt.plot(tau, MSD_, label=f'S{s}')


		dtau_list = tau[(tau > point - eps) & (tau < point + eps)]

		left_limit = dtau_list.iloc[0]
		right_limit = dtau_list.iloc[-1]
 
		idx_left = tau[tau == left_limit].index[0]
		idx_right = tau[tau == right_limit].index[0]

		dMSD_list = MSD_[idx_left:idx_right+1]

		# curve fit
		popt, _ = curve_fit(objective, dtau_list, dMSD_list)

		# summarize the parameter values
		a, b = popt
		# print('y = %.3f * x + %.3f' % (a, b))

		# define a sequence of inputs between the smallest and largest known inputs
		x_line = np.arange(left_limit, right_limit, 8.e-3)
		# calculate the output for the range
		y_line = objective(x_line, a, b)


		# plt.plot(x_line, y_line, color='black')
		# dtau = x_line[-1] - x_line[0]
		# dMSD_ = y_line[-1] - y_line[0]

		# if a < 0:
		# 	a = -a


		new_slope = pd.DataFrame({'slope': [a], 'sample': [s]})
		slopes = pd.concat([slopes, new_slope], ignore_index=True)

	
	# print(slopes)

	# plt.legend()
	# plt.show()


	return slopes


# slopes_MSD()
