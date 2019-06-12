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

#Function for the ABBA-BABA statistic 

def calculate_D(sp1_genome, sp2_genome, sp3_genome, sp4_genome):
	
	ABBA_count, BABA_count = 0, 0

	for i in range(len(sp1_genome)):
		if sp2_genome[i] == sp3_genome[i] and sp2_genome[i] != sp4_genome[i] and sp4_genome[i] == sp1_genome[i]: #ABBA sites
			ABBA_count += 1
		elif sp2_genome[i] == sp4_genome[i] and sp3_genome[i] != sp4_genome[i]	and sp3_genome[i] == sp1_genome[i]: #BABA sites
			BABA_count += 1

	D = (float(ABBA_count) - float(BABA_count))/(float(ABBA_count) + float(BABA_count)) #D statistic
	
	return D

#Function for D3 

def calculate_D3(sp2_genome, sp3_genome, sp4_genome):
	
	D23, D24, D34 = 0, 0, 0

	for i in range(len(sp2_genome)): #Count number of pairwise differences
		if sp2_genome[i] != sp3_genome[i]:
			D23 += 1
		if sp2_genome[i] != sp4_genome[i]:
			D24 += 1
		if sp3_genome[i] != sp4_genome[i]:
			D34 += 1

	D23, D24, D34 = float(D23)/len(sp1_genome), float(D24)/len(sp1_genome), float(D34)/len(sp1_genome) #Divide by genome length (100 million bp)

	three_pairwise = [(D24-D23)/(D23+D24), (D23-D34)/(D23+D34), abs(D24-D34)/(D24+D34)] #Get the three pairwise divergence comparisons 

	three_pairwise_abs = [abs(value) for value in three_pairwise] #Get absolute values of comparisons

	index_min = min(xrange(len(three_pairwise_abs)), key=three_pairwise_abs.__getitem__) #get index of D3 value

	D3 = three_pairwise[index_min]  #Get value of D3

	return D3

#Function to estimate variance of D and D3 using block jackknife

def D_D3_block_bootstrap(sp1_genome, sp2_genome, sp3_genome, sp4_genome, n_replicates):
	
	D_estimates = []
	D3_estimates = []
	
	for i in range(n_replicates): #for each bootstrap replicate

		sp1_bootstrapped, sp2_bootstrapped, sp3_bootstrapped, sp4_bootstrapped = [], [], [], [] #to store bootstrapped genomes

		for j in range(100): #for each resampling window
		
			sampling_index = random.randint(0, 990000) #index to slice 

			#sample windows 
			sp1_bootstrapped.append(sp1_genome[sampling_index:sampling_index+10000])
			sp2_bootstrapped.append(sp2_genome[sampling_index:sampling_index+10000])
			sp3_bootstrapped.append(sp3_genome[sampling_index:sampling_index+10000])
			sp4_bootstrapped.append(sp4_genome[sampling_index:sampling_index+10000])
		
		#concatenate resampling windows
		sp1_bootstrapped = ''.join(sp1_bootstrapped)
		sp2_bootstrapped = ''.join(sp2_bootstrapped)
		sp3_bootstrapped = ''.join(sp3_bootstrapped)
		sp4_bootstrapped = ''.join(sp4_bootstrapped)

		#estimate statistics 
		D_estimates.append(calculate_D(sp1_bootstrapped, sp2_bootstrapped, sp3_bootstrapped, sp4_bootstrapped))
		D3_estimates.append(calculate_D3(sp2_bootstrapped, sp3_bootstrapped, sp4_bootstrapped))
	
	#estimate means
	mean_D = sum(D_estimates)/float(len(D_estimates))
	mean_D3 = sum(D3_estimates)/float(len(D3_estimates))	

	#estimate variance
	D_stdev = ((sum([(x - mean_D)**2 for x in D_estimates]))/len(D_estimates))**(0.5)
	D3_stdev = ((sum([(x - mean_D3)**2 for x in D3_estimates]))/len(D3_estimates))**(0.5)
	return D_stdev, D3_stdev

print(calculate_D(sp1_genome, sp2_genome, sp3_genome, sp4_genome), calculate_D3(sp2_genome, sp3_genome, sp4_genome), D_D3_block_bootstrap(sp1_genome, sp2_genome, sp3_genome, sp4_genome, 1000))

