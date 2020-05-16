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


# STATIC BLOCK CONSTANTS
BLOCK =  {

            "AIR"   :   {
                        "ID"    :   0,
                        "RGB"   :   np.array([0.0, 0.0, 0.0, 0.0], dtype='f'),
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




class block(game_object):

    def __init__(self, name="block", parent=None, transform=transform(), type="AIR"):
        super().__init__(name + type, parent, transform)
        self.type = type


class chunk(game_object):

    def __init__(self, name="chunk", parent=None, transform=transform(), noise=NOISE.NONE, seed=0):
        if noise != NOISE.NONE:
            print("deepcopy")
            self.blocks = copy.deepcopy(BASE_CHUNK.blocks)
        else:
            self.blocks = [[[None for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        super().__init__(name, parent, transform)
        self.noise = noise
        self.seed = seed
        self.generate()
        self.generateMesh()


    def generate(self):
        if self.noise == NOISE.NONE:
            for k in range(CONST_DEPTH):
                for j in range(CONST_HEIGHT):
                    for i in range(CONST_WIDTH):
                        if j < 63:
                            self.blocks[k][j][i] = block("BLOCK_DIRT", self, transform(vec3(i, j, k)), "DIRT")
                        else:
                            self.blocks[k][j][i] = block("BLOCK_AIR", self, transform(vec3(i, j, k)), "AIR")

        if self.noise == NOISE.PERLIN:
            perlin = getPerlinIMG(2)
            for k in range(CONST_DEPTH):
                for i in range(CONST_WIDTH):
                    offset = perlin[k][i] * CONST_AMPLITUDE
                    for j in range(CONST_AMPLITUDE * 2):
                        if j + 63 - CONST_AMPLITUDE < 63 - CONST_AMPLITUDE + offset:
                            self.blocks[k][j][i] = block("BLOCK_DIRT", self, transform(vec3(i, j, k)), "DIRT")
                        else:
                            self.blocks[k][j][i] = block("BLOCK_AIR", self, transform(vec3(i, j, k)), "AIR")

        if self.noise == NOISE.RANDOM:
            for k in range(CONST_DEPTH):
                for i in range(CONST_WIDTH):
                    offset = round(random() * CONST_AMPLITUDE)
                    for j in range(CONST_AMPLITUDE * 2):
                        if j + 63 - CONST_AMPLITUDE < 63 - CONST_AMPLITUDE + offset:
                            self.blocks[k][j][i] = block("BLOCK_DIRT", self, transform(vec3(i, j, k)), "DIRT")
                        else:
                            self.blocks[k][j][i] = block("BLOCK_AIR", self, transform(vec3(i, j, k)), "AIR")


    def generateMesh(self):
        air = "AIR"
        count = 0
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):

                    if self.blocks[k][j][i] == None:
                        print("NONE")
                        count += 1
                        continue
                    # if solid -> check for visible mesh]
                    if self.blocks[k][j][i].type != air:
                        isVisible = False
                        # left face
                        if i == 0:
                            isVisible = True
                        elif self.blocks[k][j][i - 1].type == air:
                            isVisible = True

                        # right face
                        if i == CONST_WIDTH - 1:
                            isVisible = True
                        elif self.blocks[k][j][i + 1].type == air:
                            isVisible = True

                        # top face
                        if j == 0:
                            isVisible = True
                        elif self.blocks[k][j - 1][i].type == air:
                            isVisible = True

                        # bottom face
                        if j == CONST_HEIGHT - 1:
                            isVisible = True
                        elif self.blocks[k][j + 1][i].type == air:
                            isVisible = True

                        # back face
                        if k == 0:
                            isVisible = True
                        elif self.blocks[k - 1][j][i].type == air:
                            isVisible = True

                        # front face
                        if k == CONST_DEPTH - 1:
                            isVisible = True
                        elif self.blocks[k + 1][j][i].type == air:
                            isVisible = True

                        if isVisible:
                            self.children.append(self.blocks[k][j][i])

BASE_CHUNK = chunk()

def main():
    print("terrain_2.py main")
    t = timer.timer()
    c = chunk("name", None, transform(), NOISE.PERLIN)
    print(len(c.children))
    print(t.getTime())

if __name__ == "__main__":
    main()
