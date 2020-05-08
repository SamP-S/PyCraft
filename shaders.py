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
        vs = self.vertex()
        fs = self.fragment()
        self.id = self.program(vs, fs)
        glUseProgram(self.id)

    def create(self, type, source):
        shader = glCreateShader(type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        glShaderErrorCheck(shader)
        return shader

    def program(self, vs, fs):
        program = glCreateProgram()
        glAttachShader(program, vs)
        glAttachShader(program, fs)
        glBindFragDataLocation(program, 0, "fragColour");
        glLinkProgram(program)
        glLinkErrorCheck(program)
        return program

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
            gl_Position = proj * view * modelBlock * modelChunk * vec4(position, 1.0);
            gl_Position = vec4(position, 1);
        }
        """
        id = self.create(GL_VERTEX_SHADER, v)
        return id

    def fragment(self):
        f = """
        #version 330
        in vec4 solidColour;
        out vec4 fragColour;
        void main()
        {
            fragColour = vec4(1, 1, 1, 1);
        }
        """
        id = self.create(GL_FRAGMENT_SHADER, f)
        return id
