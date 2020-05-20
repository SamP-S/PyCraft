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

            BLOCK.AIR    :  {
                        "ID"    :   0,
                        "NAME"  :   "AIR",
                        "RGB"   :   np.array([1.0, 1.0, 1.0, 0.0], dtype='f'),
                        "STATE" :   ELEMENT_STATE.GAS
            },

            BLOCK.DIRT  :   {
                        "ID"    :   1,
                        "NAME"  :   "DIRT",
                        "RGB"   :   np.array([0.2, 1.0, 0.2, 1.0], dtype='f'),
                        "STATE" :   ELEMENT_STATE.SOLID
            },

            BLOCK.STONE  :   {
                        "ID"    :   2,
                        "NAME"  :   "STONE",
                        "RGB"   :   np.array([0.8, 0.8, 0.8, 1.0], dtype='f'),
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
        self.mesh = models.mesh(id, "chunk_mesh", 0, models.RENDER.ELEMENTS_INSTANCED)
        self.generate()
        self.generate_instances()

        # print debug info
        if False:
            print("mesh data id: ", self.mesh.data)
            print("colours: ", self.mesh.instances.colours)
            print("colours size: ", self.mesh.instances.colours.size)
            print("transforms: ", self.mesh.instances.model_projections)
            print("transforms size: ", self.mesh.instances.model_projections.size)


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


    def change_block(self, new_type=BLOCK.AIR, x=-1, y=-1, z=-1):
        # write change log
        self.logs.append(log(vec3(x, y, z), self.blocks[z][y][x], new_type))
        # get old block type at position
        old_type = self.blocks[z][y][x]
        # calculate index / ID
        pos = z * CONST_WIDTH * CONST_HEIGHT + y * CONST_WIDTH + x
        # short hand name
        instances = self.mesh.instances

        if new_type == BLOCK.AIR:
            # get first index of 1D-array of game object id
            index = np.where(instances.game_object_ids == pos)[0][0]

            # position
            instances.game_object_ids = np.delete(instances.game_object_ids, index)

            # colour
            colour_index = index * 4
            colour_list = []
            for i in range(4):
                colour_list.append(colour_index + i)
            instances.colours = np.delete(instances.colours, colour_list)

            # transformation
            model_index = index * 16
            model_list = []
            for i in range(16):
                model_list.append(model_index + i)
            instances.model_projections = np.delete(instances.model_projections, model_list)

            # count
            instances.count -= 1

        elif new_type != BLOCK.AIR and old_type != BLOCK.AIR:
            print("i didn't know this was possible")
            print("so i haven't coded it sowwy :(")
        elif new_type != BLOCK.AIR and old_type == BLOCK.AIR:
            # get instance data
            colour = BLOCK_DIC[new_type].get("RGB")
            proj = transform(vec3(x, y, z)).getModel()
            # append to instance arrays
            instances.game_object_ids = np.append(instances.game_object_ids, pos)
            instances.colours = np.append(instances.colours, colour)
            instances.model_projections = np.append(instances.model_projections, proj)
            instances.count += 1

        self.blocks[z][y][x] = new_type


    # only to be called once upon chunk creation/generation
    def generate_instances(self):
        air = BLOCK.AIR
        count = 0
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    isVisible = False

                    # check block exists
                    if self.blocks[k][j][i] == None:
                        print("NONE")
                        continue

                    # if solid -> check for visible mesh]
                    if self.blocks[k][j][i] != air:

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

                    # if visible add instance to mesh arrays
                    if isVisible == True:
                        count += 1
                        pos = k * CONST_WIDTH * CONST_HEIGHT + j * CONST_WIDTH + i
                        colour = BLOCK_DIC[self.blocks[k][j][i]].get("RGB")
                        transform = copy.deepcopy(self.transform)
                        transform.position.x += i
                        transform.position.y += j
                        transform.position.z += k

                        self.mesh.instances.game_object_ids = np.append(self.mesh.instances.game_object_ids, pos)
                        self.mesh.instances.colours = np.append(self.mesh.instances.colours, colour)
                        self.mesh.instances.model_projections = np.append(self.mesh.instances.model_projections, transform.getModel())

                        if False:
                            print("game object: ", pos)
                            print("colour: ", colour)
                            print("transformation: ", transform.getModel())
                            print("transform shape: ", transform.getModel().shape)
                            print("transform shape: ", self.mesh.instances.model_projections.shape)
                            if count == 1000:
                                quit()
        self.mesh.instances.count = count

BASE_CHUNK = chunk()

def main():
    print("terrain_2.py main")
    t = timer.timer()
    c = chunk("name", None, transform(), NOISE.PERLIN)

if __name__ == "__main__":
    main()



################################################################################
# DEPRECATED

if False:

    # old generation algorithmn used to generate an array of children from 3d block array
    # removed as it required per frame processing on graphics side which was very slow
    # replaced by instance object in mesh and processing data for graphics directly
    # in chunk instead of in graphics so it only has to be done once
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
