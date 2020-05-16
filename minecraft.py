import numpy as np
import pygame
from pygame.locals import *

from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GLU import *

from random import random

# custom
from terrain import *
import input
import cameras
from timer import *
import noise
import shaders
from maths3d import *


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
    frametimer = timer()
    while True:
        handleEvents()
        camera.process(keyboard, mouse)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        shader.use()

        glUniformMatrix4fv(shader.locations[b"proj"], 1, uniform_transpose, maths3d.m4_perspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 1000).m)
        glUniformMatrix4fv(shader.locations[b"view"], 1, uniform_transpose, camera.view.m)

        glBindVertexArray(vao)
        terrain.render(shader)

        pygame.display.flip()

        # fps counter
        #print("fps: ", 1000 / frametimer.getTime())
        frametimer.reset()


if __name__ == "__main__":
    main()
