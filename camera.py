import math

from OpenGL.GL import *
from OpenGL.GLU import *

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360

import input
import timer
import maths3d
import shaders

CONST_SPEED = 10;
MOUSE_SENS = 0.4;

class camera:

    # NOTE:
    # Camera by default starts at origin (0, 0, 0)
    # Camera by default looks towards -z direction

    def __init__(self):
        self.pos = maths3d.vec3(0, 64, 0)
        self.vAngle = 0
        self.hAngle = 0
        self.timer = timer.timer()
        self.dt = 0

        self.forward = maths3d.vec3(0, 0, -1)
        self.right = maths3d.vec3(-1, 0, 0)
        self.up = maths3d.vec3(0, 1, 0)

    def set(self, shader):
        # perspective projection matrix
        self.proj = maths3d.m4_projection(45, 0.1, 1000)

        #self.proj = maths3d.mat4()

        uni = glGetUniformLocation(shader.id, "proj")
        glUniformMatrix4fv(uni, 1, GL_TRUE, self.proj.m)
        #print("projction")
        #shaders.glErrorCheck()

        #glLoadIdentity()
        #gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 1000)

        # view matrix
        self.view = maths3d.m4_lookAt(self.pos, maths3d.v3_add(self.pos, self.forward), self.up)

        #self.view = maths3d.mat4()

        uni = glGetUniformLocation(shader.id, "view")
        glUniformMatrix4fv(uni, 1, GL_TRUE, self.view.m)

        #print("view")
        #shaders.glErrorCheck()

        #gluLookAt(0, 0, 0, self.forward.x, self.forward.y, self.forward.z, self.up.x, self.up.y, self.up.z)
        #glTranslatef(-self.pos.x, -self.pos.y, -self.pos.z) # negative for inverse


    def process(self, keyboard, mouse):
        # frame time
        self.dt = self.timer.getTime(False)
        self.timer.reset()

        self.move(keyboard)
        self.look(mouse)


    def look(self, mouse):
        self.hAngle -= self.dt * MOUSE_SENS * mouse.dx
        self.vAngle -= self.dt * MOUSE_SENS * mouse.dy
        mouse.dx = 0;
        mouse.dy = 0;

        self.forward = maths3d.vec3(
            math.cos(self.vAngle) * math.sin(self.hAngle),
            math.sin(self.vAngle),
            math.cos(self.vAngle) * math.cos(self.hAngle))

        self.right = maths3d.vec3(
            math.sin(self.hAngle - math.pi / 2),
            0,
            math.cos(self.hAngle - math.pi / 2))

        self.up = maths3d.v3_cross(self.right, self.forward)


    def move(self, keyboard):
        # keyboard movement processing
        forward = 0
        if (keyboard.keys["w"] == True and keyboard.keys["s"] != True):
            forward = 1
        elif (keyboard.keys["w"] != True and keyboard.keys["s"] == True):
            forward = -1

        right = 0
        if (keyboard.keys["d"] == True and keyboard.keys["a"] != True):
            right = 1
        elif (keyboard.keys["d"] != True and keyboard.keys["a"] == True):
            right = -1

        up = 0
        if (keyboard.keys["SPACE"] == True and keyboard.keys["LCTRL"] != True):
            up = 1
        elif (keyboard.keys["SPACE"] != True and keyboard.keys["LCTRL"] == True):
            up = -1

        self.pos = maths3d.v3_add(self.pos, maths3d.v3_mulf(self.forward, self.dt * CONST_SPEED * forward))
        self.pos = maths3d.v3_add(self.pos, maths3d.v3_mulf(self.right, self.dt * CONST_SPEED * right))
        self.pos = maths3d.v3_add(self.pos, maths3d.v3_mulf(self.up, self.dt * CONST_SPEED * up))
