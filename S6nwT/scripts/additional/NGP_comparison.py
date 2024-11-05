import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# from scipy.stats import norm
from scipy.interpolate import splrep, BSpline
import sys
sys.path.append('../main/')
import MSD

# print(MSD.samples)
# print("\n")


def read_NGP(t):

	file_path = f"/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6nwT/S6nwT{t}/data_out/backup/NGP_S6T{t}.dat"

	tau = []
	ngp = []

	with open(file_path) as f:
		next(f)
		for row in f:
			tau.append(float(row.split(',')[0]))
			ngp.append(float(row.split(',')[1]))


	return tau, ngp



def read_MSD(t):

	file_path = f"/Users/miroshni/Documents/Unifr/Unifr_work/glass_transition_in_emulsions/TrackPy/microgels/feb20/S6nwT/S6nwT{t}/data_out/backup/MSD_S6T{t}.dat"

	msd = []

	with open(file_path) as f:
		next(f)
		for row in f:
			msd.append(float(row.split(',')[1]))


	return msd



# fit with Gaussian
def Gaussian(x, a, x0, sigma, h):

	return a * np.exp(-(x - x0)**2 / (2 * sigma**2)) + h



# fit with Parabola
def Parabola(x, a, b, c):

	return a * x**2 + b * x + c



# # fit with Cubic
# def Cubic(x, a, b, c, d):

# 	# return a * x**3 + b * x**2 + c * x + d
# 	return a * x*x*x + b * x*x + c * x + d



# # fit with Quadratic
# def Quadratic(x, a, b, c, d, e):

# 	return a * x*x*x*x + b * x*x*x + c * x*x + d * x + e



def draw_NGP(temperatures):

	for t in temperatures:
		tau, NGP = read_NGP(t)
		MSD = read_MSD(t)

		plt.plot(tau, NGP, ls='-', marker='o', ms=5, label=f'T = {t} ' + r'$^{\circ} C$')

		# FITTING
		x = np.arange(tau[0], tau[-1], 0.1)

		# smooth curves
		tck = splrep(tau, NGP, s=30)
		y_spline = BSpline(*tck)(x)
		

		# fit with Gaussian
		if t in [18, 25]:

			popt, _ = curve_fit(Gaussian, x, y_spline)

			y = Gaussian(x, popt[0], popt[1], popt[2], popt[3])
			plt.plot(x, y, c='k', ls='-', lw=3) # label=f'fit T = {t}' + r'$^{\circ} C$'

		else:
			# plot smoothed curve if it wasn't fitted with Gaussian
			plt.plot(x, y_spline, c='k', ls='-', lw=2)





plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 20
plt.rcParams["figure.autolayout"] = True

draw_NGP(MSD.temperature)

plt.title('NGP, S6 (6.84 wt%)', fontsize=20, fontweight='bold')

plt.xlabel(r'$\tau$ [sec]', fontsize=28)
plt.ylabel(r'$\alpha_2$', fontsize=28)

# plt.xscale('log')
# plt.yscale('log')

plt.xlim(0, 5)
plt.ylim(0, 70)

plt.legend(fontsize=16)


plt.show()