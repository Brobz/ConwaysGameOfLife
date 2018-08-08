#!/usr/local/bin/pythonw
import pygame, random, sys

#// CREATE -/- INIT COLOR OBJECT //#

class Color():
	BLACK = (0,0,0)
	WHITE = (255,255,255)
	GRAY = (150,150,150)
	RED = (255,0,0)
	GREEN = (0,255,0)
	BLUE = (0,0,255)

#// CREATE CELL OBJECT //# 

class Cell():

	"""
	-> Any live cell with fewer than two live neighbours dies, as if caused by under-population.
	
	-> Any live cell with two or three live neighbours lives on to the next generation.
	
	-> Any live cell with more than three live neighbours dies, as if by overcrowding.
	
	-> Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

	"""

	OFF = 0
	ON = 1
	SIZE = 7

	def __init__(self, state, x = 50, y = 50):
		self.state = state
		self.color = Color.BLACK
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, self.SIZE, self.SIZE)
		self.neighbours = None

	def draw(self, display):
		pygame.draw.rect(display, self.color, self.rect)  

	def getNeighbours(self, grid):
		cells = []

		x = self.x / self.SIZE
		y = self.y / self.SIZE

		x1 = x + 1
		x_1 = x - 1

		y1 = y + 1
		y_1 = y - 1
			

		if x1 > len(grid) - 1:
			x1 = 0							

		if y1 > len(grid[0]) - 1:
			y1 = 0

		if x_1 < 0:
			x_1 = len(grid) - 1

		if y_1 < 0:
			y_1 = len(grid[0]) - 1


		cells.append(grid[x1][y])

		cells.append(grid[x_1][y])

		cells.append(grid[x][y1])

		cells.append(grid[x][y_1])


		cells.append(grid[x1][y1])

		cells.append(grid[x1][y_1])
	
		cells.append(grid[x_1][y1])

		cells.append(grid[x_1][y_1])


		return cells

	def updateState(self, grid):
		onNeighbours = []
		offNeighbours = []

		self.neighbours = self.getNeighbours(grid)

		for n in self.neighbours:	
			if n.state == self.ON:
				onNeighbours.append(n)
			else:
				offNeighbours.append(n)

		if self.state == self.OFF:
			if len(onNeighbours) == 3:
				self.state = self.ON
		else:
			if len(onNeighbours) < 2 or len(onNeighbours) > 3:
				self.state = self.OFF
