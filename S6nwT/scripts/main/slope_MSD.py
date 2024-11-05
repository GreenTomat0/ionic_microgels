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

	slopes = pd.DataFrame(columns=['slope', 'temperature'])

	point = 0.5 #0.5 # point where we determine the slope
	eps = 0.2 #0.2

	for t in MSD.temperature:

		data_cond = MSD.data[MSD.data['temperature'] == t]

		tau = data_cond['lag time t']
		MSD_ = data_cond['dr^2']

		# plt.plot(tau, MSD_, label=f'T{t}')


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


		new_slope = pd.DataFrame({'slope': [a], 'temperature': [t]})
		slopes = pd.concat([slopes, new_slope], ignore_index=True)

	
	# print(slopes)

	# plt.legend()
	# plt.show()


	return slopes


# slopes_MSD()
