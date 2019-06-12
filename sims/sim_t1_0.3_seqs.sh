#!/bin/bash

#Change working directory 
cd /N/dc2/scratch/mhibbins/introgression_statistic/

#Simulate coalescent trees in ms.   
for i in {1..100}
do
msdir/ms 4 1000 -T -I 4 1 1 1 1 -ej 4.0 2 1 -ej 0.6 3 2 -ej 0.3 4 3 -es 0.05 3 0.95 -ej 0.05 5 2 | tail -n +4 | grep -v // >revision_seq_sims/t1_sims/t1_0.3_sims/t1_0.3_trees_$i.txt
#Simulate sequences from trees using Seq-Gen.  
Seq-Gen/source/seq-gen -m HKY -l 1000 -s 0.01 <revision_seq_sims/t1_sims/t1_0.3_sims/t1_0.3_trees_$i.txt > revision_seq_sims/t1_sims/t1_0.3_sims/t1_0.3_seqs_$i.txt
done 

