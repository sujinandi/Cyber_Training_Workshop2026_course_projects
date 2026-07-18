import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

path='two_baths.dat.log'
plt.rcParams["font.family"] = "serif"

def load_spinboson_pops(fname, convert_to_ps=False):
    try:
        arr = np.genfromtxt(fname, dtype=complex, comments="#", skip_header=1)
    except OSError:
        print("Could not load file.")
        exit()
    t = arr[:,0].real
    if convert_to_ps:
        t *= 1e-3
    pops = np.vstack((arr[:,1].real, arr[:,4].real)).T
    # purity Tr(rho^2) = rho00^2 + rho11^2 + 2*rho01*rho10
    purity = (arr[:,1]**2 + arr[:,4]**2 + 2 * arr[:,2] * arr[:,3]).real
    return t, pops, purity

time_series, population_series, purity_series = load_spinboson_pops(path)

fig, (ax1, ax2) = plt.subplots(
    1,2, figsize=(6.8, 2.0), sharex=True
)
# --- (a) populations ---
ax1.plot(time_series, population_series[:,0], label=r"$\rho_{00}$")
ax1.plot(time_series, population_series[:,1], label=r"$\rho_{11}$")

ax1.set_ylabel("Population", labelpad=6)
ax1.set_xlabel("Time (fs)", labelpad=6)
ax1.set_xlim(0, 500)
ax1.legend(loc="best", fontsize=8, frameon=False)

# --- (b) purity ---
ax2.plot(time_series, purity_series, color="k")

ax2.set_ylabel(r"Purity $\mathrm{Tr}(\rho^2)$", labelpad=6)
ax2.set_xlabel("Time (fs)", labelpad=6)
ax2.set_ylim(0.45, 1.05)

fig.tight_layout()
plt.savefig("SpinBoson_populations.png", bbox_inches='tight', dpi=300, transparent=True)
plt.show()
