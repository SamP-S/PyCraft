import numpy as np
import pygame
from pygame.locals import *

from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GLU import *

from random import random

# custom
import terrain
import input
import camera
import timer
import noise
import shaders

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360


def quadCube():
    cubeVertices = ((-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1))
    cubeQuads = ((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 7, 6, 5))
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

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
    shader = shaders.shader()
    chunk = terrain.chunk()
    player_cam = camera.camera()

    # lighting
    lightCol = [ 1.0, 1.0, 0.9, 1.0 ]
    lightPos = [ 5.0, 70.0, 5.0, 1.0 ]

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

        shader.use()
        player_cam.set(shader)
        chunk.render(shader)

        # attribute validation
        bufSize = 256
        length = (GLint * 1)()
        size = (GLint * 1)()
        type = (GLuint * 1)()
        name = ""


        countAttrib = glGetProgramiv(shader.id, GL_ACTIVE_ATTRIBUTES)
        #print("Active Attributes: ", countAttrib)
        for i in range(countAttrib):
            glGetActiveAttrib(shader.id, GLuint(i), bufSize, length, size, type, name)
            print("Attribute #", i, " Type: ", type, " Name: ", name)


        # uniform validation
        countUniforms = glGetProgramiv(shader.id, GL_ACTIVE_UNIFORMS)
        #print("Active Uniforms: ", countUniforms)
        for i in range(countUniforms):
            glGetActiveUniform(shader.id, i, bufSize, length, size, type, name)
            print("Attribute #", i, " Type: ", type, " Name: ", name)


        pygame.display.flip()

        # fps counter
        # print(1 / frametimer.getTime())
        # frametimer.reset()


if __name__ == "__main__":
    main()
