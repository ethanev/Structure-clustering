#!/bin/bash
#SBATCH -p defq
#SBATCH -t 24:00:00
#SBATCH --mem=80000

distance=10000
epsilon=1
round=1
chunks="$(python Generate_data_chunks.py)"
while [ $distance -gt $epsilon ]
do
  rm temp
  echo "clustering round: $round"
  if [ $round -eq 1 ]; then
    python Generate_center.py > centers.txt
  fi
  echo Getting centers!
  centers=`cat centers.txt`
  echo $centers
  echo Starting structure-to-cluster assignment
  for chunk in $chunks;
  do
    echo '#!/bin/bash' > test.sh
    echo '#SBATCH -p defq' >> test.sh
    echo '#SBATCH -t 00:60:00' >> test.sh
    echo '#SBATCH --mem=80000' >> test.sh
    echo "./pymol -cq assign_struct_to_center.py -- $centers $chunk " >> test.sh
    sbatch test.sh &
    sleep 10
  done
  sleep 3m
  ./pymol -qc update_mean.py > centers.txt
  sleep 10
  distance=`cat latest_distance.txt`
  round=`expr $round + 1`
done
