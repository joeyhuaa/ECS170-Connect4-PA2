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
		self.weight = [
			[3, 4, 5, 5, 5, 4, 3],
			[4, 6, 8, 8, 8, 6, 4],
			[5, 8, 12, 13, 12, 8, 5],
			[5, 8, 12, 13, 12, 8, 5],
			[4, 6, 8, 10, 8, 6, 4],
			[3, 4, 5, 7, 5, 4, 3]
		]
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

class alphaBetaAI(connect4Player):

	def play(self, env, move):
		maxDepth =  2
		
		possibleMove = env.topPosition >= 0
		Max = -math.inf
		
		player = np.sum(env.board) % 3 + 1
		us = player

		alpha = -math.inf
		beta = math.inf

		for p, i in enumerate(possibleMove):
			if i:
				if i == 2 or i == 3 or i == 4 or i == 5 or i == 6:
					maxDepth = 3
				else:
					maxDepth = 2
				Value = self.playAMinGame(deepcopy(env), p, 3-player, move, maxDepth, us, alpha, beta)
				if Value > Max:
					Max = Value
					alpha = Max
					move[:] = [p]
	
	def playAMaxGame(self, child, p, player, move, depth, us, alpha, beta):
		lastEnv = child
		self.simulateMove(child, p, 3 - player)
		Value = self.Max(move, depth - 1, child, p, player, us, lastEnv, alpha, beta)
		return Value
	
	def playAMinGame(self, child, p, player, move, depth, us, alpha, beta):
		child.visualize = False
		lastEnv = child
		self.simulateMove(child, p, 3 - player)
		Value = self.Min(move, depth - 1, child, p, player, us, lastEnv, alpha, beta)
		return Value
	
	def simulateMove(self, child, move, player):
		child.board[child.topPosition[move]][move] = player
		child.topPosition[move] -= 1
		child.history[0].append(move)

	def Max(self, move, depth, env, Idx, player, us, lastEnv, alpha, beta):
		if lastEnv.gameOver(Idx, 3 - player):  #env.gameOver(Idx, player) or
			return -depth * 100000
		elif depth == 0:
			return self.Evaluation(deepcopy(env), 3 - player, Idx, us, depth, deepcopy(lastEnv))				###############################
		possibleMove = env.topPosition >= 0

		value = -math.inf

		for p, i in enumerate(possibleMove):
			if i:
				value = max(value, self.playAMinGame(deepcopy(env), p, 3 - player, move, depth, us, alpha, beta))
				alpha = max(value, alpha)

				if value >= beta:
					break
		return value

	def Min(self, move, depth, env, Idx, player, us, lastEnv, alpha, beta):
		if lastEnv.gameOver(Idx, 3 - player):		# env.gameOver(Idx, player) or
			return depth * 100000
		elif depth == 0:
			return self.Evaluation(deepcopy(env), 3 - player, Idx, us, depth, deepcopy(lastEnv))		###############################
		possibleMove = env.topPosition >= 0

		value = math.inf
		
		for p, i in enumerate(possibleMove):
			if i:
				value = min(value, self.playAMaxGame(deepcopy(env), p, 3 - player, move, depth, us, alpha, beta))
				beta = min(value, beta)
				
				if value <= alpha:
					break
		return value

	def Evaluation(self, env, player, Idx, Us, depth, lastEnv):
		if Us == player and lastEnv.gameOver(Idx, player):
			return (depth + 1) * 10000
		elif Us != player and lastEnv.gameOver(Idx, player):
			return -(depth + 1) * 10000
		
		e = self.weight * env.board
		sum = np.sum(e)
		return sum


############################################################################################


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