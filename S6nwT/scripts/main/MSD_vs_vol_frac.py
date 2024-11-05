import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import MSD




# DEFINE MSD IN A SINGLE POINT
def MSD_one_point(point):
	#point is lag time where we take our MSD

	df_1point = pd.DataFrame()

	eps = 0.0001

	for t in MSD.temperature:

		df = MSD.data[MSD.data['temperature'] == t]

		condition = abs(df['lag time t'] - point) < eps

		df_1point = pd.concat([df_1point, df[condition]], ignore_index=True)


	T15_row = pd.DataFrame({'lag time t': [MSD_one_point_T15(point)['lag time t'].values[0]], 'dr^2': [MSD_one_point_T15(point)['dr^2'].values[0]], 'temperature': 15})
	df_1point = pd.concat([pd.DataFrame(T15_row, index=[0]), df_1point]).reset_index(drop=True)

	# print('df_1point:')
	# print(df_1point)


	return df_1point



# MSD OF S6 SAMPLE FOR 15C:
def MSD_one_point_T15(point):

	df_1point = pd.DataFrame()

	eps = 0.0001

	file_path = f'/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6/data_out/backup/feb20_S6_EMSD.csv'
	df = pd.read_csv(file_path)

	condition = abs(df['lag time t'] - point) < eps

	df_1point = pd.concat([df_1point, df[condition]], ignore_index=True)


	# print('15C, df_1point:')
	# print(df_1point)


	return df_1point





vf = pd.read_csv('output_data/volume_fraction.csv')
msd = MSD_one_point(0.5)

merged_df = vf.merge(msd, on='temperature')
merged_df.set_index('temperature', inplace=True)
merged_df.drop(columns=['lag time t'], inplace=True) # delete column 'lag time t'
merged_df.to_csv('output_data/VF_MSD.csv') # save to file

print(merged_df)



# --- straigh line --- #
def fit_points(x_data, y_data, liquid_or_glass):

	def curve_func(x, a, b):
		return a * x + b


	popt, pcov = curve_fit(curve_func, x_data, y_data)

	a_opt, b_opt = popt

	if liquid_or_glass == 'l':
		x_curve = np.arange(min(x_data) - 0.05, max(x_data) + 0.1, 0.01)
	elif liquid_or_glass == 'g':
		x_curve = np.arange(min(x_data) - 0.1, max(x_data) + 0.25, 0.01)
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





plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 20
plt.rcParams["figure.autolayout"] = True


#--- PLOT POINTS ---#
for t in merged_df.index:

	x = merged_df['volume_fraction'][t]
	y = merged_df['dr^2'][t]

	plt.scatter(x, y, edgecolor='black', facecolor='green', s=600)
	plt.text(x, y, 'T' + str(t), fontsize=10, va='center', ha='center', c='white')




#--- DRAW LINES ---#
x_line = merged_df.loc[:, 'volume_fraction']
y_line = merged_df.loc[:, 'dr^2']

x1_curve, y1_curve = fit_points([1.25] + list(x_line[:-3]), [0] + list(y_line[:-3]), 'l')
plt.plot(x1_curve, y1_curve, ls='--', c='grey')

x2_curve, y2_curve = fit_points(x_line[-2:], y_line[-2:], 'g')
plt.plot(x2_curve, y2_curve, ls='--', c='grey')



#--- POINT OF INTERSECTION ---#
line1 = (x1_curve[0], y1_curve[0], x1_curve[-1], y1_curve[-1])
line2 = (x2_curve[0], y2_curve[0], x2_curve[-1], y2_curve[-1])

x_is, y_is = intersection(line1, line2)

plt.scatter(x_is, y_is, s=400, lw=3, edgecolor='orange', facecolor='none')
plt.text(x_is-0.05, y_is-0.017, '('+'{:.2f}'.format(x_is)+', '+'{:.2f}'.format(y_is)+')', fontsize=12, fontweight='bold', ha='center', va='bottom')


#--- POINT DECORATION ---#
# plt.ylim([-0.07, 0.48])

plt.title('MSD vs. Volume fraction, S6', fontsize=20, fontweight='bold')

plt.xlabel(r'$\phi_{eff}$', fontsize=28) # Volume fraction
plt.ylabel(r'$\langle \Delta r^2 \rangle [\mu$m$^2]$', fontsize=28) # [\mu$m$^2]



plt.show()