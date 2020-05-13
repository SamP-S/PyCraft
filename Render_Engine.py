from maths3d import *
from mesh import *

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360
FOV = 45
Z_NEAR = 0.1
Z_FAR = 100

from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GLU import *

import numpy as np

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


class instance_mesh:

    def __init__(self, mesh=None):
        self.mesh = mesh

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.mesh.geometry.vertices, GL_STATIC_DRAW)
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.mesh.geometry.indices, GL_STATIC_DRAW)


class shader:

    def __init__(self):
        self.attribs = [b"position"]
        self.locations = dict((k, v) for (v, k) in enumerate(self.attribs))
        self.uniforms = [b"proj", b"view", b"model", b"colour"]

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

        uniform mat4 modelChunk;
        uniform mat4 modelBlock;
        uniform mat4 view;
        uniform mat4 proj;

        uniform mat4 cameraModel;

        uniform vec4 colour;

        out vec4 solidColour;

        void main()
        {
            solidColour = colour;
            gl_Position = proj * view * modelChunk * modelBlock * vec4(position, 1.0);
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
        w = self.viewport.resolution.width
        h = self.viewport.resolution.height
        aspect = w / h
        self.projection = m4_perspective(self.fov, aspect, self.Z_NEAR, self.Z_FAR)


class render_engine:

    def __init__(self):
        self.viewport = viewport()
        self.shader = shader()

        # list of loaded meshes
        self.meshes = []
        self.load_meshes()

        # list of all cameras
        self.cameras = []

        # list of lists of each mesh instance by mesh
        self.drawlists = [ [[], []] for i in range(len(meshes)) ]

    def load_meshes():
        print("load meshes")
        # for each mesh in mesh folder
        # load geometry
        # load material
        # add to list

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

    # pass in world tree with all gameobjects ("scene")
    def render(world):
        # use shader program
        self.shader.use()
        # perspective projection
        glUniformMatrix4fv(shader.locations[b"proj"], 1, GL_FALSE, self.viewport.projection.m)
        glUniformMatrix4fv(shader.locations[b"view"], 1, GL_FALSE, mat4().m)

        self.drawlists = [ [] for i in range(len(meshes)) ]
        # tree traversal algorithm
        # render all game objects with mesh components
        for child in world.children:
            process_node(child)

        for i in range(len(self.drawlists)):
