import sys

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

D12, D13, D14, D23, D24, D34 = 0, 0, 0, 0, 0, 0

for i in range(len(sp2_genome)): #Count number of pairwise differences
        
        if sp1_genome[i] != sp2_genome[i]:
		D12 += 1
	if sp1_genome[i] != sp3_genome[i]:
		D13 += 1
	if sp1_genome[i] != sp4_genome[i]:
		D14 += 1
        if sp2_genome[i] != sp3_genome[i]:
                D23 += 1
        if sp2_genome[i] != sp4_genome[i]:
                D24 += 1
        if sp3_genome[i] != sp4_genome[i]:
                D34 += 1



D12, D13, D14, D23, D24, D34 = float(D12)/len(sp1_genome), float(D13)/len(sp1_genome), float(D14)/len(sp1_genome), float(D23)/len(sp1_genome), float(D24)/len(sp1_genome), float(D34)/len(sp1_genome) #Divide by genome length (100 million bp)

print D12, D13, D14, D23, D24, D34

