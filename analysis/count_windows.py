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

sp1_genome = ''.join(sp1_genome)
sp2_genome = ''.join(sp2_genome)
sp3_genome = ''.join(sp3_genome)
sp4_genome = ''.join(sp4_genome)

sp1_genome = [sp1_genome[i:i+5000] for i in range(0, len(sp1_genome), 5000)]
sp2_genome = [sp2_genome[i:i+5000] for i in range(0, len(sp2_genome), 5000)]
sp3_genome = [sp3_genome[i:i+5000] for i in range(0, len(sp3_genome), 5000)]
sp4_genome = [sp4_genome[i:i+5000] for i in range(0, len(sp4_genome), 5000)]

def count_dBC_dAC(sp1_window, sp2_window, sp3_window, sp4_window):
	'''
	Estimates dBC and dAC in the given window	
	'''

	BC_diff, AC_diff = 0, 0

        for i in range(len(sp1_window)):
		if sp2_window[i] != sp3_window[i]:
			BC_diff += 1
		if sp2_window[i] != sp4_window[i]:
			AC_diff += 1

	return BC_diff, AC_diff

window = []
excess = []

for i in range(len(sp1_genome)):
	dBC, dAC = count_dBC_dAC(sp1_genome[i], sp2_genome[i], sp3_genome[i], sp4_genome[i])
	window.append(i)
	excess.append(dBC-dAC)


negatives = 0

for i in range(len(excess)):
	if excess[i] < 0:
		negatives += 1

print(negatives/float(len(excess)))
