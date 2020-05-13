import math

from OpenGL.GL import *
from OpenGL.GLU import *

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360

import input
import timer
from maths3d import *
import shaders

CONST_SPEED = 20;
MOUSE_SENS = 0.4;

class camera:

    # NOTE:
    # Camera by default starts at origin (0, 0, 0)
    # Camera by default looks towards -z direction

    def __init__(self):
        self.pos = .vec3(0, 70, 0)
        self.vAngle = 0
        self.hAngle = 0
        self.timer = timer.timer()
        self.dt = 0

        self.forward = vec3(0, 0, -1)
        self.right = vec3(-1, 0, 0)
        self.up = vec3(0, 1, 0)

        self.view = mat4()


    def process(self, keyboard, mouse):
        # frame time
        self.dt = self.timer.getTime(False)
        self.timer.reset()

        self.move(keyboard)
        self.look(mouse)

        # make update
        look = m4_lookAt(self.pos, v3_add(self.forward, self.pos), vec3(0, 1, 0))
        translate = m4_translate(-self.pos.x, -self.pos.y, -self.pos.z)
        self.view = m4_mul(translate, look)


    def look(self, mouse):
        # mouse movement processing
        self.hAngle -= self.dt * MOUSE_SENS * mouse.dx
        self.vAngle -= self.dt * MOUSE_SENS * mouse.dy
        mouse.dx = 0;
        mouse.dy = 0;

        self.forward = vec3(
            math.cos(self.vAngle) * math.sin(self.hAngle),
            math.sin(self.vAngle),
            math.cos(self.vAngle) * math.cos(self.hAngle))

        self.right = vec3(
            math.sin(self.hAngle - math.pi / 2),
            0,
            math.cos(self.hAngle - math.pi / 2))

        self.up = v3_cross(self.right, self.forward)


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

        self.pos = v3_add(self.pos, v3_mulf(self.forward, self.dt * CONST_SPEED * forward))
        self.pos = v3_add(self.pos, v3_mulf(self.right, self.dt * CONST_SPEED * right))
        self.pos = v3_add(self.pos, v3_mulf(self.up, self.dt * CONST_SPEED * up))
