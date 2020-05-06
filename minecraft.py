import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# custom
import terrain

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360

cubeVertices = ((-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1))
cubeQuads = ((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 7, 6, 5))

# definitions
def glWindow():
    pygame.init()
    window = pygame.display
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Minecraft")
    gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 50)
    glTranslatef(0, 0, -10)
    glScalef(0.5, 0.5, 0.5)


def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def quadCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()


def main():
    print("minecraft")
    glWindow()
    c = terrain.chunk()
    while True:
        handleEvents()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #quadCube()
        for k in range(terrain.CONST_DEPTH):
            glTranslatef(0, 0, 1)
            for j in range(terrain.CONST_HEIGHT):
                glTranslatef(0, 1, 0)
                for i in range(terrain.CONST_WIDTH):
                    glTranslatef(1, 0, 0)
                    quadCube()
                glTranslatef(-terrain.CONST_WIDTH, 0, 0)
            glTranslatef(0, -terrain.CONST_HEIGHT, 0)
        glTranslatef(0, 0, -terrain.CONST_DEPTH)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
