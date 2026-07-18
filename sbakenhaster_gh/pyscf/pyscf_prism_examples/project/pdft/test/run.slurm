#!/bin/bash

#SBATCH --job-name=example1
#SBATCH --output=example2.out
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute

source /projects/academic/cyberwksp21/SOFTWARE_2026/pyscf_prism_environment.sh

python casci_pdft2.py > casci_pdft2.dat 2>&1
