from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray

from OpenGL.GLU import *

from random import random
from enum import IntEnum
import numpy as np

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

cubeIndices = np.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=np.uint32)

cubeFaceIndicies = np.array([   [0, 1, 5, 5, 4, 0],     # left
                                [2, 3, 7, 7, 6, 2],     # right
                                [0, 3, 2, 2, 1, 0],     # bottom
                                [4, 5, 6, 6, 7, 4],     # top
                                [3, 0, 4, 4, 7, 3],     # back
                                [1, 2, 6, 6, 5, 1]],    # front
                                dtype=np.uint32)

leftFace = np.array([0, 1, 5, 5, 4, 0], dtype=np.uint32)
rightFace = np.array([2, 3, 7, 7, 6, 2], dtype=np.uint32)
bottomFace = np.array([0, 3, 2, 2, 1, 0], dtype=np.uint32)
topFace = np.array([4, 5, 6, 6, 7, 4], dtype=np.uint32)
backFace = np.array([3, 0, 4, 4, 7, 3], dtype=np.uint32)
frontFace = np.array([1, 2, 6, 6, 5, 1], dtype=np.uint32)


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
    global cubeEBO

    global leftEBO
    global rightEBO
    global bottomEBO
    global topEBO
    global backEBO
    global frontEBO

    cubeVBO = glGenBuffers(1)
    #glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)
    #glBufferData(GL_ARRAY_BUFFER, cubeVertices, GL_STATIC_DRAW)

    cubeEBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cubeEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, cubeIndices, GL_STATIC_DRAW)

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

        model = maths3d.m4_translatev(self.pos)
        glUniformMatrix4fv(shader.locations[b"modelBlock"], 1, GL_FALSE, model.m)

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

            #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, bottomEBO)
            #glDrawArrays(GL_TRIANGLES, 0, cubeVertices.size)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)


class chunk:

    def __init__(self, x=0, y=0, z=0):
        self.pos = maths3d.vec3(x, y, z)
        self.blocks = [[[0 for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        self.vertices = np.array([], dtype=np.float32)
        self.generate()
        self.generateMesh()
        self.vbo = GLuint(-1)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)
        #glBufferData(GL_ARRAY_BUFFER, self.vertices.size * self.vertices.itemsize, self.vertices, GL_STATIC_DRAW)


    def render(self, shader):
        model = maths3d.m4_translatev(self.pos)
        glUniformMatrix4fv(shader.locations[b"modelChunk"], 1, GL_FALSE, model.m)
        #glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        #glVertexPointer(3, GL_FLOAT, 0, None)
        #glDrawArrays(GL_TRIANGLES, 0, self.vertices.size)
        #return
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
        vertices = []
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
                            faces.append(FACE.BOTTOM)
                        elif self.blocks[k][j - 1][i].type == 0:
                            faces.append(FACE.BOTTOM)

                        # bottom face
                        if j == CONST_HEIGHT - 1:
                            faces.append(FACE.TOP)
                        elif self.blocks[k][j + 1][i].type == 0:
                            faces.append(FACE.TOP)

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
                        for face in faces:
                            indicies = cubeFaceIndicies[face]
                            for indicie in indicies:
                                vertices.append(cubeVertices[indicie * 3] + i)
                                vertices.append(cubeVertices[indicie * 3 + 1] + j)
                                vertices.append(cubeVertices[indicie * 3 + 2] + k)
        self.vertices = np.array(vertices, dtype=np.float32)


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
         #createBufferObjects()


    def render(self, shader):
        # calls render
        #glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)

        for k in range(self.MAX_Z):
            for j in range(self.MAX_Y):
                for i in range(self.MAX_X):
                    #print(self.chunks[k][j][i].vbo)
                    print(self.chunks[k][j][i].vbo)
                    glBindBuffer(GL_ARRAY_BUFFER, self.chunks[k][j][i].vbo)
                    glDrawArrays(GL_TRIANGLES, 0, self.chunks[k][j][i].vertices.size)
                    #self.chunks[k][j][i].render(shader)


def main():
    print("terrain.py main")
    c = chunk()
    c.print()

if __name__ == "__main__":
    main()
