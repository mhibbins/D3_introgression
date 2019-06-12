import sys
import random

seqs = []

with open(sys.argv[1], 'r') as alignment_file: #read in the alignment file
        for line in alignment_file:
                if '4 1000' not in line:
                        seqs.append(str.strip(line)) #read in the relevant lines

sp1_genome, sp2_genome, sp3_genome, sp4_genome = [], [], [], []

for i in range(len(seqs)): #concatenate sequences into whole genome for each species 
        if '1' in seqs[i]:
                sp1_genome.append(seqs[i].split()[1])
        elif '2' in seqs[i]:
                sp2_genome.append(seqs[i].split()[1])
        elif '3' in seqs[i]:
                sp3_genome.append(seqs[i].split()[1])
        else:
                sp4_genome.append(seqs[i].split()[1])

sp1_genome, sp2_genome, sp3_genome, sp4_genome = ''.join(sp1_genome), ''.join(sp2_genome), ''.join(sp3_genome), ''.join(sp4_genome)

def add_errors(genome, rate):
	'''
	Introduces artificial errors to the given genome sequence
	at the specified rate
	'''
	new_genome = list(genome)
	
	bases = ['A', 'C', 'T', 'G']

	for i in range(0, len(new_genome), int(round((1/rate)))):
		
		base = new_genome[i]
		newbase = new_genome[i]

		while newbase == base:
			newbase = random.choice(bases)

		new_genome[i] = newbase

	return ''.join(new_genome)

def calculate_D3(sp2_genome, sp3_genome, sp4_genome):

        D23, D24, D34 = 0, 0, 0

        for i in range(len(sp2_genome)): #Count number of pairwise differences
                if sp2_genome[i] != sp3_genome[i]:
                        D23 += 1
                if sp2_genome[i] != sp4_genome[i]:
                        D24 += 1
                if sp3_genome[i] != sp4_genome[i]:
                        D34 += 1

        D23, D24, D34 = float(D23)/len(sp2_genome), float(D24)/len(sp2_genome), float(D34)/len(sp2_genome) #Divide by genome length (100 million bp)


        return (D24-D23)/(D24+D23)

def prop_D3_windows(sp2_genome, sp3_genome, sp4_genome):
	
	positives = 0

	sp2_genome_windows = [sp2_genome[i:i+5000] for i in range(0, len(sp2_genome), 5000)]
	sp3_genome_windows = [sp3_genome[i:i+5000] for i in range(0, len(sp3_genome), 5000)]
	sp4_genome_windows = [sp4_genome[i:i+5000] for i in range(0, len(sp4_genome), 5000)]

	for i in range(len(sp2_genome_windows)):
		
		window_D3 = calculate_D3(sp2_genome_windows[i], sp2_genome_windows[i], sp4_genome_windows[i])
		
		if window_D3 > 0:
			positives += 1

	return float(positives)/len(sp2_genome_windows) 

def D_D3_block_bootstrap(sp2_genome, sp3_genome, sp4_genome, n_replicates):

        D3_estimates = []

        for i in range(n_replicates): #for each bootstrap replicate

                sp2_bootstrapped, sp3_bootstrapped, sp4_bootstrapped = [], [], [] #to store bootstrapped genomes

                for j in range(100): #for each resampling window

                        sampling_index = random.randint(0, 990000) #index to slice 

                        #sample windows 
                        sp2_bootstrapped.append(sp2_genome[sampling_index:sampling_index+10000])
                        sp3_bootstrapped.append(sp3_genome[sampling_index:sampling_index+10000])
                        sp4_bootstrapped.append(sp4_genome[sampling_index:sampling_index+10000])

                #concatenate resampling windows
                sp2_bootstrapped = ''.join(sp2_bootstrapped)
                sp3_bootstrapped = ''.join(sp3_bootstrapped)
                sp4_bootstrapped = ''.join(sp4_bootstrapped)

                #estimate statistics 
                D3_estimates.append(calculate_D3(sp2_bootstrapped, sp3_bootstrapped, sp4_bootstrapped))

        #estimate means
        mean_D3 = sum(D3_estimates)/float(len(D3_estimates))

        #estimate variance
        
	D3_stdev = ((sum([(x - mean_D3)**2 for x in D3_estimates]))/len(D3_estimates))**(0.5)
        
	return D3_stdev

sp4_genome_errors = add_errors(sp4_genome, float(sys.argv[2]))
print(calculate_D3(sp2_genome, sp3_genome, sp4_genome_errors), D_D3_block_bootstrap(sp2_genome, sp3_genome, sp4_genome_errors, 1000), prop_D3_windows(sp2_genome, sp3_genome, sp4_genome))


