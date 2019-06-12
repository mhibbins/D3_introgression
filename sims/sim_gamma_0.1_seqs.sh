#!/bin/bash

#Change working directory 
cd /N/dc2/scratch/mhibbins/introgression_statistic/

#Simulate coalescent trees in ms. This simulates introgression from taxon 3 into taxon 2, at a time of 0.2N generations, with an admixture proportion of 10%. It also cleans up the tree outputs for input into Seq-Gen.  
for i in {1..100}
do
msdir/ms 4 1000 -T -I 4 1 1 1 1 -ej 4.0 2 1 -ej 0.6 3 2 -ej 0.3 4 3 -es 0.05 3 0.9 -ej 0.05 5 2 | tail -n +4 | grep -v // >seq_sims/gamma_0.1_sims/gamma_0.1_trees_$i.txt
#Simulate sequences from trees using Seq-Gen. This simulates a sequence of 1000 bp for each gene tree, under the Jukes-Cantor model. 
Seq-Gen/source/seq-gen -m HKY -l 1000 -s 0.01 <seq_sims/gamma_0.1_sims/gamma_0.1_trees_$i.txt > seq_sims/gamma_0.1_sims/gamma_0.1_seqs_$i.txt
done 

