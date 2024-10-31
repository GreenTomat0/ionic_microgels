import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit





# --- fit with parabola --- #
def fit_points_curve(x_data, y_data):

	def curve_func(x, a, b, c):
		return a * x*x + b * x + c

	popt, pcov = curve_fit(curve_func, x_data, y_data)
	a_opt, b_opt, c_opt = popt
	
	x_curve = np.arange(0, max(x_data), 0.01)
	y_curve = curve_func(x_curve, a_opt, b_opt, c_opt)


	return x_curve, y_curve



# --- fit with straigh line --- #
def fit_points_line(x_data, y_data, liquid_or_glass):

	def curve_func(x, a, b):
		return a * x + b


	popt, pcov = curve_fit(curve_func, x_data, y_data)
	a_opt, b_opt = popt

	if liquid_or_glass == 'l':
		x_curve = np.arange(min(x_data) - 0.05, max(x_data) + 0.2, 0.01)
	elif liquid_or_glass == 'g':
		x_curve = np.arange(min(x_data) - 0.1, max(x_data) + 0.05, 0.01)
	else:
		print('Is it liquid or glass?')
	
	y_curve = curve_func(x_curve, a_opt, b_opt)


	return x_curve, y_curve



# --- find intersection point --- #
def intersection(line1, line2):
	x1, y1, x2, y2 = line1
	x3, y3, x4, y4 = line2

	# Calculate intersection point
	intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
	intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))


	return intersection_x, intersection_y



# --- plot all points --- #
def plot_MSD_vs_volFrac(DIR):

	df = pd.read_csv(DIR + 'VF_MSD.csv')

	x = df.loc[:, 'volume_fraction'].values
	y = df.loc[:, 'dr^2'].values

	plt.scatter(x, y, edgecolor='black', facecolor='green', s=600)


	return list(x), list(y)





# --- MAIN --- #
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 20
plt.rcParams["figure.autolayout"] = True

x_main, y_main = plot_MSD_vs_volFrac('/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/scripts/main/output_data/')
x_S5, y_S5 = plot_MSD_vs_volFrac('/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S5nwT/scripts/main/output_data/')
x_S6, y_S6 = plot_MSD_vs_volFrac('/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6nwT/scripts/main/output_data/')



X = x_main + x_S5 + x_S6
Y = y_main + y_S5 + y_S6

# for i in range(len(X)):
# 	print(f'{X[i]}\t{Y[i]}')
# print("\n----------------\n")

X_sort = [x for x, y in sorted(zip(X, Y))]
Y_sort = [y for x, y in sorted(zip(X, Y))]

# for i in range(len(X_sort)):
# 	print(f'{X_sort[i]}\t{Y_sort[i]}')



inx = [6, 7, 8, 9, 10, 11, 12, 14]
x_ch = [X_sort[i] for i in inx]
y_ch = [Y_sort[i] for i in inx]

X_line_l, Y_line_l = fit_points_line(x_ch, y_ch, 'l')
plt.plot(X_line_l, Y_line_l, ls='--', c='darkgray')


inx = [-1, -2, -3, -4]
x_ch = [X_sort[i] for i in inx]
y_ch = [Y_sort[i] for i in inx]

X_line_g, Y_line_g = fit_points_line([1.0] + x_ch, [0.] + y_ch, 'g')
plt.plot(X_line_g, Y_line_g, ls='--', c='darkgray')


#--- POINT OF INTERSECTION ---#
line1 = (X_line_l[0], Y_line_l[0], X_line_l[-1], Y_line_l[-1])
line2 = (X_line_g[0], Y_line_g[0], X_line_g[-1], Y_line_g[-1])

x_is, y_is = intersection(line1, line2)

plt.scatter(x_is, y_is, s=400, lw=3, edgecolor='orange', facecolor='none')
plt.text(x_is-0.01, y_is-0.06, '('+'{:.2f}'.format(x_is)+', '+'{:.2f}'.format(y_is)+')', fontsize=12, fontweight='bold', ha='center', va='bottom')




# #--- PLOT POINTS ---#
# for t in merged_df.index:

# 	x = merged_df['volume_fraction'][t]
# 	y = merged_df['dr^2'][t]

# 	plt.scatter(x, y, edgecolor='black', facecolor='green', s=600)
# 	plt.text(x, y, 'T' + str(t), fontsize=10, va='center', ha='center', c='white')



#--- POINT DECORATION ---#

plt.title('MSD vs. Volume fraction', fontsize=20, fontweight='bold')

plt.xlabel(r'$\phi_{eff}$', fontsize=28) # Volume fraction
plt.ylabel(r'$\langle \Delta r^2 \rangle [\mu$m$^2]$', fontsize=28) # [\mu$m$^2]



plt.show()