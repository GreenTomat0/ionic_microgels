# This is for samples S5, S34, S2, S8, S6

import numpy as pn
import matplotlib.pyplot as plt



a_s = [1.83, 1.58, 1.485, 1.28]
vf = [0.14, 0.566, 0.89, 1.445]


fig = plt.figure(figsize=(12, 8))
plt.rcParams['font.size'] = 20

plt.plot(vf, a_s, ls='-', marker='o', markerfacecolor='none', color='k', ms=14, lw=3)

plt.xlabel(r'$\phi_{eff}$', fontsize=28) # Volume fraction
plt.ylabel(r'$a_s [\mu m]$', fontsize=28) # [\mu$m$^2]


plt.show()