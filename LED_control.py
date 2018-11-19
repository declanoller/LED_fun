
import time
from neopixel import *
import argparse
from LED_grid import LED_grid
from copy import copy

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

    def __init__(self, Nx=15, Ny=20, zigzag=False):

        self.Nx = Nx
        self.Ny = Ny
        self.LED_count = self.Nx*self.Ny

        self.zigzag = zigzag

        self.grid = LED_grid(Nx=self.Nx, Ny=self.Ny)

        # Create NeoPixel object with appropriate configuration.
        print('creating neopixel object...')
        self.strip = Adafruit_NeoPixel(self.LED_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        print('initializing neopixel object...')
        self.strip.begin()
        print('done.')

        self.color_dict = {0: self.redColor(), 1: self.blueColor(), 2: self.greenColor()}


    def __del__(self):
        pass
        #self.clearAll()



    def matrixToList(self, mat):
        #This takes a numpy array in, and reshapes it to a list that will assume the rows are continuous
        #strips and each row connects to the one below it.
        mat_copy = copy(mat).transpose()

        if self.zigzag:
            print('adjusting for zigzag')
            for i in range(mat_copy.shape[0]):
                if i%2==1:
                    mat_copy[i] = mat_copy[i,::-1]

        reshaped = mat_copy.reshape(1, self.LED_count).squeeze()
        return(reshaped)



    ############## Basic color functions

    def redColor(self):
        return(Color(255, 0, 0))


    def blueColor(self):
        return(Color(0, 255, 0))


    def greenColor(self):
        return(Color(0, 0, 255))


    def whiteColor(self):
        return(Color(127, 127, 127))



    ################# Higher level drawing

    def scrollNumbers(self):
        print('starting number scroll')
        for i in range(10):
            print('\nnumber',i)
            #print('reset grid:')
            self.grid.resetGrid()
            #print('get number pixels:')
            pixel_coords = self.grid.getNumberPixels(i, offset=[0,0])
            #print('set grid pixels:')
            self.grid.setGridPixels(pixel_coords)
            #print('convert mat to list:')
            pixel_list = self.matrixToList(self.grid.getGridMatrix())
            #print('pixel list: ', pixel_list)
            #print('drawing list:')
            self.drawList(pixel_list, i%3)
            time.sleep(1.0)
            self.clearAll()

        print('done!')


    def scrollLetters(self):
        print('starting number scroll')
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(len(alphabet)):
            print('\nletter: ', alphabet[i])
            #print('reset grid:')
            self.grid.resetGrid()
            #print('get number pixels:')
            pixel_coords = self.grid.getLetterPixels(alphabet[i], offset=[0,0])
            #print('set grid pixels:')
            self.grid.setGridPixels(pixel_coords)
            #print('convert mat to list:')
            pixel_list = self.matrixToList(self.grid.getGridMatrix())
            #print('pixel list: ', pixel_list)
            #print('drawing list:')
            self.drawList(pixel_list, i%3)
            time.sleep(1.0)
            self.clearAll()

        print('done!')



    ############## Basic drawing functions

    def clearAll(self):
        self.colorWipe(Color(0,0,0), 10)


    def drawList(self, pixel_list, color=0):
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



















#
