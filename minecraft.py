# MODULES
import pygame
from pygame.locals import *


from timer import *
import terrain_2 as terrain


################################################################################
# pygame

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


################################################################################
# Input Management
import input
global mouse
global keyboard
mouse = input.mouse()
keyboard = input.keyboard()


################################################################################
# GLOBALS
import scene
global world
world = scene.world()
world.children.append(terrain.chunk())

import graphics_engine
global graphics
graphics = graphics_engine.render_engine()


################################################################################
# MAIN

def main():
    print("PyCraft")

    ###### MOVE PYGAME DISPLAY TO GRAPHICS
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Render Engine")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    frame = 0

    t = timer()
    while True:
        #print("frame")

        handleEvents()
        world.camera.process(keyboard, mouse)
        graphics.render(world)

        pygame.display.flip()
        frame += 1

        if frame % 1000 == 0:
            print("fps: ", frame / t.getTime(False))

        if frame == 1000 and True:
            scene.children[0].change_block(terrain.BLOCK.AIR, 0, 0, 0)
            scene.children[0].change_block(terrain.BLOCK.STONE, 0, 0, 0)


if __name__ == "__main__":
    main()
