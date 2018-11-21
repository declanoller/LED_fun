import numpy as np
import time
import argparse
from copy import copy
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from pylab import get_cmap

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class LED_control:

	def __init__(self, Nx=15, Ny=20, **kwargs):

		# This is now configured so you can run it either as a "simulation",
		# which will plot it in matplotlib so you can see what it will do without
		# connecting it to the LED strip, or with the run_type argument "real",
		# which will run it with the LEDs.

		# A couple practical notes:
		# --The LED strip is addressed via a single index, so you have to call
		# 	gridToList to get the list of which indices of it to turn on.
		#
		# --I tried to make it so you can call functions like drawGrid() in either
		# 	run_type, and it will fork there and figure out what to do, so you shouldn't
		# 	have to figure out that lower level stuff and can just work with the grid.
		#
		# --If you hook up the LED strip in a "zig zag" way, you have to pass it that parameter
		# 	so it reshapes self.grid correctly (see gridToList()).
		#
		# --Right now, self.grid has the INFO for which pixels are turned on, but the actual
		# 	display (i.e., the plot or real pixels) are separate from that, meaning that you can
		# 	clear them without resetting self.grid. This might be useful if you want to animate.


		self.Nx = Nx
		self.Ny = Ny
		self.LED_count = self.Nx*self.Ny

		self.grid = np.zeros((self.Nx, self.Ny))

		self.run_type = kwargs.get('run_type', 'simulation')

		self.delay = 0.05

		if self.run_type == 'simulation':
			self.createFig()

		if self.run_type == 'real':
			self.zigzag = kwargs.get('zigzag', False)
			#from neopixel import *
			# Create NeoPixel object with appropriate configuration.
			print('creating neopixel object...')
			self.strip = Adafruit_NeoPixel(self.LED_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
			# Intialize the library (must be called once before other functions).
			self.color_dict = {0: self.redColor(), 1: self.blueColor(), 2: self.greenColor()}
			print('initializing neopixel object...')
			self.strip.begin()
			print('done.')




	def __del__(self):
		if self.run_type == 'real':
			self.clearPixelDisplay()



	############## Basic color functions

	def redColor(self):
		return(Color(255, 0, 0))


	def blueColor(self):
		return(Color(0, 255, 0))


	def greenColor(self):
		return(Color(0, 0, 255))


	def whiteColor(self):
		return(Color(127, 127, 127))


	################# Higher level drawing stuff that's used for both simulation and real stuff.

	def horizontalScroll(self, in_str):

		grid_list = self.stringToGridList(in_str)
		big_grid = np.concatenate(grid_list)
		big_grid_width = big_grid.shape[0]
		big_grid_height = big_grid.shape[1]

		# Do a thing where you have a "pointer" to the big_grid, and mod it by its length.

		scroll_origin = [0,5]

		bg_pos = 0
		while True:
			self.resetGrid()

			for x in range(scroll_origin[0], self.Nx):
				for y in range(big_grid_height):

					bg_x_ind = (x + bg_pos) % big_grid_width
					if big_grid[bg_x_ind, y]:
						self.grid[x, scroll_origin[1] + y] = 1

			# Draw the grid
			self.drawGrid()
			time.sleep(.01)
			# Clear the display (not the grid!)
			#self.clearAll()
			bg_pos += 1


	def stringToGridList(self, in_str):

		# This takes a string (letters or numbers), splits them up into a list,
		# and then takes each one and converts it to its grid. Then it combines them
		# all into one mega-grid that's probably bigger than the display (but that part
		# will be handled by another function.)

		in_str += '  '

		blank_grid = np.zeros((3,5))
		space_width = 2
		space_grid = np.zeros((space_width, 5))
		between_letter_space_width = 1
		between_letter_grid = np.zeros((between_letter_space_width, 5))

		grids = []

		for i,char in enumerate(in_str):

			if char == ' ':
				grids.append(space_grid)
			else:
				px_list = self.getLetterPixels(char)
				char_grid = copy(blank_grid)
				for px in px_list:
					char_grid[px] = 1

				grids.append(char_grid)
				grids.append(between_letter_grid)

		return(grids)



	def loopNumbers(self):
		print('starting number scroll')
		for i in range(10):
			print('\nnumber',i)

			self.resetGrid()

			# Gets a list of the coordinates to "turn on"
			pixel_coords = self.getNumberPixels(i, offset=[0,0])
			# Sets these coords to 1 in self.grid
			self.setGridPixels(pixel_coords)

			# Draw the grid
			self.drawGrid(i%3)
			time.sleep(1.0)
			# Clear the display (not the grid!)
			self.clearAll()

		print('done!')


	def loopLetters(self):
		print('starting number scroll')
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		for i in range(len(alphabet)):
			print('\nletter: ', alphabet[i])

			self.resetGrid()

			# Gets a list of the coordinates to "turn on"
			pixel_coords = self.getLetterPixels(alphabet[i], offset=[0,0])
			# Sets these coords to 1 in self.grid
			self.setGridPixels(pixel_coords)

			# Draw the grid
			self.drawGrid(i%3)
			time.sleep(1.0)
			# Clear the display (not the grid!)
			self.clearAll()

		print('done!')


	def sun(self):
		pass


	def drawGrid(self, color=0):
		if self.run_type == 'simulation':
			self.plotPixelGrid()
		if self.run_type == 'real':
			self.displayPixelGrid(pixel_list, color)


	def clearAll(self):
		# This clears the simulation plot or real display. Note that it DOESN'T
		# clear self.grid.
		if self.run_type == 'simulation':
			self.clearPixelGrid()
		if self.run_type == 'real':
			self.clearPixelDisplay()


	############## Basic real pixel drawing functions

	def clearPixelDisplay(self):
		self.colorWipe(Color(0,0,0), 10)


	def displayPixelGrid(self):
		pixel_list = self.gridToList(self.grid)
		self.displayPixelList(pixel_list, color=0)


	def displayPixelList(self, pixel_list, color=0):
		for i, pixel_val in enumerate(pixel_list):
			if pixel_val==1:
				#print('setting pixel {} with value {}'.format(i, pixel_val))
				self.strip.setPixelColor(i, self.color_dict[color])
		self.strip.show()


	def colorWipe(self, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		for i in range(self.LED_count):
			self.strip.setPixelColor(i, color)

		time.sleep(wait_ms/1000.0)
		self.strip.show()



	#################### Plotting simulation stuff

	def createFig(self):
		fig_size = 8
		self.fig, self.axes = plt.subplots(1,1,figsize=(fig_size*self.Nx/self.Ny, fig_size))
		plt.show(block=False)


	def clearPixelGrid(self):

		# This clears the pixel grid, basically just drawing white on every pixel.

		width = 1.0
		height = 1.0*self.Ny/self.Nx

		block_width = width/self.Nx
		margin = block_width/2.5

		#cm = get_cmap('Paired')
		cm = get_cmap('inferno')

		box_margin = 0.008
		self.axes.clear()
		#self.axes.add_patch(patches.Rectangle((-box_margin*width,-box_margin*width),(1+2*box_margin)*width,(1+2*box_margin)*height,linewidth=4,edgecolor='black',facecolor='white'))

		self.axes.add_patch(patches.Rectangle((0,0),width,height,linewidth=4,edgecolor='black',facecolor='white'))

		self.axes.set_xlim(-box_margin*width,(1+box_margin)*width)
		self.axes.set_ylim(-box_margin*height,(1+box_margin)*height)
		self.axes.set_aspect('equal')
		self.axes.axis('off')

		for i in range(self.Nx):
			for j in range(self.Ny):

				(x0,y0) = (i*block_width+margin,j*block_width+margin)
				rect_width = block_width - 2*margin

				rect = patches.Rectangle((x0,y0), rect_width, rect_width,  facecolor='white')
				self.axes.add_patch(rect)


		#plt.tight_layout()
		self.fig.canvas.draw()


	def plotPixelGrid(self, color=0):

		# This plots self.grid on the simulation plot.

		width = 1.0
		height = 1.0*self.Ny/self.Nx

		block_width = width/self.Nx
		margin = block_width/2.5

		#cm = get_cmap('Paired')
		cm = get_cmap('inferno')

		box_margin = 0.008
		self.axes.clear()
		#self.axes.add_patch(patches.Rectangle((-box_margin*width,-box_margin*width),(1+2*box_margin)*width,(1+2*box_margin)*height,linewidth=4,edgecolor='black',facecolor='white'))

		self.axes.add_patch(patches.Rectangle((0,0),width,height,linewidth=4,edgecolor='black',facecolor='white'))

		self.axes.set_xlim(-box_margin*width,(1+box_margin)*width)
		self.axes.set_ylim(-box_margin*height,(1+box_margin)*height)
		self.axes.set_aspect('equal')
		self.axes.axis('off')

		for i in range(self.Nx):
			for j in range(self.Ny):

				(x0,y0) = (i*block_width+margin,j*block_width+margin)
				rect_width = block_width - 2*margin

				if self.grid[i,j]==1:
					color = 'black'
				else:
					color = 'white'
				#color = cm(1.*self.grid[i,j].type/self.N_types)
				#rect = patches.Rectangle((x0,y0),rect_width,rect_width,linewidth=2,edgecolor=color,facecolor=color)
				rect = patches.Rectangle((x0,y0), rect_width, rect_width,  facecolor=color)
				self.axes.add_patch(rect)


		#plt.tight_layout()
		self.fig.canvas.draw()



	#################### Grid/list stuff.

	def resetGrid(self):
		self.grid = np.zeros((self.Nx, self.Ny))


	def setGridPixels(self, pixel_indices_list):
		for pixel in pixel_indices_list:
			self.grid[pixel] = 1


	def gridToList(self, mat):
		# This takes a numpy array in, and reshapes it to a list that will assume the rows are continuous
		# strips and each row connects to the one below it.
		mat_copy = copy(mat).transpose()

		if self.zigzag:
			print('adjusting for zigzag')
			for i in range(mat_copy.shape[0]):
				if i%2==1:
					mat_copy[i] = mat_copy[i,::-1]

		reshaped = mat_copy.reshape(1, self.LED_count).squeeze()
		return(reshaped)


	def getNumberPixels(self, num, offset=[0,0]):

		offset=np.array(offset)

		#A num is going to be 3 wide, and 5 tall.
		#This will just give a list of the x,y coords to set to 1, and it
		#will be up to another function to set the grid to them.
		dig_list = dig_dict[num]

		dig_list_offset = [tuple(np.array(dot) + offset) for dot in dig_list]

		return(dig_list_offset)


	def getLetterPixels(self, letter, offset=[0,0]):

		offset=np.array(offset)

		#A num is going to be 3 wide, and 5 tall.
		#This will just give a list of the x,y coords to set to 1, and it
		#will be up to another function to set the grid to them.
		letter_list = letter_dict[letter]

		letter_list_offset = [tuple(np.array(dot) + offset) for dot in letter_list]

		return(letter_list_offset)







dig0 = [[0,0], [1,0], [2,0], [0,4], [1,4], [2,4], [0,1], [0,2], [0,3], [2,1], [2,2], [2,3]]
dig1 = [[0,0], [1,0], [2,0], [1,1], [1,2], [1,3], [1,4], [0,3]]
dig2 = [[0,3], [1,4], [2,3], [1,2], [0,1], [0,0], [1,0], [2,0]]
dig3 = [[0,4], [1,4], [2,3], [1,2], [2,1], [1,0], [0,0]]
dig4 = [[2,0], [2,1], [2,2], [2,3], [2,4], [0,2], [0,3], [0,4], [1,2]]
dig5 = [[0,4], [1,4], [2,4], [0,3], [0,2], [1,2], [2,1], [0,0], [1,0]]
dig6 = [[0,1], [0,2], [0,3], [1,4], [2,4], [1,2], [2,1], [1,0]]
dig7 = [[2,0], [2,1], [2,2], [2,3], [2,4], [0,4], [1,4], [0,4]]
dig8 = [[0,0], [1,0], [2,0], [0,4], [1,4], [2,4], [0,1], [0,2], [0,3], [2,1], [2,2], [2,3], [1,2]]
dig9 = [[0,0], [1,0], [0,4], [1,4], [2,4], [0,2], [0,3], [2,1], [2,2], [2,3], [1,2]]


dig_dict = {0: dig0, 1: dig1, 2: dig2, 3: dig3, 4: dig4, 5: dig5, 6: dig6, 7: dig7, 8: dig8, 9: dig9}


#a, b, ...
letter0 = [[2,0], [2,3], [2,4], [1,0], [1,2], [1,4], [0,0], [0,1], [0,4]]
letter1 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,0], [1,2], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter2 = [[2,0], [2,4], [1,0], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter3 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,0], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter4 = [[2,0], [2,4], [1,0], [1,2], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter5 = [[2,4], [1,2], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter6 = [[2,0], [2,1], [2,2], [2,4], [1,1], [1,4], [0,1], [0,2], [0,3], [0,4]]
letter7 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,2], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter8 = [[2,0], [2,4], [1,0], [1,1], [1,2], [1,3], [1,4], [0,0], [0,4]]
letter9 = [[2,4], [1,0], [1,1], [1,2], [1,3], [1,4], [0,0], [0,4]]
letter10 = [[2,0], [2,1], [2,3], [2,4], [1,2], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter11 = [[2,0], [1,0], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter12 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,3], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter13 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter14 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,0], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter15 = [[2,2], [2,3], [2,4], [1,2], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter16 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,1], [1,4], [0,1], [0,2], [0,3], [0,4]]
letter17 = [[2,0], [2,2], [2,3], [2,4], [1,1], [1,2], [1,4], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter18 = [[2,0], [2,1], [2,2], [2,4], [1,0], [1,2], [1,4], [0,0], [0,2], [0,3], [0,4]]
letter19 = [[2,4], [1,0], [1,1], [1,2], [1,3], [1,4], [0,4]]
letter20 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,0], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter21 = [[2,1], [2,2], [2,3], [2,4], [1,0], [0,1], [0,2], [0,3], [0,4]]
letter22 = [[2,0], [2,1], [2,2], [2,3], [2,4], [1,1], [0,0], [0,1], [0,2], [0,3], [0,4]]
letter23 = [[2,0], [2,1], [2,3], [2,4], [1,2], [0,0], [0,1], [0,3], [0,4]]
letter24 = [[2,3], [2,4], [1,0], [1,1], [1,2], [0,3], [0,4]]
letter25 = [[2,0], [2,3], [2,4], [1,0], [1,2], [1,4], [0,0], [0,1], [0,4]]

letter_dict = {'a': letter0,
				'b': letter1,
				'c': letter2,
				'd': letter3,
				'e': letter4,
				'f': letter5,
				'g': letter6,
				'h': letter7,
				'i': letter8,
				'j': letter9,
				'k': letter10,
				'l': letter11,
				'm': letter12,
				'n': letter13,
				'o': letter14,
				'p': letter15,
				'q': letter16,
				'r': letter17,
				's': letter18,
				't': letter19,
				'u': letter20,
				'v': letter21,
				'w': letter22,
				'x': letter23,
				'y': letter24,
				'z': letter25,
				}


#
