#!/bin/bash

#Change working directory
cd /N/dc2/scratch/mhibbins/introgression_statistic/

#Simulate coalescent trees in ms. 
for i in {1..100}
do
msdir/ms 4 1000 -T -I 4 1 1 1 1 -ej 4.0 2 1 -ej 0.6 3 2 -ej 0.3 4 3 -es 0.05 3 0.9 -ej 0.05 5 2 | tail -n +4 | grep -v // >revision_seq_sims/vary_Ne/vary_Ne_gamma_0.1/vary_Ne_gamma_0.1_trees_$i.txt

#Split tree file into four smaller temporary files
split -500 revision_seq_sims/vary_Ne/vary_Ne_gamma_0.1/vary_Ne_gamma_0.1_trees_$i.txt gamma_0.1_trees_

#Simulate sequences from these temporary tree files using Seq-Gen. 
Seq-Gen/source/seq-gen -m HKY -l 1000 -s 0.00025 <gamma_0.1_trees_aa >> revision_seq_sims/vary_Ne/vary_Ne_gamma_0.1/vary_Ne_gamma_0.1_seqs_$i.txt
Seq-Gen/source/seq-gen -m HKY -l 1000 -s 0.005 <gamma_0.1_trees_ab >> revision_seq_sims/vary_Ne/vary_Ne_gamma_0.1/vary_Ne_gamma_0.1_seqs_$i.txt
Seq-Gen/source/seq-gen -m HKY -l 1000 -s 0.01 <gamma_0.1_trees_ac >> revision_seq_sims/vary_Ne/vary_Ne_gamma_0.1/vary_Ne_gamma_0.1_seqs_$i.txt
Seq-Gen/source/seq-gen -m HKY -l 1000 -s 0.02475 <gamma_0.1_trees_ad >> revision_seq_sims/vary_Ne/vary_Ne_gamma_0.1/vary_Ne_gamma_0.1_seqs_$i.txt

#Remove temporary files
rm gamma_0.1_trees_aa
rm gamma_0.1_trees_ab
rm gamma_0.1_trees_ac
rm gamma_0.1_trees_ad

done


