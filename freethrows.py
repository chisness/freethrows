import numpy as np 
import random
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import collections 

EPSILON = 0.1 
VAL_ITERATION_EPS = 0.001
WIN = 10000 #reward if succeed 90/100
FREETHROWRATE = 0.8

#state is [free throws made, free throws missed]
rewards = np.zeros((91, 11)) #rewards for each state 
for i in range(11):
	rewards[90][i] = 100 #90 = win

class value_iteration:
	def __init__(self):
		self.policy = np.zeros((90, 11), dtype=np.float128)
		self.val_state = np.zeros((91, 11), dtype=np.float128)

	def bellman(self, state_made, state_missed, action, val_state):
		if action == 1: 
			return FREETHROWRATE * (rewards[state_made+1][state_missed] + GAMMA * val_state[state_made+1][state_missed]) + (1 - FREETHROWRATE) * (rewards[state_made][state_missed+1] + GAMMA * val_state[state_made][state_missed+1])
		else: #action == 0 
			return val_state[0][0]

	def val_iteration(self):
		while True:
			delta = 0
			for state_made in range(1,90): #go through each state
				for state_missed in range(1, 11):
					v = self.val_state[state_made, state_missed] 
					val_action = np.zeros(2)
					for action in range(2): #reset = 0, shoot = 1
						val_action[action] = self.bellman(state_made, state_missed, action, self.val_state)
					self.val_state[state_made][state_missed] = np.max(val_action)
					delta = max(delta, np.abs(self.val_state[state_made, state_missed] - v)) #find maximum change over all states
			if delta < VAL_ITERATION_EPS:
				break
		return self.policy_it()

	def policy_it(self):
		for state_made in range(1,90): #go through each state
			for state_missed in range(1, 11):
				val_action = np.zeros(2)
				for action in range(2):
					val_action[action] = self.bellman(state_made, state_missed, action, self.val_state)
				best_action = np.argmax(val_action)
				self.policy[state_made][state_missed] = best_action
		return self.val_state, self.policy




vi = value_iteration()
v, p = vi.val_iteration()
print(v)
print(p)
