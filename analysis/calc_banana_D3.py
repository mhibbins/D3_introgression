import sys 
import random

banana_data = []

with open(sys.argv[1], 'r') as banana_file: #read in banana alignment 
	for line in banana_file:
		banana_data.append(str.strip(line))

Banksii_sequence = ''.join(banana_data[banana_data.index('>Banksii')+1:banana_data.index('>burmannica')]) #Get Banksii sequence
burmannica_sequence = ''.join(banana_data[banana_data.index('>burmannica')+1:banana_data.index('>malaccensi')]) #Get burmannica sequence
malaccensi_sequence = ''.join(banana_data[banana_data.index('>malaccensi')+1:banana_data.index('>zebrina')]) #get malaccensi sequence

#Function to calculcate D3

def calculate_D3(Banksii, burmannica, malaccensi):

	D_Banksii_burmannica, D_Banksii_malaccensi, D_burmannica_malaccensi = 0, 0, 0

	for i in range(len(Banksii)): #Count # pairwise differences
		if Banksii[i] != burmannica[i]:
			D_Banksii_burmannica += 1
		if Banksii[i] != malaccensi[i]:
			D_Banksii_malaccensi += 1
		if burmannica[i] != malaccensi[i]:
			D_burmannica_malaccensi += 1

	#Per-site divergence  
	D_Banksii_burmannica, D_Banksii_malaccensi, D_burmannica_malaccensi = float(D_Banksii_burmannica)/len(Banksii), float(D_Banksii_malaccensi)/len(Banksii), float(D_burmannica_malaccensi)/len(Banksii)
	
	#Three pairwise divergence comparisons 
	three_pairwise = [(D_Banksii_burmannica - D_Banksii_malaccensi)/float(D_Banksii_burmannica + D_Banksii_malaccensi + 0.0000001), (D_Banksii_burmannica - D_burmannica_malaccensi)/float(D_Banksii_burmannica + D_burmannica_malaccensi + 0.0000001), (D_Banksii_malaccensi - D_burmannica_malaccensi)/float(D_Banksii_malaccensi - D_burmannica_malaccensi + 0.0000001)]
	
	
	three_pairwise_abs = [abs(value) for value in three_pairwise] #Get absolute values of comparisons

        index_min = min(xrange(len(three_pairwise_abs)), key=three_pairwise_abs.__getitem__) #get index of D3 value
	
	D3 = three_pairwise[index_min] #D3 is the difference of smallest magnitude 

	return D3


def bootstrap_D3(Banksii, burmannica, malaccensi, n_replicates):

	D3_distribution = [] #list for distribution of D3 statistics

	for i in range(n_replicates):

		Banksii_bootstrap = []
		burmannica_bootstrap = []
		malaccensi_bootstrap = []

		#sample bootstrap windows
		for j in range(1000):

			bootstrap_index = random.randint(0, len(Banksii)-8330) #index to sample alignment
			Banksii_bootstrap.append(Banksii[bootstrap_index:bootstrap_index+8330])
			burmannica_bootstrap.append(burmannica[bootstrap_index:bootstrap_index+8330])
			malaccensi_bootstrap.append(malaccensi[bootstrap_index:bootstrap_index+8330])
		 
		#concatenate windows
		Banksii_bootstrap = ''.join(Banksii_bootstrap)
		burmannica_bootstrap = ''.join(burmannica_bootstrap)
		malaccensi_bootstrap = ''.join(malaccensi_bootstrap)

		#estimate D3
		D3_distribution.append(calculate_D3(Banksii_bootstrap, burmannica_bootstrap, malaccensi_bootstrap))

	D3_value = calculate_D3(Banksii, burmannica, malaccensi) #actual value of D3

	significance_count = 0 #count of bootstrap values more extreme than observed 

	for i in range(len(D3_distribution)): 
		if D3_value > D3_distribution[i]:
			significance_count += 1

	rank = float(significance_count)/len(D3_distribution) #rank of observed value with respect to bootstrap

	p = 1 - (2*abs(0.5 - rank))  #p-value	

	for value in D3_distribution:
		print(value)	

print(bootstrap_D3(Banksii_sequence, burmannica_sequence, malaccensi_sequence, 10000))


