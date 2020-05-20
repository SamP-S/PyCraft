import noise
import input
from objects import *
from terrain_2 import *
from cameras import *

# the world is the root node of the "scene"
# must contain additional data about the world:
# seed
# noise type

class world:

    def __init__(self):
        print("init world")
        self.children = []

        self.camera = camera()
