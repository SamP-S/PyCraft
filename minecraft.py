import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# custom
import terrain
import input
import camera
import timer

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

    frametimer = timer.timer()
    while True:
        handleEvents()
        player_cam.process(keyboard, mouse)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glPushMatrix()
        player_cam.setPerspective()
        player_cam.set()

        chunk.render()
        glPopMatrix()
        pygame.display.flip()

        # fps counter
        # print(1 / frametimer.getTime())
        # frametimer.reset()


if __name__ == "__main__":
    main()
