import json
import random
from random import choices

class AI:

	def __init__(self):
		self.games = 0 # No of games played by the AI in the current run
		self.dump_freq = 20 # No of games after which data is dumped into json
		self.step_size = 0.7
		self.reward = {'alive' : 1, 'dead' : -1000}
		self.discount = 1.0
		self.last_state = "32_36_10"
		self.last_action = 0
		self.moves = []
		self.load_q()

	def set_last_state(self,  x_dist, y_dist, vel):
		self.last_state = self.get_state(x_dist, y_dist, vel)
	# FUNCTION TO LOAD Q VALUES FROM A JSON qvalues.json
	def load_q(self):

		self.qvalues = {}
		try:
			f = open('qvalues.json', 'r')
			self.qvalues = json.load(f)
			f.close()
		except IOError:
			pass

	# FUNCTION WHICH RETURNS HOW THE AI SHOULD ACT IN A PARTICULAR GAME STATE; 1 FOR JUMP AND 0 FOR DO-NOTHING
	def act(self, x_dist, y_dist, vel): 
		# GETS THE GAME STATE FOR THE GIVEN PARAMETERS
		state = self.get_state(x_dist, y_dist, vel)

		# ADDS THE EXPERIENCE TO THE HISTORY OF MOVES
		self.moves.append((self.last_state, self.last_action, state))
		self.last_state = state

		if self.qvalues[state][0] >= self.qvalues[state][1]:
			self.last_action = 0
			#print("NO JUMP")
			return 0
		else:
			self.last_action = 1
			#print("JUMP")
			return 1

	# FUNCTIONS WHICH UPDATES THE Q VALUES
	def update_q(self, dump_q = True):

		#REVERSING THE LIST OF MOVES
		history = list(reversed(self.moves))

		index = 0
		
		high_death_flag = True if int(history[0][2].split("_")[1])>60 else False
		low_death_flag = True if int(history[0][2].split("_")[1])<48 else False

		for exp in history:

			state = exp[0]
			act = exp[1]
			res_state = exp[2]

			# ASSIGNING REWARDS BASED ON THE SITUATION
			if index == 0 or index == 1:
				cur_reward = self.reward['dead']
			elif high_death_flag and act:
				cur_reward = self.reward['dead']
				print("High death")
				high_death_flag = False
			else:
				cur_reward = self.reward['alive']

			# UPDATING THE Q VALUE
			self.qvalues[state][act] = (1-self.step_size) * (self.qvalues[state][act]) + self.step_size * ( cur_reward + self.discount*max(self.qvalues[res_state]) )
			index += 1

		self.games += 1
		self.moves = []
		if dump_q == True:
			self.dump_q()
		#print("Q-values updated in class.")

	# FUNCTION TO DUMP THE Q VALUES IN THE JSON FILE
	def dump_q(self, force = False):
		if self.games%self.dump_freq == 0 or force:
			f = open("qvalues.json", "w")
			json.dump(self.qvalues, f)
			f.close()
			print("Q-values updated in json.")

	#FUNCTION TO RETURN THE GAME STATE GIVEN THE PARAMETERS
	def get_state(self, x_dist, y_dist, vel):

		x_dist = (x_dist + 60)//10
		y_dist = (y_dist + 600)//10
		return str(int(x_dist)) + "_" + str(int(y_dist)) + "_" + str(int(vel))