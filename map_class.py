#!/usr/local/bin/pythonw
import pygame, random, sys
from cell_class import *

#// CREATE SCREEN OBJECT //#

class Screen():
	def __init__(self, width = 650, height = 550):
		self.screen = pygame.display.set_mode((width,height))
		self.width = width
		self.height = height
		self.cellHeight = self.height - (self.height / 4)

	def fill(self, color = (0,0,0)):
		self.screen.fill(color)

screen = Screen(650, 600)

#// CREATE MAP OBJECT //#

class Map(object):
	def __init__(self, cells):
		self.width = screen.width
		self.height = screen.cellHeight
		self.generation = 0
		self.livingCells = 0
		self.cells = cells
	def updateCells(self):
		lastGrid = [[0 for x in xrange(screen.cellHeight/Cell.SIZE + 1)] for x in xrange(screen.width/Cell.SIZE + 1)]

		for y in xrange(screen.cellHeight/Cell.SIZE + 1):
			for x in xrange(screen.width/Cell.SIZE + 1):
				lastGrid[x][y] = Cell(self.cells[x][y].state, x * Cell.SIZE, y * Cell.SIZE)

		for y in xrange(screen.cellHeight/Cell.SIZE + 1):
			for x in xrange(screen.width/Cell.SIZE + 1):
				self.cells[x][y].updateState(lastGrid)

		self.generation += 1


	def drawCells(self, display):

		self.livingCells = 0
		for y in xrange(screen.cellHeight/Cell.SIZE + 1):
			for x in xrange(screen.width/Cell.SIZE + 1):
				if(self.cells[x][y].state == Cell.ON):
					self.cells[x][y].draw(display)
					self.livingCells += 1



	def drawGrid(self, display):
		for y in xrange(screen.cellHeight  / Cell.SIZE + 2):
			pygame.draw.line(display, Color.GRAY, (0, y * Cell.SIZE), (screen.width, y * Cell.SIZE))

		for x in xrange(screen.width / Cell.SIZE + 1):
			pygame.draw.line(display, Color.GRAY, (x * Cell.SIZE, 0), (x * Cell.SIZE, screen.cellHeight + Cell.SIZE))
