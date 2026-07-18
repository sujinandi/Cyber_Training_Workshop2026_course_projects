import copy
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pyspawn
import numpy as np
au_to_fs = 0.02418884254
au_to_ev = 13.6
au_to_ang = 0.529177

# open sim.hdf5 for processing
simfile = os.path.join(os.pardir, "sim.hdf5")
an = pyspawn.fafile(simfile)

# create N.dat and store the data in times and N
an.fill_electronic_state_populations(column_filename="N.dat")
an.fill_labels()
an.fill_istates()
an.get_numstates()

times = an.datasets["quantum_times"]
el_pop = an.datasets["electronic_state_populations"]
istates = an.datasets["istates"]
labels = an.datasets["labels"]
ntraj = len(an.datasets["labels"])
nstates = an.datasets['numstates']

an.fill_nuclear_bf_populations()

# write files with energy data for each trajectory
an.fill_trajectory_energies(column_file_prefix="E")

# write file with time derivative couplings for each trajectory
#an.fill_trajectory_tdcs(column_file_prefix="tdc")

# compute Mulliken population of each trajectory
#an.fill_mulliken_populations(column_filename="mull.dat")
#mull_pop = an.datasets["mulliken_populations"]

# list all datasets
#an.list_datasets()

N = an.datasets["nuclear_bf_populations"]

for n in range(ntraj):
    with open('{}_pop.dat'.format(labels[n]), 'a') as f:
        for i in range(len(N)):
            f.write('{} {}\n'.format(math.ceil(times[i][0]*au_to_fs*10.0) / 10.0, N[i,n+1]))
    with open('Labels.dat','a') as f:
        f.write('{}\n'.format(labels[n]))
