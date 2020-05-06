from OpenGL.GL import *
from OpenGL.GLU import *

import input
import timer
import vectors

CONST_SPEED = 5;

class camera:

    def __init__(self):
        self.pos = vectors.vec3(0, 0, -5)
        self.vAngle = 0
        self.hAngle = 0
        self.timer = timer.timer()
        self.dt = 0


    def process(self, keyboard, mouse):
        # frame time
        self.dt = self.timer.getTime(False)
        self.timer.reset()

        self.move(keyboard)
        self.look(mouse)


    def look(self, mouse):
        self.hAngle += mouse.dx
        self.vAngle += mouse.dy

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

        # make directional rather than axial
        self.pos.z += forward * self.dt * CONST_SPEED
        self.pos.x += right * self.dt * CONST_SPEED
        self.pos.y += up * self.dt * CONST_SPEED


    def set(self):
        glTranslatef(-self.pos.x, -self.pos.y, -self.pos.z) # negative for inverse
