from maths3d import *
import mesh

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

def glShaderErrorCheck(shader):
    err = glGetShaderiv(shader, GL_COMPILE_STATUS);
    if err != GL_TRUE:
        log = glGetShaderInfoLog(shader)
        print(log)

def glLinkErrorCheck(program):
    err = glGetProgramiv(program, GL_LINK_STATUS)
    if err != GL_TRUE:
        log = glGetProgramInfoLog(program)
        print(log)


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

        print("translate 1:")
        print(m4_translate(0, 0, -1).m)
        print("translate 2:")
        print(m4_translate(-1, -1, -1).m)
        print("array")
        print(np.append(m4_translate(0, 0, 0).m, m4_translate(0, 0, 0).m))

        self.modelArr = np.append(m4_translate(0, 0, 0).m, m4_translate(-1, -1, 0).m)
        self.colourArr = np.append(np.array([1, 1, 1, 1], dtype=np.float32), np.array([1, 0, 0, 1], dtype=np.float32))

        # list of loaded meshes
        self.vaos = []
        self.vbos = []
        self.ebos = []
        self.meshes = []
        self.load_meshes()
        self.setup_meshes()

        # list of all cameras
        self.cameras = []

        # list of lists of each mesh instance by mesh
        self.drawlists = [ [[], []] for i in range(len(self.meshes)) ]

        self.pos = vec3(0, 0, -3)

    def load_meshes(self):
        print("load meshes")
        # for each mesh in mesh folder
        # load geometry
        # load material
        # add to list


        # hardcoded for now
        cubeGeometry = mesh.geometry(mesh.cubeVertices, mesh.cubeIndices)
        cubeMaterial = mesh.material()
        cubeMesh = mesh.mesh(cubeGeometry, cubeMaterial)
        self.meshes.append(cubeMesh)
        # seems to fuck with the setup
        return

        playerGeometry = mesh.geometry(mesh.playerVertices, mesh.playerIndices)
        playerMaterial = mesh.material()
        playerMesh = mesh.mesh(playerGeometry, playerMaterial)
        self.meshes.append(playerMesh)

    def setup_meshes(self):
        print("setup meshes")
        for i in range(len(self.meshes)):
            # VAO
            vao = GLuint(-1)
            glGenVertexArrays(1, vao)
            glBindVertexArray(vao)
            for attrib in self.shader.attribs:
                glEnableVertexAttribArray(self.shader.locations[attrib])

            # VBO
            vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, self.meshes[i].geometry.vertices, GL_STATIC_DRAW)
            # EBO
            ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.meshes[i].geometry.indices, GL_STATIC_DRAW)
            print(self.meshes[i].geometry.indices)
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

                print(colourLoc)
                self.vbos.append(colourVBO)


            if True:
                # vbo for model transformations
                modelVBO = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, modelVBO)
                glBufferData(GL_ARRAY_BUFFER, self.modelArr, GL_STATIC_DRAW)
                print(self.modelArr)

                # model projection instance attribute
                modelLoc = self.shader.locations[b"model"]
                glBindBuffer(GL_ARRAY_BUFFER, modelVBO)

                glEnableVertexAttribArray(modelLoc    )
                glVertexAttribPointer(modelLoc    , 4, GL_FLOAT, GL_FALSE, self.modelArr.itemsize * 16, ctypes.c_void_p(0))
                glEnableVertexAttribArray(modelLoc + 1)
                glVertexAttribPointer(modelLoc + 1, 4, GL_FLOAT, GL_FALSE, self.modelArr.itemsize * 16, ctypes.c_void_p(self.modelArr.itemsize * 4))
                glEnableVertexAttribArray(modelLoc + 2)
                glVertexAttribPointer(modelLoc + 2, 4, GL_FLOAT, GL_FALSE, self.modelArr.itemsize * 16, ctypes.c_void_p(self.modelArr.itemsize * 8))
                glEnableVertexAttribArray(modelLoc + 3)
                glVertexAttribPointer(modelLoc + 3, 4, GL_FLOAT, GL_FALSE, self.modelArr.itemsize * 16, ctypes.c_void_p(self.modelArr.itemsize * 12))

                glVertexAttribDivisor(modelLoc    , 1);
                glVertexAttribDivisor(modelLoc + 1, 1);
                glVertexAttribDivisor(modelLoc + 2, 1);
                glVertexAttribDivisor(modelLoc + 3, 1);

                print(modelLoc)
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
        if node.mesh != None:
            # iterate through loaded mesh
            for i in range(len(self.meshes)):
                # if equal
                if node.mesh == self.meshes[i]:
                    # add an instance to the mesh's draw list
                    self.drawlists[i][0].append(node.transform.getModel())
                    self.drawlists[i][1].append(node.mesh.material.colour)

        # process node's children
        for child in node.chilren:
            render_node(child, worldTransform)

    def test_render(self):
        self.shader.use()
        glUniformMatrix4fv(self.shader.locations[b"view"], 1, GL_FALSE, m4_translatev(self.pos).m)
        glBindVertexArray(self.vaos[0])
        glDrawElementsInstanced(GL_TRIANGLES, self.meshes[0].geometry.indices.size, GL_UNSIGNED_INT, None, 2)
        #glDrawElements(GL_TRIANGLES, self.meshes[0].geometry.indices.size, GL_UNSIGNED_INT, None)

    # pass in world tree with all gameobjects ("scene")
    def render(self, world):
        # use shader program
        self.shader.use()
        # perspective projection
        glUniformMatrix4fv(self.shader.locations[b"proj"], 1, GL_FALSE, self.viewport.projection.m)
        glUniformMatrix4fv(self.shader.locations[b"view"], 1, GL_FALSE, mat4().translate(0, 0, -5))

        self.drawlists = [ [] for i in range(len(meshes)) ]
        # tree traversal algorithm
        # render all game objects with mesh components
        for child in world.children:
            process_node(child)

        for i in range(len(self.drawlists)):
            modelArr = self.drawlists[i][0]
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
            renderer.modelArr = np.append(m4_translate(-1, 0, 0).m, m4_translate(0, -1, 0).m)
            glBindBuffer(GL_ARRAY_BUFFER, renderer.vbos[1])
            glBufferData(GL_ARRAY_BUFFER, renderer.colourArr, GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, renderer.vbos[2])
            glBufferData(GL_ARRAY_BUFFER, renderer.modelArr, GL_STATIC_DRAW)
            print("buffer data changed")



if __name__ == "__main__":
    main()
