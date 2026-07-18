#!/bin/bash

#SBATCH --job-name=b3lyp_nosing
#SBATCH --output=b3lyp_nosing.out
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute

source /projects/academic/cyberwksp21/SOFTWARE_2026/pyscf_prism_environment.sh

python b3lyp_nosing.py > b3lyp_nosing.dat 2>&1
