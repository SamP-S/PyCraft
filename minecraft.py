import numpy as np
import pygame
from pygame.locals import *

from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GLU import *

from ctypes import sizeof, c_float, c_void_p, c_uint
import ctypes

from random import random

# custom
import terrain
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
    test = True
    if test == True:
        # data
        cube = np.array([0.0, 0.0, 0.0,   0.0, 0.0, 1.0,   1.0, 0.0, 1.0,
                        1.0, 0.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 1.0,
                        1.0, 1.0, 1.0,   1.0, 1.0, 0.0],
                        dtype=np.float32)
        #shader
        shader = shaders.shader()
        camera = cameras.camera()
        # vao
        vao = GLuint(-1)
        glGenVertexArrays(1, vao)
        glBindVertexArray(vao)
        # vbo
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, cube.itemsize * cube.size, cube, GL_STATIC_DRAW)
        # attributes
        for attrib in shader.attribs:
            glEnableVertexAttribArray(shader.locations[attrib])
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        # projections
        #gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 50)
        #glTranslatef(0, 0, -5)
        # main
        while True:
            #glRotatef(0.01, 1, 1, 1)
            handleEvents()
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            # setup
            shader.use()
            glBindVertexArray(vao)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glVertexPointer(3, GL_FLOAT, 0, None)
            # uniforms
            glUniformMatrix4fv(shader.locations[b"proj"], 1, GL_TRUE, maths3d.mat4().m)
            glUniformMatrix4fv(shader.locations[b"view"], 1, GL_TRUE, maths3d.mat4().m)
            glUniformMatrix4fv(shader.locations[b"modelBlock"], 1, GL_TRUE, maths3d.mat4().m)
            glUniformMatrix4fv(shader.locations[b"modelChunk"], 1, GL_TRUE, maths3d.mat4().m)
            # draw
            glDrawArrays(GL_TRIANGLES, 0, cube.size)
            pygame.display.flip()
#########################################

    shader = shaders.shader()
    land = terrain.terrain()
    camera = cameras.camera()

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
    print("start")
    while True:

        handleEvents()
        camera.process(keyboard, mouse)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        shader.use()
        player_cam.set(shader)
        #land.render(shader)

        shaders.glErrorCheck()

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

        pygame.display.flip()

        # fps counter
        # print(1 / frametimer.getTime())
        # frametimer.reset()


if __name__ == "__main__":
    main()
