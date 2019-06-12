import sys 
import random

banana_data = []

with open(sys.argv[1], 'r') as banana_file: #read in banana alignment 
	for line in banana_file:
		banana_data.append(str.strip(line))

Banksii_sequence = ''.join(banana_data[banana_data.index('>Banksii')+1:banana_data.index('>burmannica')]) #Get Banksii sequence
zebrina_sequence = ''.join(banana_data[banana_data.index('>zebrina')+1:banana_data.index('>outgroup')]) #Get zebrina sequence
malaccensi_sequence = ''.join(banana_data[banana_data.index('>malaccensi')+1:banana_data.index('>zebrina')]) #get malaccensi sequence

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
	
	
	return (D_Banksii_zebrina-D_zebrina_malaccensi)/(D_Banksii_zebrina+D_zebrina_malaccensi) 

Banksii_windows = [Banksii_sequence[i:i+8000] for i in range(0, len(Banksii_sequence), 8000)]
zebrina_windows = [zebrina_sequence[i:i+8000] for i in range(0, len(zebrina_sequence), 8000)]
malaccensi_windows = [malaccensi_sequence[i:i+8000] for i in range(0, len(malaccensi_sequence), 8000)]

D3_vals = []
D3_positives = []
D3_negatives = []

for i in range(len(Banksii_windows)):
	D3_vals.append(calculate_D3(Banksii_windows[i], zebrina_windows[i], malaccensi_windows[i]))

positive_windows = 0

for i in range(len(D3_vals)):
	if D3_vals[i] > 0:
		positive_windows += 1
		D3_positives.append(D3_vals[i])
	elif D3_vals[i] < 0:
		D3_negatives.append(D3_vals[i])

print(sum(D3_positives)/float(len(D3_positives)))
print(sum(D3_negatives)/float(len(D3_negatives)))
print(float(positive_windows)/len(D3_vals)) 
