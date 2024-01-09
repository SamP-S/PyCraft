# MODULES
import pygame
from pygame.locals import *


from timer import *
import terrain_2 as terrain


################################################################################
# INPUT MANAGEMENT
import input
global mouse
global keyboard
mouse = input.mouse()
keyboard = input.keyboard()


################################################################################
# PYGAME


################################################################################
# GRAPHICS
import graphics_engine
global graphics


################################################################################
# WORLD
import scene
global world


################################################################################
# pygame

# these need to be moved to graphics engine
# so opengl context in graphics engine
# not sure how to sort out events stuff though

def glWindow():
    pygame.init()
    window = pygame.display
    pygame.display.set_mode((graphics_engine.WINDOW_WIDTH, graphics_engine.WINDOW_HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Minecraft")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)


def handleEvents():
    pygame.mouse.set_pos = (graphics_engine.WINDOW_WIDTH / 2, graphics_engine.WINDOW_HEIGHT / 2)
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
# MAIN

def main():
    print("PyCraft")
    glWindow()
    # move to global declarations once pygame not in main
    graphics = graphics_engine.render_engine()
    world = scene.world()
    world.children.append(terrain.chunk())

    frame = 0
    t = timer()
    while True:
        handleEvents()
        world.camera.process(keyboard, mouse)
        graphics.render(world)

        pygame.display.flip()
        frame += 1

        if frame % 1000 == 0:
            print("fps: ", frame / t.getTime(False))

        if frame == 1000 and True:
            print("test block changes")
            world.children[0].change_block(terrain.BLOCK.AIR, 0, 0, 0)
            world.children[0].change_block(terrain.BLOCK.AIR, 1, 0, 0)
            world.children[0].change_block(terrain.BLOCK.STONE, 0, 0, 0)


if __name__ == "__main__":
    main()
