#!/usr/local/bin/pythonw
from cell_class import *
from map_class import *

#// INIT SCREEN OBJECT //#

pygame.init()
pygame.display.set_caption("Conway's Game Of Life")
pygame.mouse.set_visible(False)

#// CREATE -/- INIT GUI OBJECT //#

class  GUI():
	def __init__(self, position, color):
		self.position = position
		self.color = color

	def showGUI(self, text):
		myfont = pygame.font.SysFont("arial", 15)

		label = myfont.render(text, 1, self.color)
		screen.screen.blit(label, self.position)

GPS_GUI = GUI((25,480), Color.BLACK)
click_GUI = GUI((325, 480), Color.BLACK)
n_GUI = GUI((325, 500), Color.BLACK)
c_GUI = GUI((325, 520), Color.BLACK)
space_GUI = GUI((325, 540), Color.BLACK)
arrows_GUI = GUI((325, 560), Color.BLACK)
FPS_GUI = GUI((580, 575), Color.BLACK)
GENERATIONS_GUI = GUI((25, 510), Color.BLACK)
LIVE_CELLS_GUI = GUI((25, 550), Color.BLACK)

#// HELPER FUNCTIONS //#
isPressingLeft = False
isPressingRight = False
clearing = True
def checkForInput(mx,my, grid, display):
	global simulationHasStarted
	global simulation_delay
	global isPressingLeft
	global isPressingRight
	global looping
	global clearing
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		mouseRect = pygame.Rect(mx, my, 1.5, 1.5)
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				isPressingLeft = True
			if event.button == 3:
				isPressingRight = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				isPressingLeft = False
			if event.button == 3:
				isPressingRight = False
		for l in grid:
			for c in l:
				if mouseRect.colliderect(c.rect) and not simulationHasStarted:
					if c.state == Cell.OFF:
						c.color = Color.GRAY
						c.state = Cell.ON
					elif c.color == Color.BLACK:
						c.color = Color.RED
					if isPressingLeft:
						if c.color == Color.GRAY:
							c.color = Color.BLACK
					if isPressingRight:
						c.state = Cell.OFF
				else:
					if c.color == Color.GRAY:
						c.color = Color.BLACK
						c.state = Cell.OFF
					if c.color == Color.RED:
						c.color = Color.BLACK
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_n:
				looping = False
				clearing = False
			if event.key == pygame.K_c:
				looping = False
				clearing = True
			if event.key == pygame.K_SPACE:
				simulationHasStarted = not simulationHasStarted
			if event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
				if simulation_delay > 1:
					simulation_delay -= 1
					while 20 / float(simulation_delay) % 1:
						simulation_delay -= 1
			if event.key == pygame.K_DOWN or event.key == pygame.K_LEFT:
				if simulation_delay < 20:
					simulation_delay += 1
					while 20 / float(simulation_delay) % 1:
						simulation_delay += 1


#// GAME LOOP //#

def game(clear = True):

	global simulationHasStarted
	global looping
	global simulation_delay
	global time_remaning

	looping = True
	clock = pygame.time.Clock()

	cells = [[0 for x in xrange(screen.cellHeight/Cell.SIZE + 1)] for x in xrange(screen.width/Cell.SIZE + 1)]



	#// FILLS SCREEN WITH RANDOM CELLS //#

	for x in xrange(screen.width/Cell.SIZE + 1):
		for y in xrange(screen.cellHeight/Cell.SIZE + 1):
			if(random.randrange(101)) > 70:
				cells[x][y] = Cell(Cell.ON, x * Cell.SIZE, y * Cell.SIZE)
			else:
				cells[x][y] = Cell(Cell.OFF, x * Cell.SIZE, y * Cell.SIZE)



	#// FILLS SCREEN WITH DEAD CELLS //#


	if clear:
		for y in xrange(screen.cellHeight/Cell.SIZE + 1):
			for x in xrange(screen.width/Cell.SIZE + 1):
				cells[x][y] = Cell(Cell.OFF, x * Cell.SIZE, y * Cell.SIZE)

	#// GET CELLS NEIGHBOURS //#

	for y in xrange(screen.cellHeight/Cell.SIZE + 1):
		for x in xrange(screen.width/Cell.SIZE + 1):
			cells[x][y].neighbours = cells[x][y].getNeighbours(cells)

	_map = Map(cells)

	simulationHasStarted = False



	while looping:

		#// CLEAR SCREEN //#

		screen.fill(Color.WHITE)

		#// GET USER INPUT //#

		mx,my = pygame.mouse.get_pos()

		checkForInput(mx, my, _map.cells, screen.screen)

		#// UPDATE GAME STATE	//#

		if simulationHasStarted:
			if time_remaning <= 0:
				_map.updateCells()
				time_remaning = simulation_delay

		time_remaning -= 1



		#// DRAW TO SCREEN //#

		_map.drawCells(screen.screen)

		_map.drawGrid(screen.screen)

		if simulationHasStarted:
			#FPS_GUI.showGUI("FPS: " + str(clock.tick(simulation_delay)))
			clock.tick(20)


			GENERATIONS_GUI.showGUI("GENERATION: " + str(_map.generation))
			LIVE_CELLS_GUI.showGUI("LIVE CELLS: " + str(_map.livingCells))


		GPS_GUI.showGUI("MAX GENERATIONS PER SECOND: " + str(20 / simulation_delay))
		click_GUI.showGUI("LEFT CLICK TO PLACE CELL; RIGHT CLICK TO REMOVE CELL")
		n_GUI.showGUI("PRESS 'N' FOR A NEW, RANDOM BOARD")
		c_GUI.showGUI("PRESS 'C' TO CLEAR BOARD")
		space_GUI.showGUI("PRESS 'SPACE' TO START/PAUSE/RESUME")
		arrows_GUI.showGUI("USE ARROW KEYS TO CHANGE SPEED")

		#// UPDATE DISPLAY //#

		pygame.display.update()



if __name__ == "__main__":
	global simulation_delay
	global time_remaning
	simulation_delay = 5
	time_remaning = simulation_delay
	while 1:
		game(clearing) #Pass false for random starting cells
