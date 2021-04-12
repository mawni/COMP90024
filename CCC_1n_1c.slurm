#!/bin/bash

# give job a name
#SBATCH --job-name=Twt1n1c

# run on 1 cpu
#SBATCH --ntasks=1

# use physical partition
#SBATCH --partition=physical

# set max wall time 30 mins
#SBATCH --time=0-0:30:00

# email for progress
#SBATCH --mail-user=mawni@student.unimelb.edu.au
#SBATCH --mail-type=ALL

# Load required module
module purge
module load foss/2019b
module load python/3.7.4

# run program once
time srun -n 1 python3 twitterAnalytics.py