<<<<<<< HEAD
import numpy as np
import pygame
from pygame.locals import *

from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GLU import *

from random import random

# custom
import terrains
import input
import cameras
import timer
import noise
import shaders
import maths3d

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

#########################################
    depricated = False
    if depricated == True:
        cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1,1,-1))
        cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))
        glBegin(GL_QUADS)
        for cubeQuad in cubeQuads:
            for cubeVertex in cubeQuad:
                glVertex3fv(cubeVertices[cubeVertex])
        glEnd()
        pygame.display.flip()
        return
#########################################

    uniform_transpose = GL_FALSE
    shader = shaders.shader()
    terrain = terrains.terrain(shader)
    camera = cameras.camera()

    # lighting
    lightCol = [ 1.0, 1.0, 0.9, 1.0 ]
    lightPos = [ 5.0, 70.0, 5.0, 1.0 ]

    # draw order
    glEnable(GL_DEPTH_TEST)
    # back face culling
    glFrontFace(GL_CCW)
    glCullFace(GL_BACK)
    glEnable(GL_CULL_FACE)

    # vertex_array_object
    vao = GLuint(-1)
    glGenVertexArrays(1, vao)
    glBindVertexArray(vao)
    for attrib in shader.attribs:
        glEnableVertexAttribArray(shader.locations[attrib])
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    print("start")
    frametimer = timer.timer()
    while True:
        handleEvents()
        camera.process(keyboard, mouse)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        shader.use()

        glUniformMatrix4fv(shader.locations[b"proj"], 1, uniform_transpose, maths3d.m4_projection(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 1000).m)
        glUniformMatrix4fv(shader.locations[b"view"], 1, uniform_transpose, camera.view.m)
        glUniformMatrix4fv(shader.locations[b"modelBlock"], 1, uniform_transpose, maths3d.mat4().m)
        glUniformMatrix4fv(shader.locations[b"modelChunk"], 1, uniform_transpose, maths3d.mat4().m)

        glBindVertexArray(vao)

        terrain.render(shader)
        pygame.display.flip()

        debug = False
        if debug == True:
            # attribute validation
            bufSize = 256
            length = (GLint * 1)()
            size = (GLint * 1)()
            type = GLuint(0)
            name = bytearray(bufSize)

            countAttrib = glGetProgramiv(shader.id, GL_ACTIVE_ATTRIBUTES)
            print("Active Attributes: ", countAttrib)
            for i in range(countAttrib):
                glGetActiveAttrib(shader.id, GLuint(i), bufSize, length, size, type, name)
                print("Attribute #", i, " Type: ", type, " Name: ", name.decode("utf-8"))

                # uniform validation
                countUniforms = glGetProgramiv(shader.id, GL_ACTIVE_UNIFORMS)
                print("Active Uniforms: ", countUniforms)
                for i in range(countUniforms):
                    glGetActiveUniform(shader.id, i, bufSize, length, size, type, name)
                    print("Uniform #", i, " Type: ", type, " Name: ", name.decode("utf-8"))

        # fps counter
        #print("fps: ", 1000 / frametimer.getTime())
        frametimer.reset()


if __name__ == "__main__":
    main()
=======
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
>>>>>>> 1cf19361f5e172955bd752744e6c7c8b6d39a767
