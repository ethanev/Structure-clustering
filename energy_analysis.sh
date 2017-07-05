#!/bin/bash
#SBATCH -p defq
#SBATCH -t 10:00:00
#SBATCH --mem=80000
#SBATCH --ntasks-per-node=42
#SBATCH --nodes=1

./pymol -c five_struct_energy_analysis.py 
wait
chmod +x release_lowest_structs.sh
./release_lowest_structs.sh

