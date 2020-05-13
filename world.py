import noise
import input
from objects import *
from terrain import *

# the world is the root node of the "scene"
# must contain additional data about the world:
# seed
# noise type

global mouse
global keyboard
mouse = input.mouse()
keyboard = keyboard.mouse()

class world:

    def __init__(self, seed=2, noise=noise.NOISE.PERLIN):
        print("init world")
        self.children = []

        # add terrain
        self.children.append(terrain(seed, noise))
        self.children.append()
