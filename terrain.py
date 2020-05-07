from OpenGL.GL import shaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray

from OpenGL.GLU import *

from random import random
from enum import IntEnum

import numpy as np


print("terrain.py")

CONST_WIDTH = 16
CONST_DEPTH = 16
CONST_HEIGHT = 256

cubeVertices = ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 0.0))
cubeQuads = ((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 7, 6, 5))
cubeEdges = ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))

squareQuads = ((0, 4, 5, 1), (2, 6, 7, 3), (0, 1, 2, 3), (4, 7, 6, 5), (3, 7, 4, 0), (1, 5, 6, 2))

leftSquareQuads = (0, 4, 5, 1)
rightSquareQuads = (2, 6, 7, 3)
bottomSquareQuads = (0, 1, 2, 3)
topSquareQuads = (4, 7, 6, 5)
backSquareQuads = (3, 7, 4, 0)
frontSquareQuads = (1, 5, 6, 2)

xSquareEdges = ((0, 4), (4, 5), (5, 1), (1, 0))
ySquareEdges = ((0, 1), (1, 2), (2, 3), (3, 0))
zSquareEdges = ((3, 7), (7, 4), (4, 0), (0, 3))

blockRGB = { (0.0, 0.0, 0.0, 0.0), (0.2, 1.0, 0.2, 1.0), (0.5, 0.5, 0.5, 1.0) }


class BLOCK(IntEnum):
    AIR = 0
    DIRT = 1
    STONE = 2

class FACE(IntEnum):
    LEFT = 0
    RIGHT = 1
    BOTTOM = 2
    TOP = 3
    BACK = 4
    FRONT = 5


class chunk:

    def __init__(self):
        self.data = [[[0 for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        self.generate()
        self.generateMesh()

        # generate VAO
        self.vao = GLuint(0)
        glGenVertexArrays(1, self.vao)
        glBindVertexArray(self.vao)

        # generate VBO
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.itemsize * len(self.vertices) , self.vertices, GL_STATIC_DRAW)

        # bind attributes
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)


    def generate(self):
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    if j > 63:
                        self.data[k][j][i] = BLOCK.AIR
                    elif j < 20:
                        self.data[k][j][i] = BLOCK.STONE
                    else:
                        self.data[k][j][i] = BLOCK.DIRT


    def addMesh(self, face, x, y, z):
        quadIndicies = squareQuads[face]
        for index in quadIndicies:
            vertex = cubeVertices[index]
            arr = np.array([x + vertex[0], y + vertex[1], z + vertex[2]], dtype='f')
            self.vertices = np.append(self.vertices, arr)


    def generateMesh(self):
        self.vertices = np.array([], dtype='f')
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    # if solid -> check for visible mesh
                    if self.data[k][j][i] != 0:

                        # left face
                        if i == 0:
                            self.addMesh(FACE.LEFT, i, j, k)
                        elif self.data[k][j][i - 1] == 0:
                            self.addMesh(FACE.LEFT, i, j, k)

                        # right face
                        if i == CONST_WIDTH - 1:
                            self.addMesh(FACE.RIGHT, i, j, k)
                        elif self.data[k][j][i + 1] == 0:
                            self.addMesh(FACE.RIGHT, i, j, k)

                        # top face
                        if j == 0:
                            self.addMesh(FACE.BOTTOM, i, j, k)
                        elif self.data[k][j - 1][i] == 0:
                            self.addMesh(FACE.BOTTOM, i, j, k)

                        # bottom face
                        if j == CONST_HEIGHT - 1:
                            self.addMesh(FACE.TOP, i, j, k)
                        elif self.data[k][j + 1][i] == 0:
                            self.addMesh(FACE.TOP, i, j, k)

                        # back face
                        if k == 0:
                            self.addMesh(FACE.BACK, i, j, k)
                        elif self.data[k - 1][j][i] == 0:
                            self.addMesh(FACE.BACK, i, j, k)

                        # front face
                        if k == CONST_DEPTH - 1:
                            self.addMesh(FACE.FRONT, i, j, k)
                        elif self.data[k + 1][j][i] == 0:
                            self.addMesh(FACE.FRONT, i, j, k)


    def print(self):
        for k in range(CONST_DEPTH):
            print ()
            for j in range(CONST_HEIGHT):
                print()
                for i in range(CONST_WIDTH):
                    print(self.data[k][j][i])

    def render(self):
        # assign uniforms
        # bind vertex_array_object
        # bind vbo
        # draw elements

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glDrawArrays(GL_QUADS, 0, self.vertices.size)


def main():
    print("terrain.py main")
    c = chunk()
    c.print()

if __name__ == "__main__":
    main()
