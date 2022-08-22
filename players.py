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

def Evaluation(env, player, Idx, Us, depth, lastEnv):
	#todo - implement state
	#print(env.board)
	#print("Here", np.sum(env.board) % 3)
	#print(env.board)
	#print("Eval Player: ", player)
	#if Us and env.gameOver(Idx, player):
	if Us == player and lastEnv.gameOver(Idx, player):
		print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", (depth + 1) * 10000)
		return (depth + 1) * 10000
	#else:
	#elif not Us and env.gameOver(Idx, player):
	elif Us != player and lastEnv.gameOver(Idx, player):
		print("------------------------------------------------------------", -(depth + 1) * 10000)
		return -(depth + 1) * 10000
	#print(depth)
	weight = [
		[3, 4, 5, 7, 5, 4, 3],
		[4, 6, 8, 10, 8, 6, 4],
		[5, 8, 12, 13, 12, 8, 5],
		[5, 8, 12, 13, 12, 8, 5],
		[4, 6, 8, 10, 8, 6, 4],
		[3, 4, 5, 7, 5, 4, 3]
	]
	
	#weight = [
	#	[1, 2, 3, 4, 3, 2, 1],
	#	[2, 3, 4, 5, 4, 3, 2],
	#	[3, 4, 5, 6, 5, 4, 3],
	#	[4, 5, 6, 7, 6, 5, 4],
	#	[4, 6, 8, 10, 8, 6, 4],
	#	[5, 8, 12, 13, 12, 8, 5]
	
	#]
	
	a = env.board
	#print('eval board\n', a)
	for i in a:
		for j in i:
			if j == 2:
				j = -1
	#print(a)
	b = a
	a = a * 2
	a = a * 2 * b

	e = weight * a
	
	Sum = np.sum(e)
	#print("Sum here: ", Sum)		####################################

	
	
	return Sum




class minimaxAI(connect4Player):
	def play(self, env, move):
		maxDepth = 4
		
		possibleMove = env.topPosition >= 0
		Max = -math.inf
		value = 0
		a = -1
		
		player = np.sum(env.board) % 3 + 1
		print("the first player: ", player)
		us = player
		
		for p, i in enumerate(possibleMove):
			if i:
			#print("Minimax P1: ", p)
			
				Value = self.playAMinGame(deepcopy(env), p, 3 - player, move, maxDepth, us)
			
			#self.simulateMove(deepcopy(env), p, self.position)
			#env = a
			
				print("Minimax P2: ", p)
				#max_v = -math.inf
			
			#Value = self.Min(move, maxDepth - 1, env, p)
			#print("There asdjfkljasdlkjfalskdjf;laskdjfl;askjdflasdkjf;lasjdflskjfla;sdj")
			#print("i: ", i)
			#print("Minimax P3: ", p)			# p returns 0 - 6
			#print("Value: ", Value)
			#print("Max: ", Max)
				#print("Min: ", Value)
			# env = currEnv
				if Value > Max:
				#print("Minimax P4: ", p)
					Max = Value
					#print("Value After: ", Max)
				#print("adsfasdfsa", Max)
				#print("Padfasdf: ", p)
					#move[:] = [p]
					a = p

		#print("a: ", a)
		print("Value Final: ", Max)
		move[:] = [a]

	
	def playAMaxGame(self, child, p, player, move, depth, us):
		#player = np.sum(child.board) % 3 + 1
		#if child.gameOver(p, player):
		#	return depth * 10000
		lastEnv = child
		print(" MAX Game self.opponent.position: ", self.opponent.position, player)
		#self.simulateMove(child, p, self.opponent.position)
		self.simulateMove(child, p, 3 - player)
		Value = self.Max(move, depth - 1, child, p, player, us, lastEnv)
		return Value
	
	def playAMinGame(self, child, p, player, move, depth, us):
		#player = np.sum(child.board) % 3 + 1
		#if child.gameOver(p, 3 - player):
		#	return -depth * 10000
		lastEnv = child
		print(" MIN Game self.position: ", self.position, player)
		#self.simulateMove(child, p, self.position)
		self.simulateMove(child, p, 3 - player)
		Value = self.Min(move, depth - 1, child, p, player, us, lastEnv)
		return Value
	
	def simulateMove(self, child, move, player):
		# print("Simulate Player: ", player)
		#print("Simulate move: ", move)
		child.board[child.topPosition[move]][move] = player
		child.topPosition[move] -= 1
		child.history[0].append(move)
		# print(move)
		# print("Simulated: ", env.board)



	# move is a column number 0-6
	def Max(self, move, depth, env, Idx, player, us, lastEnv):
	
		#print("Max here")			######################################################
		print("Max Player: ", player)
		if lastEnv.gameOver(Idx, 3 - player):  #env.gameOver(Idx, player) or
			print("-----------------------------")
			return -depth * 100000
		elif depth == 0:
		
			#print("Idx: ", Idx)
			#print("Eval: ", Evaluation(env, player, move))
			#print(env.board)
			#print("Max Eval")
			return Evaluation(deepcopy(env), 3 -  player, Idx, us, depth, deepcopy(lastEnv))				###############################
		possibleMove = env.topPosition >= 0
		maxVal = -(math.inf)
		
		
		
		for p, i in enumerate(possibleMove):
			if i:
				#print("Max P: ", p)
				#self.simulateMove(env, p, self.opponent.position)
				#print("After: ", env.board)
				
				#print("Max 1:   ", max_v)
				value = max(maxVal, self.playAMinGame(deepcopy(env), p, 3 - player, move, deepcopy(depth), us))
				#max_v = value
				maxVal = value
				#print("Max 2:   ", value)
				# env = curEnv
		return maxVal

	def Min(self, move, depth, env, Idx, player, us, lastEnv):
	
		#print("Min here")			######################################################
		#print("Min Player: ", player)
		if lastEnv.gameOver(Idx, 3 - player):		# env.gameOver(Idx, player) or
			print("++++++++++++++++++++++++++++++++++++++")
			return depth * 100000
		elif depth == 0:
			#print("Min Eval")
			return Evaluation(deepcopy(env), 3- player, Idx, us, depth, deepcopy(lastEnv))		###############################
		possibleMove = env.topPosition >= 0
		minVal = math.inf
		#print(depth)
		for p, i in enumerate(possibleMove):
			if i:
				#print("Min P1: ", p)
				#print("Min Player: ", player)
				#self.simulateMove(env, p, self.position)
				#print("Min P2: ", p)
				
				#print("Min 1: ", min_v)
				value = min(minVal, self.playAMaxGame(deepcopy(env), p, 3 - player, move, deepcopy(depth), us))
				#print("Min 2: ", value)
				minVal = value
				# env = curEnv
		return minVal


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