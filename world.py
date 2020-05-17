import noise
import input
from objects import *
from terrain_2 import *
from cameras import *

# the world is the root node of the "scene"
# must contain additional data about the world:
# seed
# noise type

global mouse
global keyboard
mouse = input.mouse()
keyboard = input.keyboard()

class world:

    def __init__(self):
        print("init world")
        self.children = []

        self.camera = camera()

        #TESTING
        # add chunk
        self.children.append(chunk(0))
