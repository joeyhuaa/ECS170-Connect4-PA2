import random
import time
import pygame
import math
import numpy as np
from connect4 import connect4
from copy import deepcopy

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

def Evaluation(env, player, Idx, Us):
	#todo - implement state
	if Us and env.gameOver(Idx, player):
		return math.inf
	elif not Us and env.gameOver(Idx, player):
		return -(math.inf)
	
	weight = [
		[3, 4, 5, 7, 5, 4, 3],
		[4, 6, 8, 10, 8, 6, 4],
		[5, 8, 12, 13, 12, 8, 5],
		[5, 8, 12, 13, 12, 8, 5],
		[4, 6, 8, 10, 8, 6, 4],
		[3, 4, 5, 7, 5, 4, 3]
	]
	
	base = [
		[3, 3, 3, 3, 3, 3, 3],
		[3, 3, 3, 3, 3, 3, 3],
		[3, 3, 3, 3, 3, 3, 3],
		[3, 3, 3, 3, 3, 3, 3],
		[3, 3, 3, 3, 3, 3, 3],
		[3, 3, 3, 3, 3, 3, 3]
	]

	
	#print("Eval Board1: ", env.board)
	#print(move)
	

	a = env.board
	b = a
	#c = 1 / a
	#print(c)
	a = a * 2
	#print("Eval Board1: ", a)
	a = base - a
	#print("Eval Board1: ", a)
	a = a * 2 * b
	#print("Eval Board1: ", a)

	e = weight * a
	
	#print("Players' Weight: ", b)
	

	#print("Players Weight: ", e)
	
	Sum = np.sum(e)
	#print("Sum here: ", Sum)		####################################
	return Sum


class minimaxAI(connect4Player):
	
	
	def play(self, env, move):



		player = 0
		if np.sum(env.board) % 3 == 0:
			player = 1
		else:
			player = 2
		
		
		#self.opponent.position

		maxDepth = 3
		possibleMove = env.topPosition >= 0
		Max = -math.inf
		a = -1
		
		for p, i in enumerate(possibleMove):
			#print("Minimax P1: ", p)
			currEnv = env
			env = self.simulateMove(deepcopy(env), i, player)
			#env = a
			simEnv = env
			
			#print("Minimax P2: ", p)
			max_v = -math.inf
			
			Value = self.Min(move, maxDepth - 1, env, player, p, simEnv)
			#print("There asdjfkljasdlkjfalskdjf;laskdjfl;askjdflasdkjf;lasjdflskjfla;sdj")
			#print("i: ", i)
			#print("Minimax P3: ", p)			# p returns 0 - 6
			#print("Value: ", Value)
			#print("Max: ", Max)
			#print("Min: ", Value)
			env = currEnv
			if Value > Max:
				#print("Minimax P4: ", p)
				Max = Value
				#print("adsfasdfsa", Max)
				#print("Padfasdf: ", p)
				move[:] = [p]

		#print("a: ", a)
			
		#move[:] = [i]
	
	def simulateMove(self, env, move, player):
		#print("Simulate Player: ", player)
		#print("Simulate move: ", move)
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		#env.history[0].append(move)
		#print(move)
		#print("Simulated: ", env.board)
		return env


	# move is a column number 0-6
	def Max(self, move, depth, env, player, Idx, simEnv):
	
		#print("Max here")			######################################################
		
		if env.gameOver(Idx, player) or depth == 0:  #env.gameOver(Idx, player) or 
			#print("Idx: ", Idx)
			#print("Eval: ", Evaluation(env, player, move))
			#print(env.board)
			print("Max Eval")
			return Evaluation(deepcopy(env), player, Idx, True)				###############################
		possibleMove = env.topPosition >= 0
		max_v = -(math.inf)
		curEnv = env
		for p, i in enumerate(possibleMove):
			if i:
				#print("Max P: ", p)
				env = self.simulateMove(deepcopy(env), p, player)
				#env = simEnv
				#curEnv = simEnv
				#print("After: ", env.board)
				Idx = p
				print("Max 1:   ", max_v)
				value = max(max_v, self.Min(move, depth - 1, env, 3 - player, Idx, simEnv))
				#max_v = value
				if value > max_v:
					max_v = value
				print("Max 2:   ", value)
				#curEnv = simEnv
				env = curEnv
		return max_v

	def Min(self, move, depth, env, player, Idx, simEnv):
	
		#print("Min here")			######################################################
	
		if env.gameOver(Idx, player) or depth == 0:		# env.gameOver(Idx, player) or 
			print("Min Eval")
			return Evaluation(deepcopy(env), player, Idx, False)		###############################
		possibleMove = env.topPosition >= 0
		min_v = math.inf
		#print(depth)
		curEnv = env
		for p, i in enumerate(possibleMove):
			if i:
				print("Min P1: ", p)
				#print("Min Player: ", player)
				env = self.simulateMove(deepcopy(env), p, player)
				#print("Min P2: ", p)
				#env = simEnv
				#curEnv = simEnv
				Idx = p
				print("Min 1: ", min_v)
				value = min(min_v, self.Max(move, depth - 1, env, 3 - player, Idx, simEnv))
				print("Min 2: ", value)
				min_v = value
				#curEnv = simEnv
				env = curEnv
		return min_v


	# def iterativeDeepening(self, env, move):
	# 	maxDepth = 6
	# 	while (True):
	# 		move[:] = [self.miniMax(env, maxDepth, move)]
	# 		limit += 1



############################################################################################


class alphaBetaAI(connect4Player):

	def play(self, env, move):
		pass


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)

#<<<<<<< HEAD



#=======
# hello
#>>>>>>> 78f9ecef53802dca1387c929823fae15a494481f
