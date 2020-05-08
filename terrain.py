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

leftFace = np.array([0, 4, 5, 5, 1, 0], dtype='uint')
rightFace = np.array([2, 6, 7, 7, 3, 2], dtype='uint')
bottomFace = np.array([0, 1, 2, 2, 3, 0], dtype='uint')
topFace = np.array([4, 7, 6, 6, 5, 4], dtype='uint')
backFace = np.array([3, 7, 4, 4, 0, 3], dtype='uint')
frontFace = np.array([1, 5, 6, 6, 2, 1], dtype='uint')


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

    def setFaces(self, faces):
        self.faces = faces

    def render(self, shader):
        #uni = glGetUniformLocation(shader.id, "model")
        #glUniformMatrix4fv(uni, 1, GL_TRUE, model.m)
        if len(self.faces) == 0:
            return

        uni = glGetUniformLocation(shader.id, "colour")
        colour = blockRGB[self.type]
        glUniform4f(uni, colour[0], colour[1], colour[2], colour[3])


        #glDrawElements <- 6 indicies for square
        for face in self.faces:
            if face == FACE.LEFT:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, leftEBO)
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, leftFace)
            if face == FACE.RIGHT:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, rightEBO)
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, rightFace)
            if face == FACE.BOTTOM:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, bottomEBO)
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, bottomFace)
            if face == FACE.TOP:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, topEBO)
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, topFace)
            if face == FACE.BACK:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, backEBO)
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, backFace)
            if face == FACE.FRONT:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, frontEBO)
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, frontFace)
            #glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, cubeVBO)




class chunk:

    def __init__(self, x=0, y=0, z=0):
        self.pos = maths3d.vec3(x, y, z)
        self.data = [[[0 for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        self.generate()
        self.generateMesh()

        # generate VAO
        self.vao = GLuint(0)
        glGenVertexArrays(1, self.vao)
        glBindVertexArray(self.vao)

        # generate VBO
        #self.vbo = glGenBuffers(1)
        #glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        #glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)
        #shaders.glErrorCheck()

        # bind attributes
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    def render(self, shader):
        # assign uniforms
        # bind vertex_array_object
        # bind vbo
        # draw elements

        model = maths3d.m4_translate(-self.pos.x, -self.pos.y, -self.pos.z)
        model = maths3d.mat4()
        uni = glGetUniformLocation(shader.id, "model")
        glUniformMatrix4fv(uni, 1, GL_TRUE, model.m)

        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    self.data[k][j][i].render(shader)
        #print("model")
        #shaders.glErrorCheck()
        #print(self.vertices.size)

        glBindVertexArray(self.vao)
        #glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)
        glVertexPointer(3, GL_FLOAT, 0, None)
        #glDrawArrays(GL_TRIANGLES, 0, self.vertices.size)


    def generate(self):
        perlin = noise.getPerlinIMG(2)
        for k in range(CONST_DEPTH):
            for i in range(CONST_WIDTH):
                offset = perlin[k][i] * CONST_AMPLITUE
                for j in range(CONST_HEIGHT):
                    if j > 63 + offset:
                        self.data[k][j][i] = block(BLOCK.AIR, maths3d.vec3(i, j, k))
                    elif j < 20:
                        self.data[k][j][i] = block(BLOCK.STONE, maths3d.vec3(i, j, k))
                    else:
                        self.data[k][j][i] = block(BLOCK.DIRT, maths3d.vec3(i, j, k))

    if False:
        def addMesh(self, face, x, y, z):
            quadIndicies = squareQuads[face]
            for index in quadIndicies:
                vertex = cubeVertices[index]
                self.vertices = np.append(self.vertices, x + vertex[0])
                self.vertices = np.append(self.vertices, y + vertex[1])
                self.vertices = np.append(self.vertices, z + vertex[2])

    def generateMesh(self):
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    # if solid -> check for visible mesh
                    if self.data[k][j][i].type != 0:
                        faces = []

                        # left face
                        if i == 0:
                            faces.append(FACE.LEFT)
                        elif self.data[k][j][i - 1].type == 0:
                            faces.append(FACE.LEFT)

                        # right face
                        if i == CONST_WIDTH - 1:
                            faces.append(FACE.RIGHT)
                        elif self.data[k][j][i + 1].type == 0:
                            faces.append(FACE.RIGHT)

                        # top face
                        if j == 0:
                            faces.append(FACE.TOP)
                        elif self.data[k][j - 1][i].type == 0:
                            faces.append(FACE.TOP)

                        # bottom face
                        if j == CONST_HEIGHT - 1:
                            faces.append(FACE.BOTTOM)
                        elif self.data[k][j + 1][i].type == 0:
                            faces.append(FACE.BOTTOM)

                        # back face
                        if k == 0:
                            faces.append(FACE.BACK)
                        elif self.data[k - 1][j][i].type == 0:
                            faces.append(FACE.BACK)

                        # front face
                        if k == CONST_DEPTH - 1:
                            faces.append(FACE.FRONT)
                        elif self.data[k + 1][j][i].type == 0:
                            faces.append(FACE.FRONT)

                        self.data[k][j][i].setFaces(faces)


    if False:
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


def main():
    print("terrain.py main")
    c = chunk()
    c.print()

if __name__ == "__main__":
    main()
