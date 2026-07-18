from math import ceil
import numpy as np
from tqdm import tqdm

from tenso.prototypes.heom import system_multibath # Propagator
from tenso.prototypes.bath import gen_bcf # Bath correlation function generator

# Propagation schemes to compare; each run is written to '<ps_method>.dat.log'
ps_methods = ['ps1', 'vmf']

bath_simulation = gen_bcf(
    re_d=[540],    # Reorganization energy in cm-1
    width_d=[70],  # Width of the DL spectral density in cm-1
    freq_b=[1243], # Central Frequency of the Brownian Spectral density in cm-1
    re_b=[161.6], # Reorganization energy of the Brownian Spectral density in cm-1
    width_b=[10],  # Width of the spectral density in cm-1
    temperature=300, # Temperature in Kelvin
    decomposition_method='Pade', # Decomposition method for the bath correlation function
    n_ltc=1, # Number of low-temperature correction terms
)
# Initialize system Hamiltonian
H = np.array([[1500/2, 600/2], [600/2, -1500/2]], dtype=np.complex128)

end_time = 1000.0 # End time in fs
dt = 1
wfn = np.array([1.0, 0.0], dtype=np.complex128)
# Run calculations for the PS1 and VMF propagation schemes with a fixed TN structure
for ps_method in ps_methods:
    propagator = system_multibath(
        fname=ps_method,
        init_rdo=np.outer(wfn, wfn.conj()),
        sys_ham=H,
        sys_ops=[np.array([[0.5, 0.0], [0.0, -0.5]], dtype=np.complex128)],
        bath_correlations=[bath_simulation],
        dim=20,
        end_time=end_time,
        step_time=dt,
        frame_method='tree2', # TN structure fixed for all runs
        stepwise_method='simple', # Plain stepwise propagation (no mixed scheme)
        ps_method=ps_method, # Propagation scheme: 'ps1' or 'vmf'
    )
    progress_bar = tqdm(propagator, total=ceil(end_time / dt))

    for _t in (progress_bar):
        progress_bar.set_description(f'[{ps_method}] @{_t:.2f} fs')
