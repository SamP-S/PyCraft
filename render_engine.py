from maths3d import *
import models

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

        vs = self.vertex()
        fs = self.fragment()

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

    def vertex(self):
        v = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec4 colour;
        layout(location = 2) in mat4 model;

        uniform mat4 view;
        uniform mat4 proj;

        out vec4 solidColour;

        void main()
        {
            solidColour = colour;
            gl_Position = proj * view * model * vec4(position, 1.0);
        }
        """
        return self.create(GL_VERTEX_SHADER, v)

    def fragment(self):
        f = """
        #version 330
        in vec4 solidColour;
        out vec4 fragColour;
        void main()
        {
            fragColour = solidColour;
        }
        """
        return self.create(GL_FRAGMENT_SHADER, f)


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

        # list of loaded models
        self.vaos = []
        self.vbos = []
        self.ebos = []
        self.models = []
        self.load_models()
        self.setup_models()

        # list of all cameras
        self.cameras = []

        # list of lists of each mesh instance by mesh
        self.drawlists = [ [[], []] for i in range(len(self.models)) ]

        self.pos = vec3(0, 0, -3)

    def load_models(self):
        print("load models")
        # for each model in model folder
        # load mesh
        # load material
        # add to list


        # hardcoded for now
        cubeMesh = models.mesh("cube_mesh", models.cubeVertices, models.cubeIndices)
        cubeMaterial = models.material("cube_material")
        cubeModel = models.model("cube_model", cubeMesh, cubeMaterial)
        self.models.append(cubeModel)
        # seems to fuck with the setup
        return

        playerMesh = models.mesh("player_mesh", models.playerVertices, models.playerIndices)
        playerMaterial = models.material("player_material")
        playerModel = models.model("player_model", playerMesh, playerMaterial)
        self.models.append(playerModel)

    def setup_models(self):
        print("setup models")
        for i in range(len(self.models)):
            # VAO
            vao = GLuint(-1)
            glGenVertexArrays(1, vao)
            glBindVertexArray(vao)
            for attrib in self.shader.attribs:
                glEnableVertexAttribArray(self.shader.locations[attrib])
            # VBO
            vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, self.models[i].mesh.vertices, GL_STATIC_DRAW)
            # EBO
            ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.models[i].mesh.indices, GL_STATIC_DRAW)
            # position attribute
            glVertexAttribPointer(self.shader.locations[b"position"], 3, GL_FLOAT, GL_FALSE, 0, None)

            # Add to lists
            self.vaos.append(vao)
            self.vbos.append(vbo)
            self.ebos.append(ebo)

            # instance
            if True:
                # vbo for colour
                colourVBO = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, colourVBO)
                glBufferData(GL_ARRAY_BUFFER, self.colourArr, GL_STATIC_DRAW)

                # colour instance attribute
                colourLoc = self.shader.locations[b"colour"]
                glBindBuffer(GL_ARRAY_BUFFER, colourVBO)
                glEnableVertexAttribArray(colourLoc)
                glVertexAttribPointer(colourLoc, 4, GL_FLOAT, GL_FALSE, 0, None)
                glVertexAttribDivisor(colourLoc, 1)

                self.vbos.append(colourVBO)


            if True:
                # vbo for model transformations
                modelVBO = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, modelVBO)
                glBufferData(GL_ARRAY_BUFFER, self.transformArr, GL_STATIC_DRAW)
                print(self.transformArr)

                # model projection instance attribute
                modelLoc = self.shader.locations[b"model"]
                glBindBuffer(GL_ARRAY_BUFFER, modelVBO)

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

                self.vbos.append(modelVBO)



    def process_node(node, transform):
        worldPos = v3_add(transform.position, self.transform.position)
        worldRot = v3_add(transform.rotation, self.transform.rotation)
        worldScl = v3_add(transform.scale, self.transform.scale)
        worldTransform = transform(worldPos, worldRot, worldScl)

        # if game object has a camera component
        if node.camera != None:
            self.cameras.append(node)

        # if game object has a mesh component
        if node.model != None:
            # iterate through loaded mesh
            for i in range(len(self.models)):
                # if equal
                if node.model.mesh == self.models[i].mesh:
                    # add an instance to the mesh's draw list
                    self.drawlists[i][0].append(node.transform.getModel())
                    self.drawlists[i][1].append(node.model.material.colour)

        # process node's children
        for child in node.chilren:
            render_node(child, worldTransform)

    def test_render(self):
        self.shader.use()
        glUniformMatrix4fv(self.shader.locations[b"view"], 1, GL_FALSE, m4_translatev(self.pos).m)
        glBindVertexArray(self.vaos[0])
        glDrawElementsInstanced(GL_TRIANGLES, self.models[0].mesh.indices.size, GL_UNSIGNED_INT, None, 2)

    # pass in world tree with all gameobjects ("scene")
    def render(self, world):
        # use shader program
        self.shader.use()
        # perspective projection
        glUniformMatrix4fv(self.shader.locations[b"proj"], 1, GL_FALSE, self.viewport.projection.m)
        glUniformMatrix4fv(self.shader.locations[b"view"], 1, GL_FALSE, mat4().translate(0, 0, -5))

        self.drawlists = [ [] for i in range(len(models)) ]
        # tree traversal algorithm
        # render all game objects with mesh components
        for child in world.children:
            process_node(child)

        for i in range(len(self.drawlists)):
            transformArr = self.drawlists[i][0]
            colourArr = self.drawlists[i][1]
            # model transform

import pygame
from pygame.locals import *

def main():

    pygame.init()
    window = pygame.display
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Render Engine")
    renderer = render_engine()
    frame = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        renderer.test_render()

        pygame.display.flip()
        pygame.time.wait(10)
        frame += 1

        if frame == 100:
            renderer.colourArr = np.append(np.array([0, 1, 1, 1], dtype=np.float32), np.array([1, 1, 0, 1], dtype=np.float32))
            renderer.transformArr = np.append(m4_translate(-1, 0, 0).m, m4_translate(0, -1, 0).m)
            glBindBuffer(GL_ARRAY_BUFFER, renderer.vbos[1])
            glBufferData(GL_ARRAY_BUFFER, renderer.colourArr, GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, renderer.vbos[2])
            glBufferData(GL_ARRAY_BUFFER, renderer.transformArr, GL_STATIC_DRAW)
            print("buffer data changed")



if __name__ == "__main__":
    main()
