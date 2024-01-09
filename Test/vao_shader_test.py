<<<<<<< HEAD:vao_shader_test.py
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
import terrains
import input
import cameras
import timer
import noise
import shaders
import maths3d

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360

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

test_shader = True
uniform_transpose = GL_FALSE
def main()
    print("####################")
    print("TESTING")
    print("####################")
    # data
    cube = np.array([0.0, 0.0, 0.0,   0.0, 0.0, 1.0,   1.0, 0.0, 1.0,
                     1.0, 0.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 1.0,
                     1.0, 1.0, 1.0,   1.0, 1.0, 0.0],
                     dtype=np.float32)
    #shader
    if test_shader == True:
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
    if test_shader == True:
        for attrib in shader.attribs:
            glEnableVertexAttribArray(shader.locations[attrib])
        else:
            glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    # projections
    if test_shader == False:
        gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 50)
        glTranslatef(0, -0.5, -5)
    # main
    while True:
        handleEvents()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # shader setup
        if test_shader == True:
            shader.use()
            glUniformMatrix4fv(shader.locations[b"proj"], 1, uniform_transpose, maths3d.m4_projection(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 50).m)
            glUniformMatrix4fv(shader.locations[b"view"], 1, uniform_transpose, maths3d.m4_translate(0, -0.5, -5).m)
            glUniformMatrix4fv(shader.locations[b"modelChunk"], 1, uniform_transpose, maths3d.mat4().m)
            glUniformMatrix4fv(shader.locations[b"modelBlock"], 1, uniform_transpose, maths3d.mat4().m)
        # vertex objects setup
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        #glVertexPointer(3, GL_FLOAT, 0, None)
        # draw
        glDrawArrays(GL_TRIANGLES, 0, cube.size)
        pygame.display.flip()


if __name__ == "__main__":
    main()
=======
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
import terrains
import input
import cameras
import timer
import noise
import shaders
import maths3d

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360

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

test_shader = True
uniform_transpose = GL_FALSE
def main()
    print("####################")
    print("TESTING")
    print("####################")
    # data
    cube = np.array([0.0, 0.0, 0.0,   0.0, 0.0, 1.0,   1.0, 0.0, 1.0,
                     1.0, 0.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 1.0,
                     1.0, 1.0, 1.0,   1.0, 1.0, 0.0],
                     dtype=np.float32)
    #shader
    if test_shader == True:
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
    if test_shader == True:
        for attrib in shader.attribs:
            glEnableVertexAttribArray(shader.locations[attrib])
        else:
            glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    # projections
    if test_shader == False:
        gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 50)
        glTranslatef(0, -0.5, -5)
    # main
    while True:
        handleEvents()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # shader setup
        if test_shader == True:
            shader.use()
            glUniformMatrix4fv(shader.locations[b"proj"], 1, uniform_transpose, maths3d.m4_projection(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 50).m)
            glUniformMatrix4fv(shader.locations[b"view"], 1, uniform_transpose, maths3d.m4_translate(0, -0.5, -5).m)
            glUniformMatrix4fv(shader.locations[b"model"], 1, uniform_transpose, maths3d.mat4().m)
        # vertex objects setup
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        #glVertexPointer(3, GL_FLOAT, 0, None)
        # draw
        glDrawArrays(GL_TRIANGLES, 0, cube.size)
        pygame.display.flip()


if __name__ == "__main__":
    main()
>>>>>>> 1cf19361f5e172955bd752744e6c7c8b6d39a767:Test/vao_shader_test.py
