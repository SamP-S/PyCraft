from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray

from OpenGL.GLU import *

from random import random
from enum import IntEnum
import numpy as np

import maths3d
import noise
import shaders


print("terrain.py")

CONST_WIDTH = 16
CONST_DEPTH = 16
CONST_HEIGHT = 256
CONST_AMPLITUE = 4

cubeVertices = np.array([0.0, 0.0, 0.0,   0.0, 0.0, 1.0,   1.0, 0.0, 1.0,   1.0, 0.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 1.0,   1.0, 1.0, 1.0,   1.0, 1.0, 0.0], dtype='f')
#cubeQuads = ((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 7, 6, 5))
#cubeEdges = ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))

leftFace = np.array([0, 4, 5, 5, 1, 0], dtype='uint32')
rightFace = np.array([2, 6, 7, 7, 3, 2], dtype='uint32')
bottomFace = np.array([0, 1, 2, 2, 3, 0], dtype='uint32')
topFace = np.array([4, 7, 6, 6, 5, 4], dtype='uint32')
backFace = np.array([3, 7, 4, 4, 0, 3], dtype='uint32')
frontFace = np.array([1, 5, 6, 6, 2, 1], dtype='uint32')


blockRGB = [ np.array([0.0, 0.0, 0.0, 0.0], dtype='f'), np.array([0.2, 1.0, 0.2, 1.0], dtype='f'), np.array([0.5, 0.5, 0.5, 1.0], dtype='f') ]


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


# vertex_buffer_object
def createBufferObjects():
    global cubeVBO
    global leftEBO
    global rightEBO
    global bottomEBO
    global topEBO
    global backEBO
    global frontEBO

    cubeVBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)
    glBufferData(GL_ARRAY_BUFFER, cubeVertices, GL_STATIC_DRAW)

    # element_buffer_objects
    leftEBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, leftEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, leftFace, GL_STATIC_DRAW)

    rightEBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, rightEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, rightFace, GL_STATIC_DRAW)

    bottomEBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, bottomEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, bottomFace, GL_STATIC_DRAW)

    topEBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, topEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, topFace, GL_STATIC_DRAW)

    backEBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, backEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, backFace, GL_STATIC_DRAW)

    frontEBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, frontEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, frontFace, GL_STATIC_DRAW)


class block:

    def __init__(self, type=0, pos=maths3d.vec3()):
        self.pos = pos
        self.type = type
        self.faces = []

    def setFaces(self, faces):
        self.faces = faces

    def render(self, shader):
        if len(self.faces) == 0:
            return

        model = maths3d.m4_translate(-self.pos.x, -self.pos.y, -self.pos.z)
        model = maths3d.mat4()
        uni = glGetUniformLocation(shader.id, "modelBlock")
        glUniformMatrix4fv(uni, 1, GL_TRUE, model.m)

        uni = glGetUniformLocation(shader.id, "colour")
        colour = blockRGB[self.type]
        glUniform4f(uni, colour[0], colour[1], colour[2], colour[3])

        #return
        #glDrawElements <- 6 indicies for square

        for face in self.faces:
            if face == FACE.LEFT:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, leftEBO)
            if face == FACE.RIGHT:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, rightEBO)
            if face == FACE.BOTTOM:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, bottomEBO)
            if face == FACE.TOP:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, topEBO)
            if face == FACE.BACK:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, backEBO)
            if face == FACE.FRONT:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, frontEBO)
            #glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, cubeVBO)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, leftEBO)
            
            #glDrawArrays(GL_TRIANGLES, 0, cubeVertices.size)

            #glDrawElements(GL_TRIANGLES, len(leftFace), GL_UNSIGNED_BYTE, None)
            #glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, leftFace)


class chunk:

    def __init__(self, x=0, y=0, z=0):
        self.pos = maths3d.vec3(x, y, z)
        self.blocks = [[[0 for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        self.generate()
        self.generateMesh()


    def render(self, shader):
        glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)
        glVertexPointer(3, GL_FLOAT, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, cubeVertices.size)

        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    self.blocks[k][j][i].render(shader)

    def generate(self):
        perlin = noise.getPerlinIMG(2)
        for k in range(CONST_DEPTH):
            for i in range(CONST_WIDTH):
                offset = perlin[k][i] * CONST_AMPLITUE
                for j in range(CONST_HEIGHT):
                    if j > 63 + offset:
                        self.blocks[k][j][i] = block(BLOCK.AIR, maths3d.vec3(i, j, k))
                    elif j < 20:
                        self.blocks[k][j][i] = block(BLOCK.STONE, maths3d.vec3(i, j, k))
                    else:
                        self.blocks[k][j][i] = block(BLOCK.DIRT, maths3d.vec3(i, j, k))

    def generateMesh(self):
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    # if solid -> check for visible mesh
                    if self.blocks[k][j][i].type != 0:
                        faces = []

                        # left face
                        if i == 0:
                            faces.append(FACE.LEFT)
                        elif self.blocks[k][j][i - 1].type == 0:
                            faces.append(FACE.LEFT)

                        # right face
                        if i == CONST_WIDTH - 1:
                            faces.append(FACE.RIGHT)
                        elif self.blocks[k][j][i + 1].type == 0:
                            faces.append(FACE.RIGHT)

                        # top face
                        if j == 0:
                            faces.append(FACE.TOP)
                        elif self.blocks[k][j - 1][i].type == 0:
                            faces.append(FACE.TOP)

                        # bottom face
                        if j == CONST_HEIGHT - 1:
                            faces.append(FACE.BOTTOM)
                        elif self.blocks[k][j + 1][i].type == 0:
                            faces.append(FACE.BOTTOM)

                        # back face
                        if k == 0:
                            faces.append(FACE.BACK)
                        elif self.blocks[k - 1][j][i].type == 0:
                            faces.append(FACE.BACK)

                        # front face
                        if k == CONST_DEPTH - 1:
                            faces.append(FACE.FRONT)
                        elif self.blocks[k + 1][j][i].type == 0:
                            faces.append(FACE.FRONT)

                        self.blocks[k][j][i].setFaces(faces)


    def print(self):
        for k in range(CONST_DEPTH):
            print ()
            for j in range(CONST_HEIGHT):
                print()
                for i in range(CONST_WIDTH):
                    print(self.blocks[k][j][i])


class terrain:

    MAX_X = 1
    MAX_Y = 1
    MAX_Z = 1

    def __init__(self):
         # make dynamic chunk position
         self.chunks = [[[chunk(0, 0, 0) for i in range(self.MAX_X)] for j in range(self.MAX_Y)] for k in range(self.MAX_Z)]
         createBufferObjects()


    def render(self, shader):
        for k in range(self.MAX_Z):
            for j in range(self.MAX_Y):
                for i in range(self.MAX_X):
                    self.chunks[k][j][i].render(shader)


def main():
    print("terrain.py main")
    c = chunk()
    c.print()

if __name__ == "__main__":
    main()
