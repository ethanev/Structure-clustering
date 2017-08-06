#!/bin/bash
#SBATCH -p defq
#SBATCH -t 03:00:00
#SBATCH --mem=80000

./pymol -qc two_structure_distance.py 
