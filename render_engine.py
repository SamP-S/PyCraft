from maths3d import *
import models
import world
from objects import *
from timer import *

from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GLU import *

import numpy as np
from enum import IntEnum
import ctypes

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360
FOV = 45
Z_NEAR = 0.1
Z_FAR = 100


def glErrorCheck():
    err = glGetError()
    if err != GL_NO_ERROR:
        print("OPENGL_ERROR: ", gluErrorString(error))

def glShaderErrorCheck(program):
    err = glGetShaderiv(program, GL_COMPILE_STATUS);
    if err != GL_TRUE:
        log = glGetShaderInfoLog(program)
        print(log)

def glLinkErrorCheck(program):
    err = glGetProgramiv(program, GL_LINK_STATUS)
    if err != GL_TRUE:
        log = glGetProgramInfoLog(program)
        print(log)

def glCheckData(program):
    # attribute validation
    bufSize = 256
    length = (GLint * 1)()
    size = (GLint * 1)()
    type = GLuint(0)
    name = bytearray(bufSize)

    countAttrib = glGetProgramiv(program, GL_ACTIVE_ATTRIBUTES)
    print("Active Attributes: ", countAttrib)
    for i in range(countAttrib):
        glGetActiveAttrib(program, GLuint(i), bufSize, length, size, type, name)
        print("Attribute #", i, " Type: ", type, " Name: ", name.decode("utf-8"))

    # uniform validation
    countUniforms = glGetProgramiv(program, GL_ACTIVE_UNIFORMS)
    print("Active Uniforms: ", countUniforms)
    for i in range(countUniforms):
        glGetActiveUniform(program, i, bufSize, length, size, type, name)
        print("Uniform #", i, " Type: ", type, " Name: ", name.decode("utf-8"))


class shader:

    def __init__(self):
        self.attribs = [b"position", b"colour", b"model"]
        self.locations = dict((k, v) for (v, k) in enumerate(self.attribs))
        self.uniforms = [b"proj", b"view", ]

        v = open("shaders/vs_basic.glsl", 'r')
        f = open("shaders/fs_basic.glsl", 'r')

        vs = self.create(GL_VERTEX_SHADER, v)
        fs = self.create(GL_FRAGMENT_SHADER, f)

        program = glCreateProgram()
        glAttachShader(program, vs)
        glAttachShader(program, fs)
        for attrib in self.attribs:
                glBindAttribLocation(program, self.locations[attrib], attrib)
        glBindFragDataLocation(program, 0, "fragColour");
        glLinkProgram(program)
        glLinkErrorCheck(program)
        for uniform in self.uniforms:
            self.locations[uniform] = glGetUniformLocation(program, uniform)
        glUseProgram(program)
        self.id = program

    def create(self, type, source):
        shader = glCreateShader(type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        glShaderErrorCheck(shader)
        return shader

    def use(self):
        glUseProgram(self.id)


class size:

    def __init__(self, width=-1, height=-1):
        self.width = width
        self.height = height

class viewport:

    Z_NEAR = 0.1
    Z_FAR = 100

    def __init__(self, fov=45, resolution=size(WINDOW_WIDTH, WINDOW_HEIGHT)):
        self.fov = fov
        self.resolution = resolution
        w = self.resolution.width
        h = self.resolution.height
        aspect = w / h
        self.projection = m4_perspective(self.fov, aspect, self.Z_NEAR, self.Z_FAR)


class render_engine:

    # make vao
    # bind vao
    # bind vbo
    # enable attrbutes
    # set attribute pointers

    def __init__(self):
        ("init render engine")
        self.viewport = viewport()
        self.shader = shader()
        glUniformMatrix4fv(self.shader.locations[b"proj"], 1, GL_FALSE, self.viewport.projection.m)
        glUniformMatrix4fv(self.shader.locations[b"view"], 1, GL_FALSE, mat4().m)

        self.transformArr = np.append(m4_translate(0, 0, 0).m, m4_translate(-1, -1, 0).m)
        self.colourArr = np.append(np.array([1, 1, 1, 1], dtype=np.float32), np.array([1, 0, 0, 1], dtype=np.float32))

        # arrays of buffer objects
        self.vaos = []
        self.vbos = []
        self.ebos = []

        # store loaded model data
        # seperated meshes and materials for easier individual reuse
        self.meshes = []
        self.materials = []

        # store some preset models
        # mgiht be a bad idea :/
        self.models = []

        # load models
        self.load_models()
        self.setup_models()

        # list of all cameras
        self.cameras = []

        # list of lists of each mesh instance by mesh
        self.drawlists = [ [[], []] for i in range(len(self.models)) ]

        self.pos = vec3(0, 0, -3)


    # currently all models are hardcoded in here
    # later: make it read from json to get all models
    # ONLY able when models are on file tho
    def load_models(self):
        print("load models")

        # cube
        cubeMesh = models.mesh(0, "cube_mesh", models.cubeVertices, models.cubeIndices)
        self.meshes.append(cubeMesh)

        cubeMaterial = models.solid_material(0, "cube_material")
        self.materials.append(cubeMaterial)

        cubeModel = models.model(0, "cube_model", cubeMesh.id, cubeMaterial.id)
        self.models.append(cubeModel)

        # player
        playerMesh = models.mesh(1, "player_mesh", models.playerVertices, models.playerIndices)
        self.meshes.append(playerMesh)

        playerMaterial = models.solid_material(1, "player_material")
        self.materials.append(playerMaterial)

        playerModel = models.model(1, "player_model", playerMesh, playerMaterial)
        self.models.append(playerModel)

    def setup_models(self):
        print("setup meshes")
        for i in range(len(self.meshes)):
            # VAO
            vao = GLuint(-1)
            glGenVertexArrays(1, vao)
            glBindVertexArray(vao)
            for attrib in self.shader.attribs:
                glEnableVertexAttribArray(self.shader.locations[attrib])
            # VBO
            vbos = glGenBuffers(3)
            glBindBuffer(GL_ARRAY_BUFFER, vbos[0])
            glBufferData(GL_ARRAY_BUFFER, self.meshes[i].vertices, GL_STATIC_DRAW)
            # EBO
            ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.meshes[i].indices, GL_STATIC_DRAW)

            # position attribute
            glVertexAttribPointer(self.shader.locations[b"position"], 3, GL_FLOAT, GL_FALSE, 0, None)

            # instance
            if True:
                # vbo for colour
                glBindBuffer(GL_ARRAY_BUFFER, vbos[1])
                glBufferData(GL_ARRAY_BUFFER, self.colourArr, GL_STATIC_DRAW)

                # colour instance attribute
                colourLoc = self.shader.locations[b"colour"]
                glBindBuffer(GL_ARRAY_BUFFER, vbos[1])
                glEnableVertexAttribArray(colourLoc)
                glVertexAttribPointer(colourLoc, 4, GL_FLOAT, GL_FALSE, 0, None)
                glVertexAttribDivisor(colourLoc, 1)

            if True:
                # vbo for model transformations
                glBindBuffer(GL_ARRAY_BUFFER, vbos[2])
                glBufferData(GL_ARRAY_BUFFER, self.transformArr, GL_STATIC_DRAW)

                # model projection instance attribute
                modelLoc = self.shader.locations[b"model"]
                glBindBuffer(GL_ARRAY_BUFFER, vbos[2])

                glEnableVertexAttribArray(modelLoc    )
                glVertexAttribPointer(modelLoc    , 4, GL_FLOAT, GL_FALSE, self.transformArr.itemsize * 16, ctypes.c_void_p(0))
                glEnableVertexAttribArray(modelLoc + 1)
                glVertexAttribPointer(modelLoc + 1, 4, GL_FLOAT, GL_FALSE, self.transformArr.itemsize * 16, ctypes.c_void_p(self.transformArr.itemsize * 4))
                glEnableVertexAttribArray(modelLoc + 2)
                glVertexAttribPointer(modelLoc + 2, 4, GL_FLOAT, GL_FALSE, self.transformArr.itemsize * 16, ctypes.c_void_p(self.transformArr.itemsize * 8))
                glEnableVertexAttribArray(modelLoc + 3)
                glVertexAttribPointer(modelLoc + 3, 4, GL_FLOAT, GL_FALSE, self.transformArr.itemsize * 16, ctypes.c_void_p(self.transformArr.itemsize * 12))

                glVertexAttribDivisor(modelLoc    , 1);
                glVertexAttribDivisor(modelLoc + 1, 1);
                glVertexAttribDivisor(modelLoc + 2, 1);
                glVertexAttribDivisor(modelLoc + 3, 1);


            # Add to lists
            self.vaos.append(vao)
            self.vbos.append(vbos)
            self.ebos.append(ebo)


    def process(self, world):
        worldPos = vec3(0, 0, 0)
        worldRot = vec3(0, 0, 0)
        worldScl = vec3(1, 1, 1)
        worldTransform = transform(worldPos, worldRot, worldScl)

        for child in world.children:
            self.process_node(child, worldTransform)

    def process_node(self, node, origin):
        # if game object has a camera component
        if node.camera != None:
            self.cameras.append(node)

        # if game object has a mesh component
        if node.mesh != None:
            # iterate through loaded mesh
            for i in range(len(self.meshes)):
                # if equal
                if node.mesh == self.meshes[i].id:
                    # add an instance to the mesh's draw list
                    #print("node: ", node.transform.getModel())
                    self.drawlists[i][0] = np.append(self.drawlists[i][0], node.transform.getModel())
                    self.drawlists[i][1] = np.append(self.drawlists[i][1], np.array(self.materials[node.material].colour, dtype=np.float32))
                    break

        if len(node.children) == 0:
            return

        # gets new local origin for children
        worldPos = v3_add(origin.position, node.transform.position)
        worldRot = v3_add(origin.rotation, node.transform.rotation)
        worldScl = v3_add(origin.scale, node.transform.scale)
        worldTransform = transform(worldPos, worldRot, worldScl)

        # process node's children
        for child in node.children:
            self.process_node(child, worldTransform)

    def test_render(self):
        # called once
        self.shader.use()
        glUniformMatrix4fv(self.shader.locations[b"view"], 1, GL_FALSE, m4_translatev(self.pos).m)

        # iterate through every model's draw list
        glBindVertexArray(self.vaos[0])
        glDrawElementsInstanced(GL_TRIANGLES, self.meshes[0].indices.size, GL_UNSIGNED_INT, None, 2)

    # pass in world tree with all gameobjects ("scene")
    def render(self, world):
        t = timer()
        self.drawlists = [ [np.array([], dtype=np.float32), np.array([], dtype=np.float32)] for i in range(len(self.meshes)) ]
        self.process(world)

        # use shader program
        self.shader.use()
        # perspective projection
        glUniformMatrix4fv(self.shader.locations[b"proj"], 1, GL_FALSE, self.viewport.projection.m)
        glUniformMatrix4fv(self.shader.locations[b"view"], 1, GL_FALSE, world.camera.view.m)

        for i in range(len(self.meshes)):
            #print(self.drawlists[i][0])
            glBindVertexArray(self.vaos[i])
            glBindBuffer(GL_ARRAY_BUFFER, self.vbos[i][1])
            glBufferData(GL_ARRAY_BUFFER, self.drawlists[i][1], GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbos[i][2])
            glBufferData(GL_ARRAY_BUFFER, self.drawlists[i][0], GL_STATIC_DRAW)
            instances = round(self.drawlists[i][1].size / 4)
            glDrawElementsInstanced(GL_TRIANGLES, self.meshes[i].indices.size, GL_UNSIGNED_INT, None, instances)


import pygame
from pygame.locals import *
import input

global mouse
global keyboard
mouse = input.mouse()
keyboard = input.keyboard()

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

    pygame.init()
    window = pygame.display
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Render Engine")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    renderer = render_engine()
    frame = 0
    scene = world.world()
    while True:
        handleEvents()
        scene.camera.process(keyboard, mouse)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        renderer.render(scene)

        pygame.display.flip()
        frame += 1

        if frame == 100 and True:
            print("changed buffer")
            print("r", renderer.drawlists[0][1][0], "g", renderer.drawlists[0][1][1], "b", renderer.drawlists[0][1][2], "a", renderer.drawlists[0][1][3])
            renderer.drawlists[0][1][0] = 1.0
            renderer.drawlists[0][1][1] = 0.0
            renderer.drawlists[0][1][2] = 0.0
            renderer.drawlists[0][1][3] = 1.0
            glBindBuffer(GL_ARRAY_BUFFER, renderer.vbos[0][1])
            glBufferData(GL_ARRAY_BUFFER, renderer.drawlists[0][1], GL_STATIC_DRAW)

        if frame == 100 and False:
            renderer.colourArr = np.append(np.array([0, 1, 1, 1], dtype=np.float32), np.array([1, 1, 0, 1], dtype=np.float32))
            renderer.transformArr = np.append(m4_translate(-1, 0, 0).m, m4_translate(0, -1, 0).m)
            glBindBuffer(GL_ARRAY_BUFFER, renderer.vbos[0][1])
            glBufferData(GL_ARRAY_BUFFER, renderer.colourArr, GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, renderer.vbos[0][2])
            glBufferData(GL_ARRAY_BUFFER, renderer.transformArr, GL_STATIC_DRAW)
            print("buffer data changed")



if __name__ == "__main__":
    main()
