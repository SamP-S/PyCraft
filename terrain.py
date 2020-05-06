from OpenGL.GL import shaders
from OpenGL.GL import vbo
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GL import *
from OpenGL.GLU import *

import enum
from random import random

print("terrain.py")

CONST_WIDTH = 16
CONST_DEPTH = 16
CONST_HEIGHT = 256

cubeVertices = ((0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0), (0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0))
cubeQuads = ((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 7, 6, 5))
cubeEdges = ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))

xSquareQuads = (0, 4, 5, 1)
ySquareQuads = (0, 1, 2, 3)
zSquareQuads = (3, 7, 4, 0)

xSquareEdges = ((0, 4), (4, 5), (5, 1), (1, 0))
ySquareEdges = ((0, 1), (1, 2), (2, 3), (3, 0))
zSquareEdges = ((3, 7), (7, 4), (4, 0), (0, 3))


class FACE(enum.Enum):
    TOP = 0
    BOTTOM = 1
    RIGHT = 2
    LEFT = 3
    FRONT = 4
    BACK = 5


def quadSquare(face):
    glPushMatrix()
    glColor3f(1, 1, 1)
    geometry = ()

    if face == FACE.TOP:
        glTranslatef(0, 1, 0)
        geometry = ySquareQuads
    elif face == FACE.BOTTOM:
        glTranslatef(0, 0, 0)
        geometry = ySquareQuads
    elif face == FACE.RIGHT:
        glTranslatef(1, 0, 0)
        geometry = xSquareQuads
    elif face == FACE.LEFT:
        glTranslatef(0, 0, 0)
        geometry = xSquareQuads
    elif face == FACE.FRONT:
        glTranslatef(0, 0, 1)
        geometry = zSquareQuads
    elif face == FACE.BACK:
        glTranslatef(0, 0, 0)
        geometry = zSquareQuads

    glBegin(GL_QUADS)
    for vertex in geometry:
        glVertex3fv(cubeVertices[vertex])
    glEnd()
    glPopMatrix()

def edgeSquare(face):
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glPushMatrix()
            glColor3f(0, 0, 0)
            glScalef(1.01, 1.01, 1.01)
            glVertex3fv(cubeVertices[cubeVertex])
            glPopMatrix()
    glEnd()



def quadCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glColor3f(1, 1, 1)
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def edgeCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glPushMatrix()
            glColor3f(0, 0, 0)
            glScalef(1.01, 1.01, 1.01)
            glVertex3fv(cubeVertices[cubeVertex])
            glPopMatrix()
    glEnd()


class chunk:

    def __init__(self):
        self.data = [[[0 for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        self.generate()

    def generate(self):
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    if j > 1:
                        self.data[k][j][i] = 0
                    else:
                        self.data[k][j][i] = 1

    def print(self):
        for k in range(CONST_DEPTH):
            print ()
            for j in range(CONST_HEIGHT):
                print()
                for i in range(CONST_WIDTH):
                    print(self.data[k][j][i])

    def render(self):
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    if self.data[k][j][i] == 1:

                        # left face
                        if i == 0:
                            quadSquare(FACE.LEFT)
                        elif self.data[k][j][i - 1] == 0:
                            quadSquare(FACE.LEFT)

                        # right face
                        if i == CONST_WIDTH - 1:
                            quadSquare(FACE.RIGHT)
                        elif self.data[k][j][i + 1] == 0:
                            quadSquare(FACE.RIGHT)

                        # top face
                        if j == 0:
                            quadSquare(FACE.BOTTOM)
                        elif self.data[k][j - 1][i] == 0:
                            quadSquare(FACE.BOTTOM)

                        # bottom face
                        if j == CONST_HEIGHT - 1:
                            quadSquare(FACE.TOP)
                        elif self.data[k][j + 1][i] == 0:
                            quadSquare(FACE.TOP)

                        # back face
                        if k == 0:
                            quadSquare(FACE.BACK)
                        elif self.data[k - 1][j][i] == 0:
                            quadSquare(FACE.BACK)

                        # front face
                        if k == CONST_DEPTH - 1:
                            quadSquare(FACE.FRONT)
                        elif self.data[k + 1][j][i] == 0:
                            quadSquare(FACE.FRONT)

                    glTranslatef(1, 0, 0)
                glTranslatef(-CONST_WIDTH, 0, 0)
                glTranslatef(0, 1, 0)
            glTranslatef(0, -CONST_HEIGHT, 0)
            glTranslatef(0, 0, 1)
        glTranslatef(0, 0, -CONST_DEPTH)

def main():
    print("terrain.py main")
    c = chunk()
    c.print()

if __name__ == "__main__":
    main()
