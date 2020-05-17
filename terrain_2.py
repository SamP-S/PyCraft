from random import random
from enum import IntEnum
import numpy as np
from math import *
import copy

from maths3d import *
from objects import *
from noise import *
import models
import timer


CONST_WIDTH = 16
CONST_DEPTH = 16
CONST_HEIGHT = 256
CONST_AMPLITUDE = 4


class FACE(IntEnum):
    LEFT = 0
    RIGHT = 1
    BOTTOM = 2
    TOP = 3
    BACK = 4
    FRONT = 5

class ELEMENT_STATE(IntEnum):
    GAS = 0
    SOLID = 1
    LIQUID = 2

class BLOCK(IntEnum):
    AIR = 0
    DIRT = 1
    STONE = 2

# STATIC BLOCK CONSTANTS
BLOCK_DIC =  {

            "AIR"   :   {
                        "ID"    :   0,
                        "RGB"   :   np.array([1.0, 1.0, 1.0, 0.0], dtype='f'),
                        "STATE" :   ELEMENT_STATE.GAS
            },

            "DIRT"  :   {
                        "ID"    :   1,
                        "RGB"   :   np.array([0.2, 1.0, 0.2, 1.0], dtype='f'),
                        "STATE" :   ELEMENT_STATE.SOLID
            },

            "STONE" :   {
                        "ID"    :   2,
                        "RGB"   :   np.array([0.5, 0.5, 0.5, 1.0], dtype='f'),
                        "STATE" :   ELEMENT_STATE.SOLID
            }

}


# basic data structure to contain data about changes of blocks
# these will be stored in file and loaded upon chunk load
class log:

    def __init__(self, pos=vec3(-1, -1, -1), old=None, new=None):
        self.pos = pos
        self.old = old
        self.new = new


# this is a basic game object that will be dynamically generated
# it will be rendered so it must contain a transform component for model transformation projection
# it must also contain a model component
# not sure how it should work but thinking of doing an id system
class block(game_object):

    def __init__(self, id=-1, name="block", parent=None, transform=transform(), type="AIR"):
        super().__init__(id, name + type, parent, transform)
        self.type = type

        # make them dictionary look ups
        self.mesh = 0
        self.material = 0



# chunk is the main game object to be used
# chunk will contain a 3D array storing the block type id
# these can then be used to dynamically generate the visible children
# the children will be made from the block game object
class chunk(game_object):

    def __init__(self, id=-1, name="chunk", parent=None, transform=transform(), noise=NOISE.NONE, seed=0):
        self.logs = []
        if noise != NOISE.NONE:
            print("deepcopy")
            self.blocks = copy.deepcopy(BASE_CHUNK.blocks)
        else:
            self.blocks = [[[None for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        super().__init__(id, name, parent, transform)
        self.noise = noise
        self.seed = seed
        self.generate()
        self.generate_children()


    def generate(self):
        if self.noise == NOISE.NONE:
            for k in range(CONST_DEPTH):
                for j in range(CONST_HEIGHT):
                    for i in range(CONST_WIDTH):
                        if j < 63:
                            self.blocks[k][j][i] = BLOCK.DIRT
                        else:
                            self.blocks[k][j][i] = BLOCK.AIR

        if self.noise == NOISE.PERLIN:
            perlin = getPerlinIMG(2)
            for k in range(CONST_DEPTH):
                for i in range(CONST_WIDTH):
                    offset = perlin[k][i] * CONST_AMPLITUDE
                    for j in range(CONST_AMPLITUDE * 2):
                        if j + 63 - CONST_AMPLITUDE < 63 - CONST_AMPLITUDE + offset:
                            self.blocks[k][j][i] = BLOCK.DIRT
                        else:
                            self.blocks[k][j][i] = BLOCK.AIR

        if self.noise == NOISE.RANDOM:
            for k in range(CONST_DEPTH):
                for i in range(CONST_WIDTH):
                    offset = round(random() * CONST_AMPLITUDE)
                    for j in range(CONST_AMPLITUDE * 2):
                        if j + 63 - CONST_AMPLITUDE < 63 - CONST_AMPLITUDE + offset:
                            self.blocks[k][j][i] = BLOCK.DIRT
                        else:
                            self.blocks[k][j][i] = BLOCK.AIR

    def change_block(self, type="AIR", x=-1, y=-1, z=-1):
        self.logs.append(log(vec3(x, y, z), self.blocks[z][y][x].type, type))
        self.blocks[z][y][x].type = type


    def generate_children(self):
        air = BLOCK.AIR
        count = 0
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):

                    if self.blocks[k][j][i] == None:
                        print("NONE")
                        count += 1
                        continue
                    # if solid -> check for visible mesh]
                    if self.blocks[k][j][i] != air:
                        isVisible = False
                        # left face
                        if i == 0:
                            isVisible = True
                        elif self.blocks[k][j][i - 1] == air:
                            isVisible = True

                        # right face
                        if i == CONST_WIDTH - 1:
                            isVisible = True
                        elif self.blocks[k][j][i + 1] == air:
                            isVisible = True

                        # top face
                        if j == 0:
                            isVisible = True
                        elif self.blocks[k][j - 1][i] == air:
                            isVisible = True

                        # bottom face
                        if j == CONST_HEIGHT - 1:
                            isVisible = True
                        elif self.blocks[k][j + 1][i] == air:
                            isVisible = True

                        # back face
                        if k == 0:
                            isVisible = True
                        elif self.blocks[k - 1][j][i] == air:
                            isVisible = True

                        # front face
                        if k == CONST_DEPTH - 1:
                            isVisible = True
                        elif self.blocks[k + 1][j][i] == air:
                            isVisible = True

                        if isVisible:
                            print("block x", i, "y", j, "z", k)
                            self.children.append(block(len(self.children), "block", self, transform(vec3(i, j, k)), "DIRT"))

BASE_CHUNK = chunk()

def main():
    print("terrain_2.py main")
    t = timer.timer()
    c = chunk("name", None, transform(), NOISE.PERLIN)

if __name__ == "__main__":
    main()
