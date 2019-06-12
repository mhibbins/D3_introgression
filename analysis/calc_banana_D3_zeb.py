import sys 
import random

banana_data = []

with open(sys.argv[1], 'r') as banana_file: #read in banana alignment 
	for line in banana_file:
		banana_data.append(str.strip(line))

Banksii_sequence = ''.join(banana_data[banana_data.index('>Banksii')+1:banana_data.index('>burmannica')]) #Get Banksii sequence
zebrina_sequence = ''.join(banana_data[banana_data.index('>zebrina')+1:banana_data.index('>outgroup')]) #Get zebrina sequence
malaccensi_sequence = ''.join(banana_data[banana_data.index('>malaccensi')+1:banana_data.index('>zebrina')]) #get malaccensi sequence
outgroup_sequence = ''.join(banana_data[banana_data.index('>outgroup')+1:])

#Function to calculcate D3

def calculate_D3(Banksii, zebrina, malaccensi):

	D_Banksii_zebrina, D_Banksii_malaccensi, D_zebrina_malaccensi = 0, 0, 0

	for i in range(len(Banksii)): #Count # pairwise differences
		if Banksii[i] != zebrina[i]:
			D_Banksii_zebrina += 1
		if Banksii[i] != malaccensi[i]:
			D_Banksii_malaccensi += 1
		if zebrina[i] != malaccensi[i]:
			D_zebrina_malaccensi += 1

	#Per-site divergence  
	D_Banksii_zebrina, D_Banksii_malaccensi, D_zebrina_malaccensi = float(D_Banksii_zebrina)/len(Banksii), float(D_Banksii_malaccensi)/len(Banksii), float(D_zebrina_malaccensi)/len(Banksii)
	
		
	#Three pairwise divergence comparisons 
	three_pairwise = [(D_Banksii_zebrina - D_Banksii_malaccensi)/float(D_Banksii_zebrina + D_Banksii_malaccensi + 0.0000001), (D_Banksii_zebrina - D_zebrina_malaccensi)/float(D_Banksii_zebrina + D_zebrina_malaccensi + 0.0000001), (D_Banksii_malaccensi - D_zebrina_malaccensi)/float(D_Banksii_malaccensi - D_zebrina_malaccensi + 0.0000001)]
	
	
	three_pairwise_abs = [abs(value) for value in three_pairwise] #Get absolute values of comparisons

        index_min = min(xrange(len(three_pairwise_abs)), key=three_pairwise_abs.__getitem__) #get index of D3 value
	
	D3 = three_pairwise[index_min] #D3 is the difference of smallest magnitude 

	return D_Banksii_zebrina, D_Banksii_malaccensi, D_zebrina_malaccensi,  D3


def calculate_D(Banksii, zebrina, malaccensi, outgroup):
	
	count_ABBA = 0
	count_BABA = 0

	for i in range(len(Banksii)):
		if zebrina[i] == malaccensi[i] and zebrina[i] != Banksii[i] and Banksii[i] == outgroup[i]: #ABBA sites
			count_ABBA += 1
		if zebrina[i] == Banksii[i] and zebrina[i] != malaccensi[i] and malaccensi[i] == outgroup[i]: #BABA sites 
			count_BABA += 1

	return count_ABBA, count_BABA,  float(count_ABBA - count_BABA)/(count_ABBA + count_BABA)


def bootstrap_D3(Banksii, zebrina, malaccensi, n_replicates):

	D3_distribution = [] #list for distribution of D3 statistics

	for i in range(n_replicates):

		Banksii_bootstrap = []
		zebrina_bootstrap = []
		malaccensi_bootstrap = []

		#sample bootstrap windows
		for j in range(1000):

			bootstrap_index = random.randint(0, len(Banksii)-8330) #index to sample alignment
			Banksii_bootstrap.append(Banksii[bootstrap_index:bootstrap_index+8330])
			zebrina_bootstrap.append(zebrina[bootstrap_index:bootstrap_index+8330])
			malaccensi_bootstrap.append(malaccensi[bootstrap_index:bootstrap_index+8330])
		 
		#concatenate windows
		Banksii_bootstrap = ''.join(Banksii_bootstrap)
		zebrina_bootstrap = ''.join(zebrina_bootstrap)
		malaccensi_bootstrap = ''.join(malaccensi_bootstrap)

		#estimate D3
		D3_distribution.append(calculate_D3(Banksii_bootstrap, zebrina_bootstrap, malaccensi_bootstrap))

	D3_value = calculate_D3(Banksii, zebrina, malaccensi) #actual value of D3

	significance_count = 0 #count of bootstrap values more extreme than observed 

	for i in range(len(D3_distribution)): 
		if D3_value > D3_distribution[i]:
			significance_count += 1

	rank = float(significance_count)/len(D3_distribution) #rank of observed value with respect to bootstrap

	p = 1 - (2*abs(0.5 - rank))  #p-value	

	for value in D3_distribution:
		print(value)	

print(calculate_D3(Banksii_sequence, zebrina_sequence, malaccensi_sequence))
print(calculate_D(Banksii_sequence, zebrina_sequence, malaccensi_sequence, outgroup_sequence))
#print(bootstrap_D3(Banksii_sequence, zebrina_sequence, malaccensi_sequence, 10000))


