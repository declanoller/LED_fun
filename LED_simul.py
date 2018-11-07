import matplotlib.patches as patches
import matplotlib.pyplot as plt
from pylab import get_cmap
import numpy as np
from random import random
import time


class LED_simul:


	def __init__(self, **kwargs):

		self.Nx = kwargs.get('Nx', None)
		self.Ny = kwargs.get('Ny', None)
		N = kwargs.get('N', None)

		if N is not None:
			self.Nx = self.Ny = N
		else:
			if (self.Nx is None) or (self.Ny is None):
				print('no N values passed; setting default to N = Nx = Ny = 20')
				self.N = self.Nx = 20

		self.grid = np.zeros((self.Nx, self.Ny))

		self.delay = 0.05

		#self.grid[1, 5] = 1

		'''for i in range(self.Nx):
			for j in range(self.Ny):
				if random() > .6:
					self.grid[i,j] = 1'''

		self.createFig()


	def createFig(self):
		fig_size = 8
		self.fig, self.axes = plt.subplots(1,1,figsize=(fig_size*self.Nx/self.Ny, fig_size))
		plt.show(block=False)


	def count(self):

		for i in range(10):
			self.setGridPixels(self.getNumberPixels(i, offset=[5,5]))

			self.plotState()
			time.sleep(1)




	def sun(self):
		pass





	def plotState(self):

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


	def resetGrid(self):
		self.grid = np.zeros((self.Nx, self.Ny))


	def setGridPixels(self, pixel_list):
		#For now I'll have this just reset the grid each time, but in the future
		#I might want it so pixels stay if you don't manually reset them?
		self.resetGrid()
		for pixel in pixel_list:
			self.grid[pixel] = 1


	def getNumberPixels(self, num, offset=[1,1]):

		offset=np.array(offset)

		#A num is going to be 3 wide, and 5 tall.
		#This will just give a list of the x,y coords to set to 1, and it
		#will be up to another function to set the grid to them.

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

		dig_list = dig_dict[num]

		dig_list_offset = [tuple(np.array(dot) + offset) for dot in dig_list]

		return(dig_list_offset)



	def getLetterPixels(self, letter, offset=[1,1]):


		offset=np.array(offset)

		#A num is going to be 3 wide, and 5 tall.
		#This will just give a list of the x,y coords to set to 1, and it
		#will be up to another function to set the grid to them.

		#a, b, ...
		letter0 = [[0,0], [1,0], [2,0], [0,4], [1,4], [2,4], [0,1], [0,2], [0,3], [2,1], [2,2], [2,3]]
		letter1 = [[0,0], [1,0], [2,0], [1,1], [1,2], [1,3], [1,4], [0,3]]

		letter_dict = {0: letter0, 1: letter1, 2: letter2, 3: letter3, 4: letter4, 5: letter5, 6: letter6, 7: letter7, 8: letter8, 9: letter9}

		letter_list = letter_dict[num]

		letter_list_offset = [tuple(np.array(dot) + offset) for dot in letter_list]

		return(letter_list_offset)














#
