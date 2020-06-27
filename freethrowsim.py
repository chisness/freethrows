import numpy as np 
import random
import seaborn as sns
import matplotlib.pyplot as plt

#number of attempts
#number of shots per attempt
#number of shots total 

def ftsim(num_sims, resets, reset_dict, p_make = 0.78):
	results = []
	shots_total = 0
	for _ in range(sims):
		success = 0
		trials = 0
		while success == 0:
			num_shots = 0
			misses = 0
			makes = 0
			
			while misses < 11 and makes < 90:
				if resets == True and makes < reset_dict[misses]: #reset condition
					break 
				rn = np.random.uniform() #maybe better to make list at beg. and take from there
				if rn <= p_make:
					makes += 1
				else:
					misses += 1
				#print(f'misses: {misses}, makes: {makes}')
			
			shots_total += makes + misses
			#print('shots total: ', shots_total)

			trials += 1
			if makes == 90:
				success = 1
		results.append(trials)
		print(trials)

	print(results)
	print(sum(results)/len(results))

	print('shots per bet:', shots_total/(sims))

	fig, ax = plt.subplots()
	ax = sns.distplot(results)
	plt.show()

binom = {0: 0, 1: 5, 2: 10, 3: 16, 4: 22, 5: 28, 6: 34, 7: 40, 8: 47, 9: 54, 10: 63} 
rl_99 = {0: 0, 1: 5, 2: 10, 3: 16, 4: 22, 5: 28, 6: 34, 7: 40, 8: 47, 9: 54, 10: 63} 
#dict is number of misses and number of makes, reset if makes is less than value given misses 
reset_dict = binom #which reset strategy to use
sims = 100
ftsim(sims, True, reset_dict)
ftsim(sims, False, reset_dict)