#!/bin/bash

#SBATCH --job-name=tda_tddft_rsh
#SBATCH --output=tda_tddft_rsh.out
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute

source /projects/academic/cyberwksp21/SOFTWARE_2026/pyscf_prism_environment.sh

python tda_tddft_rsh.py > tda_tddft_rsh.dat 2>&1
