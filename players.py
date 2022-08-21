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

def Evaluation(env, player, colNum, Us):
	if Us and env.gameOver(colNum, player): # if we win
		return math.inf
	elif not Us and env.gameOver(colNum, player): # if we lose
		return -(math.inf)
	
	weight = [
		[3, 4, 5, 7, 5, 4, 3],
		[4, 6, 8, 10, 8, 6, 4],
		[5, 8, 12, 13, 12, 8, 5],
		[5, 8, 12, 13, 12, 8, 5],
		[4, 6, 8, 10, 8, 6, 4],
		[3, 4, 5, 7, 5, 4, 3]
	]

	# num of 1s in col 3 - num of 2s in col 3
	num_1s = 0
	num_2s = 0
	for row in env.board:
		if row[3] == 1:
			num_1s += 1
		elif row[3] == 2:
			num_2s += 1
	
	print('num_1s', num_1s)
	print('num_2s', num_2s, '\n========')

	value = num_1s - num_2s
	return value


class minimaxAI(connect4Player):
	def play(self, env, move):
		maxDepth = 10
		possible = env.topPosition >= 0
		Max = -math.inf
		
		simEnv = deepcopy(env)
		for colNum, canPlay in enumerate(possible):
			if canPlay:
				child = self.simulateMove(simEnv, colNum, self.position)
				Value = self.Min(child, maxDepth-1, simEnv, colNum)
				if Value > Max:
					Max = Value
					move[:] = [colNum]
		
	def simulateMove(self, env, move, player):
		# print("Simulate Player: ", player)
		#print("Simulate move: ", move)
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
		print('history', env.history)
		# print(move)
		# print("Simulated: ", env.board)
		return env


	# move is a column number 0-6
	def Max(self, child, depth, simEnv, colNum):

		#print("Max here")			######################################################
		
		if simEnv.gameOver(colNum, self.position) or depth == 0: 
			return Evaluation(simEnv, self.position, child, True)				###############################
		possible = simEnv.topPosition >= 0
		max_v = -(math.inf)
		for colNum, canPlay in enumerate(possible):
			if canPlay:
				child = self.simulateMove(simEnv, colNum, self.opponent.position)
				max_v =  max(max_v, self.Min(child, depth-1, simEnv, colNum))
		return max_v

	def Min(self, child, depth, simEnv, colNum):
	
		#print("Min here")			######################################################
	
		if simEnv.gameOver(colNum, self.opponent.position) or depth == 0:		# env.gameOver(colNum, player) or 
			return Evaluation(simEnv, self.opponent.position, child, False)		###############################
		possible = simEnv.topPosition >= 0
		max_v = math.inf
		for colNum, canPlay in enumerate(possible):
			if canPlay:
				child = self.simulateMove(simEnv, colNum, self.position)
				max_v =  min(max_v, self.Max(child, depth-1, simEnv, colNum))
		return max_v


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
