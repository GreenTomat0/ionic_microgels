There is the order and description of how to analyze microgels:

1. MSD.py -	contains the list of samples or temperatures. Auxiliary program code. Doesn't perform tasks separately.

2. plot_MSD_as.py -	plot MSD (or MSD/a_s) curves.

3. slope_MSD.py -	calculate slopes of MSD curves. You can change the point and the length of the area on a curve where to define a slope. Auxiliary program code. Doesn't perform tasks separately.

4. diffusion_coefficient.py -	calculate diffusion coefficient slope slopes, defined with slope_MSD.py. Input is diffusion_coefficient.csv

5. volume_fraction_extrapolation.py -	this script which defines volume fraction for S6 and calculate volume fractions for other samples as a proportion to their concentrations. Input is volume_fraction.csv file

6. vol_frac_vs_diff_coef.py -	here we plot diffusion coefficient as a function of volume fraction

7. MSD_vs_vol_frac.py -	here we plot MSD vs. volume fraction. MSD is taken in chosen point from feb20_S{s}_EMSD.csv, where 's' is a sample number. 