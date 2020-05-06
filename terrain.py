from OpenGL.GL import *
from OpenGL.GLU import *

from random import random

print("terrain.py")

CONST_WIDTH = 2
CONST_DEPTH = 2
CONST_HEIGHT = 1

cubeVertices = ((0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0), (0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0))
cubeQuads = ((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 7, 6, 5))

def quadCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()


class chunk:

    def __init__(self):
        self.data = [[[0 for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        self.generate()

    def generate(self):
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    self.data[k][j][i] = random()

    def print(self):
        for k in range(CONST_DEPTH):
            print ()
            for j in range(CONST_HEIGHT):
                print()
                for i in range(CONST_WIDTH):
                    print(self.data[k][j][i])

    def render(self):
        for k in range(CONST_DEPTH):
            glTranslatef(0, 0, 1)
            for j in range(CONST_HEIGHT):
                glTranslatef(0, 1, 0)
                for i in range(CONST_WIDTH):
                    glTranslatef(1, 0, 0)
                    glColor3f(self.data[k][j][i], self.data[k][j][i], self.data[k][j][i])
                    quadCube()
                glTranslatef(-CONST_WIDTH, 0, 0)
            glTranslatef(0, -CONST_HEIGHT, 0)
        glTranslatef(0, 0, -CONST_DEPTH)

def main():
    print("terrain.py main")
    c = chunk()
    c.print()

if __name__ == "__main__":
    main()
