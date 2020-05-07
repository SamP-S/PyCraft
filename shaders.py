from OpenGL.GL import shaders as glShaders
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray

from OpenGL.GLU import *

def glErrorCheck():
    error = glGetError()
    if error != GL_NO_ERROR:
        print("OPENGL_ERROR: ", gluErrorString(error))

def glProgramErrorCheck():
    print("do this")

def glShaderErrorLog(shader):
    err = GLuint(0)
    glGetShaderiv(shader, GL_COMPILE_STATUS, err);
    print("Shader COMPILE STATUS: ", err)
    print(GL_FALSE)
    if err == GL_FALSE:
        maxLength = GLuint(0)
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, maxLength)
        log = []
        length = GLuint(0)
        glGetShaderInfoLog(shader, maxLength, length,  log)
        print(log)

class shader:

    def create(type, source):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(shader))
        return shader


    def vertex(self):
        id = glCreateShader(GL_VERTEX_SHADER)
        v = """
        #version 330
        layout(location = 0) in vec3 position;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 proj;

        uniform vec4 colour;

        out vec4 solidColour;

        void main()
        {
            solidColour = colour;
            gl_Position = proj * view * model * vec4(position, 1.0);
        }
        """
        id = glShaders.compileShader(v, GL_VERTEX_SHADER)
        glShaderErrorLog(id)
        return id

    def fragment(self):
        id = glCreateShader(GL_FRAGMENT_SHADER)
        f = """
        #version 330
        in vec4 solidColour;
        out vec4 fragColour;
        void main()
        {
            fragColour = solidColour;
        }
        """
        id = glShaders.compileShader(f, GL_FRAGMENT_SHADER)
        glShaderErrorLog(id)

        return id

    def __init__(self):
        locations = []
        uniforms = []

        program = glCreateProgram()
        glAttachShader(program, vert_shader)
        glAttachShader(program, frag_shader)
        glLinkProgram(program)
        if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(program))
        for uniform in uniforms:
            locations[uniform] = glGetUniformLocation(program, uniform)
        glUseProgram(program)

    def use(self):
        glUseProgram(self.id)

    def print(self):
        print(self.id)
