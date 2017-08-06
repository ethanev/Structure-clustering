#!/bin/bash
#SBATCH -p defq
#SBATCH -t 04:00:00
#SBATCH --mem=80000

./pymol -qc find_close_struct.py
