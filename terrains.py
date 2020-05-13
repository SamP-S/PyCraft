from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray

from OpenGL.GLU import *

from random import random
from enum import IntEnum
import numpy as np
import math

import maths3d
import noise
import timer
import shaders


print("terrain.py")

CONST_WIDTH = 16
CONST_DEPTH = 16
CONST_HEIGHT = 256
CONST_AMPLITUE = 4

cubeVertices = np.array([   0.0, 0.0, 0.0,
                            0.0, 0.0, 1.0,
                            1.0, 0.0, 1.0,
                            1.0, 0.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 1.0,
                            1.0, 1.0, 1.0,
                            1.0, 1.0, 0.0], dtype=np.float32)


cubeFaceIndicies = np.array([   [0, 1, 5, 5, 4, 0],     # left
                                [2, 3, 7, 7, 6, 2],     # right
                                [0, 3, 2, 2, 1, 0],     # bottom
                                [4, 5, 6, 6, 7, 4],     # top
                                [3, 0, 4, 4, 7, 3],     # back
                                [1, 2, 6, 6, 5, 1]],    # front
                                dtype=np.uint32)

cubeLineIndicies = np.array([   [0, 1, 1, 5, 5, 4, 4, 0],     # left
                                [2, 3, 3, 7, 7, 6, 6, 2],     # right
                                [0, 3, 3, 2, 2, 1, 1, 0],     # bottom
                                [4, 5, 5, 6, 6, 7, 7, 4],     # top
                                [3, 0, 0, 4, 4, 7, 7, 3],     # back
                                [1, 2, 2, 6, 6, 5, 5, 1]],    # front
                                dtype=np.uint32)

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


class block:

    def __init__(self, type=0, pos=maths3d.vec3()):
        self.pos = pos
        self.type = type
        self.faces = []


class chunk:

    def __init__(self, shader, x=0, y=0, z=0):
        #t = timer.timer()
        self.pos = maths3d.vec3(x, y, z)
        self.blocks = [[[0 for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        self.vertices = np.array([], dtype=np.float32)
        self.lineOffset = 0;
        #print("properties: ", t.getTime())
        self.generate()
        #print("generate: ", t.getTime())
        self.generateMesh()
        #print("mesh: ", t.getTime())

        # generate a vbo per attribute
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)
        #print("gl: ", t.getTime())


    def render(self, shader):
        model = maths3d.m4_translatev(self.pos)
        glUniformMatrix4fv(shader.locations[b"modelChunk"], 1, GL_FALSE, model.m)

        glUniform4f(shader.locations[b"colour"], 1, 1, 1, 1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glDrawArrays(GL_TRIANGLES, 0, self.lineOffset)

        glUniform4f(shader.locations[b"colour"], 0, 0, 0, 1)
        glDrawArrays(GL_LINES, self.lineOffset, self.lineSize)

    def generate(self):
        perlin = noise.getPerlinIMG(2)
        for k in range(CONST_DEPTH):
            for i in range(CONST_WIDTH):
                offset = perlin[k][i] * CONST_AMPLITUE
                for j in range(CONST_HEIGHT):
                    if j > 63 + offset:
                        self.blocks[k][j][i] = block("AIR", maths3d.vec3(i, j, k))
                    elif j < 20:
                        self.blocks[k][j][i] = block("STONE", maths3d.vec3(i, j, k))
                    else:
                        self.blocks[k][j][i] = block("DIRT", maths3d.vec3(i, j, k))

    def generateMesh(self):
        vertices = []
        lines = []
        air = "AIR"
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    # if solid -> check for visible mesh
                    if self.blocks[k][j][i].type != air:
                        #t = timer.timer()
                        faces = []

                        # left face
                        if i == 0:
                            faces.append(FACE.LEFT)
                        elif self.blocks[k][j][i - 1].type == air:
                            faces.append(FACE.LEFT)

                        # right face
                        if i == CONST_WIDTH - 1:
                            faces.append(FACE.RIGHT)
                        elif self.blocks[k][j][i + 1].type == air:
                            faces.append(FACE.RIGHT)

                        # top face
                        if j == 0:
                            faces.append(FACE.BOTTOM)
                        elif self.blocks[k][j - 1][i].type == air:
                            faces.append(FACE.BOTTOM)

                        # bottom face
                        if j == CONST_HEIGHT - 1:
                            faces.append(FACE.TOP)
                        elif self.blocks[k][j + 1][i].type == air:
                            faces.append(FACE.TOP)

                        # back face
                        if k == 0:
                            faces.append(FACE.BACK)
                        elif self.blocks[k - 1][j][i].type == air:
                            faces.append(FACE.BACK)

                        # front face
                        if k == CONST_DEPTH - 1:
                            faces.append(FACE.FRONT)
                        elif self.blocks[k + 1][j][i].type == air:
                            faces.append(FACE.FRONT)

                        self.blocks[k][j][i].faces = faces

                        #print(len(faces), "faces: ", t.getTime())

                        for face in faces:
                            indicies = cubeFaceIndicies[face]
                            for indicie in indicies:
                                vertices.append(cubeVertices[indicie * 3] + i)
                                vertices.append(cubeVertices[indicie * 3 + 1] + j)
                                vertices.append(cubeVertices[indicie * 3 + 2] + k)
                            indicies = cubeLineIndicies[face]
                            for indicie in indicies:
                                lines.append(cubeVertices[indicie * 3] + i)
                                lines.append(cubeVertices[indicie * 3 + 1] + j)
                                lines.append(cubeVertices[indicie * 3 + 2] + k)

                        #print("vertices: ", t.getTime())
        self.lineOffset = round(len(vertices) / 3)
        self.lineSize = round(len(lines) / 3)
        vertices = vertices + lines
        self.vertices = np.array(vertices, dtype=np.float32)


    def print(self):
        for k in range(CONST_DEPTH):
            print ()
            for j in range(CONST_HEIGHT):
                print()
                for i in range(CONST_WIDTH):
                    print(self.blocks[k][j][i])


class terrain:

    MAX_RANGE = 1

    def __init__(self, shader):
         # make dynamic chunk position
         self.chunks = []
         t = timer.timer()
         self.update(shader, maths3d.vec3())

    def update(self, shader, pos):
        # get min/max position x-axis
        max_x = pos.x + self.MAX_RANGE * CONST_WIDTH
        min_x = pos.x - self.MAX_RANGE * CONST_WIDTH
        # get min/max position z-axis
        max_z = pos.z + self.MAX_RANGE * CONST_DEPTH
        min_z = pos.z - self.MAX_RANGE * CONST_DEPTH

        # get min/max chunk x-axis
        max_chunk_x = math.floor(max_x / CONST_WIDTH)
        min_chunk_x = math.floor(min_x / CONST_WIDTH)
        # get min/max chunk z-axis
        max_chunk_z = math.floor(max_z / CONST_DEPTH)
        min_chunk_z = math.floor(min_z / CONST_DEPTH)

        arr = [[False for i in range(min_chunk_x, max_chunk_x + 1)] for k in range(min_chunk_z, max_chunk_z + 1)]

        for i in range(len(self.chunks) -1, -1, -1):
            if self.chunks[i].pos.x < min_x or self.chunks[i].pos.x > max_x:
                del self.chunks[i]
            elif self.chunks[i].pos.z < min_z or self.chunks[i].pos.x > max_z:
                del self.chunks[i]
            else:
                arr[math.floor(self.chunks[i].pos.z / CONST_DEPTH)][math.floor(self.chunks[i].pos.x / CONST_WIDTH)] = True

        for k in range(min_chunk_z, max_chunk_z + 1):
            for i in range(min_chunk_x, max_chunk_x + 1):
                if arr[k][i] != True:
                    self.chunks.append(chunk(shader, i * CONST_WIDTH, 0, k * CONST_DEPTH))

        #self.chunks = [[[chunk(shader, i * CONST_WIDTH, j * CONST_HEIGHT, k * CONST_DEPTH) for i in range(self.MAX_X)] for j in range(self.MAX_Y)] for k in range(self.MAX_Z)]


    def render(self, shader):
        # calls render
        #glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)

        for i in range(len(self.chunks)):
            self.chunks[i].render(shader)

        # moved into chunk render routine
        #print(self.chunks[k][j][i].vbo)
        #glBindBuffer(GL_ARRAY_BUFFER, self.chunks[k][j][i].vbo)
        #glDrawArrays(GL_TRIANGLES, 0, self.chunks[k][j][i].vertices.size)


def main():
    print("terrain.py main")

if __name__ == "__main__":
    main()
