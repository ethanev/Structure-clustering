#!/bin/bash
#SBATCH -p defq
#SBATCH -t 12:00:00
#SBATCH --mem=80000
#SBATCH --ntasks-per-node=64
#SBATCH --nodes=1

distance=10000
epsilon=1
round=1
chunks="$(python Generate_data_chunks.py)"
while [ $distance -gt $epsilon ]
do
  touch temp
  echo "clustering round: $round"
  if [ $round -eq 1 ]; then
    python Generate_center.py > centers.txt
  fi
  echo Getting centers!
  centers=`cat centers.txt`
  echo $centers
  sleep 2
  echo Starting structure-to-cluster assignment
  for chunk in $chunks;
  do
    ./pymol -cq assign_struct_to_center.py -- $centers $chunk &
    sleep 3
  done
  wait
  #sleep 5m
  ./pymol -qc update_mean.py > centers.txt & 
  wait
  distance=`cat latest_distance.txt`
  round=`expr $round + 1`
done
