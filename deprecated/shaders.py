<<<<<<< HEAD:shaders.py
from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GLU import *


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

        self.attribs = [b"position"]
        self.locations = dict((k, v) for (v, k) in enumerate(self.attribs))
        self.uniforms = [b"proj", b"view", b"modelChunk", b"modelBlock", b"colour"]

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


    #locations = {}
    #uniforms = [b"model", b"view", b"proj", b"colour"]

    def use(self):
        #for uniform in self.uniforms:
        #    self.locations[uniform] = glGetUniformLocation(self.id, uniform)
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
=======
from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
from OpenGL.GLU import *


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


    #locations = {}
    #uniforms = [b"model", b"view", b"proj", b"colour"]

    def use(self):
        #for uniform in self.uniforms:
        #    self.locations[uniform] = glGetUniformLocation(self.id, uniform)
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
>>>>>>> 1cf19361f5e172955bd752744e6c7c8b6d39a767:deprecated/shaders.py
