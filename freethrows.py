import numpy as np 
import random
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

GAMMA = .99
EPSILON = .00001
FREETHROWRATE = 0.78

#state is [free throws made, free throws missed]
rewards = np.zeros((91, 12)) #rewards for each state 
for i in range(11):
	rewards[90][i] = 100 #90 = win

class value_iteration:
	def __init__(self):
		self.policy = np.zeros((90, 11), dtype=np.float128)
		self.val_state = np.zeros((91, 12), dtype=np.float128)

	def bellman(self, state_made, state_missed, action, val_state):
		if action == 1: 
			made_val = FREETHROWRATE * (rewards[state_made+1][state_missed] + GAMMA * val_state[state_made+1][state_missed])
			missed_val = (1 - FREETHROWRATE) * (rewards[state_made][state_missed+1] + GAMMA * val_state[state_made][state_missed+1])
			return made_val + missed_val
		else: #action == 0 
			return val_state[0][0]

	def val_iteration(self):
		iteration = 0
		state00 = []
		while True:
			delta = 0
			for state_made in range(0,90): #go through each state
				for state_missed in range(0, 11):
					v = self.val_state[state_made][state_missed] 
					if state_made == 0 and state_missed == 0:
						state00.append(v)
					val_action = np.zeros(2)
					for action in range(2): #reset = 0, shoot = 1
						val_action[action] = self.bellman(state_made, state_missed, action, self.val_state)
					self.val_state[state_made][state_missed] = np.max(val_action)
					delta = max(delta, np.abs(self.val_state[state_made][state_missed] - v)) #find maximum change over all states
					print(delta)

			print('iteration', iteration)
			iteration += 1
			if delta < EPSILON:
				break
		for i in range(len(state00)):
			print(f'[0,0] state value is {state00[i]} on iteration {i}')
		return self.policy_it()

	def policy_it(self):
		for state_made in range(0,90): #go through each state
			for state_missed in range(0, 11):
				val_action = np.zeros(2)
				for action in range(2):
					val_action[action] = self.bellman(state_made, state_missed, action, self.val_state)
				if val_action[0] > val_action[1]:# + 10e-10: 
					best_action = 0
				else:
					best_action = 1
				#best_action = np.argmax(val_action)
				self.policy[state_made][state_missed] = best_action
		return self.val_state, self.policy




vi = value_iteration()
v, p = vi.val_iteration()
# print(p)
# print(v)
# print(v[80])
# print(v[85])
# print(v[89])
# print(v[90])
# print(v[10])


fig, ax = plt.subplots()
im = ax.imshow(p, origin = 'lower', aspect = 'auto')
ax.set_xticks(np.arange(0,11))
ax.set_yticks(np.arange(0,90))
plt.xlabel('Shots missed')
plt.ylabel('Shots made')
plt.title(f'Freethrow strategy with GAMMA = {GAMMA} and p_make = {FREETHROWRATE}')
plt.grid(color='black', linestyle='-', linewidth=1)
# for i in range(0,11):
# 	for j in range(0,90):
# 		text = ax.text(i, j, str(round(v[j][i],2)), ha="center", va="center", fontsize=5)

for i in range(1, 11):
	for j in range(0, 90):
		if v[j][i] > v[0][0]:
			text = ax.text(i, j+1, j, ha='center', va='center', fontsize=10)
			#text = ax.text(i, j, str(round(v[j][i],2)), ha="center", va="center", fontsize=6)
			break

import matplotlib.ticker as ticker
# plt.rc('xtick', labelsize=6)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=6)    # fontsize of the tick labels

ax.tick_params(axis='both', which='major', labelsize=5)
ax.tick_params(axis='both', which='minor', labelsize=5)

#plt.plot([], [], ' ', label="Reset in purple zone \nShoot in yellow zone")
# plt.rc('axes', labelsize=6)    # fontsize of the x and y labels

#ax.yaxis.set_major_locator(ticker.MultipleLocator(10))

#ax.set_yticks(np.arange(0, 90, 10))
plt.grid(b=None)
ax.set_xticklabels(np.arange(0,11))
ax.set_yticklabels(np.arange(0,90))
#ax.set_yticklabels(np.arange(0,91, 10))
#ax.legend(loc='upper left')

plt.show()