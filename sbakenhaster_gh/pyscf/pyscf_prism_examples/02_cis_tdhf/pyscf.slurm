#!/bin/bash

#SBATCH --job-name=02_cis_tdhf
#SBATCH --output=02_cis_tdhf.dat
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

source /projects/academic/cyberwksp21/SOFTWARE_2026/pyscf_prism_environment.sh

python 02_cis_tdhf.py > 02_cis_tdhf.dat  2>&1
