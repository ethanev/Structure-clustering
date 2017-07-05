#!/bin/bash
#SBATCH -p defq
#SBATCH -t 00:30:00 
#SBATCH --mem=80000

./pymol -cq cluster_means_2.py

