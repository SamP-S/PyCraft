import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# custom
import terrain
import input
import camera

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360


# input management
keyboard = input.keyboard()

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
        else:
            keyboard.processEvent(event)


def main():
    print("minecraft")
    glWindow()
    chunk = terrain.chunk()
    player_cam = camera.camera()
    while True:
        handleEvents()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #quadCube()

        player_cam.pos.y += 0.01
        glPushMatrix()
        player_cam.set()

        chunk.render()

        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
