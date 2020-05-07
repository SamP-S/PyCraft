import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import random

# custom
import terrain
import input
import camera
import timer
import noise

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360


# input management
keyboard = input.keyboard()
mouse = input.mouse()

# definitions
def glWindow():
    pygame.init()
    window = pygame.display
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Minecraft")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)


def handleEvents():
    pygame.mouse.set_pos = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            keyboard.processKey(event)
        elif event.type == pygame.MOUSEMOTION:
            mouse.processMotion(event)
        elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            mouse.processButton(event)


def main():
    print("minecraft")
    glWindow()
    chunk = terrain.chunk()
    player_cam = camera.camera()

    # lighting
    lightCol = [ 1.0, 1.0, 0.9, 1.0 ]
    lightPos = [ 8.0, 70.0, 8.0, 1.0 ]
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightCol)
    glShadeModel (GL_FLAT);
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # draw order
    glEnable(GL_DEPTH_TEST)
    # back face culling
    glFrontFace(GL_CW)
    glCullFace(GL_BACK)
    glEnable(GL_CULL_FACE)

    frametimer = timer.timer()
    while True:


        handleEvents()
        player_cam.process(keyboard, mouse)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        player_cam.setPerspective()
        player_cam.set()

        glPushMatrix()
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glPopMatrix()

        chunk.render()
        glPopMatrix()

        #print(noise.perlin(0, 0, round(random()*100)))
        pygame.display.flip()

        # fps counter
        # print(1 / frametimer.getTime())
        # frametimer.reset()


if __name__ == "__main__":
    main()
