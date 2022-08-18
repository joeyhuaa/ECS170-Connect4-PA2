import random
import time
import pygame
import math

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



def iterativeDeepening(env, move):
		maxDepth = 6
		while (True):
			move[:] = [miniMax(env, maxDepth)]
			limit += 1

def simulateMove(env, move, player):
		connect4.board[connect4.topPosition[move]][move] = player
		connect4.topPosition[move] -= 1
		env.history[0].append(move)

def Max(state, depth):
	if connect4.gameOver(state) or depth == 0:
		return Evaluation(state)
	possibleMove = env.topPosition >= 0
	max_v = -(math.inf)
	for i in possibleMove:
		child = simulateMove(deepcopy(env), i, self.opponent.position)
		Maxi = max(max_v, Min(child, depth - 1))
	return max_v

def Min(state):
	if env.gameOver(state) or depth == 0:
		return Evaluation(state)
	possibleMove = env.topPosition >= 0
	min_v = math.inf
	for i in possibleMove:
		child = simulateMove(deepcopy(env), i, self.opponent.position)
		Mini = max(min_v, Min(child, depth - 1))
	return min_v

# def byWeight(self, state):

def Evaluation(state):
	weight = [
		[3, 4, 5, 7, 5, 4, 3],
		[4, 6, 8, 10, 8, 6, 4],
		[5, 8, 12, 13, 12, 8, 5],
		[5, 8, 12, 13, 12, 8, 5],
		[4, 6, 8, 10, 8, 6, 4],
		[3, 4, 5, 7, 5, 4, 3]
	]
	a = self.board
	a = a * 2 - 3
	a = (-1) * a
	e = weight * a
	Sum = np.sum(e)
	return Sum

def miniMax(env, maxDepth):
	possible = env.topPosition >= 0
	Max = -math.inf
	for i in possible:
		child = self.simulateMove(deepcopy(envrionment), i, self.opponent.position)
		Value = self.Min(child, env, maxDepth - 1)
		if Value > Max:
			Max = Value
			move[:] = [Move]

class minimaxAI(connect4Player):		#############################################################################################################################


	def play(self, env, move):

		move[:] = [4]

		iterativeDeepening(env, move)


	#	pass






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




