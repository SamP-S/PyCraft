from OpenGL.GL import *
from OpenGL.GLU import *

import input
import timer
import vectors

class camera:

    def __init__(self):
        self.pos = vectors.vec3(0, 0, -5)
        self.vAngle = 0
        self.hAngle = 0
        self.timer = timer.timer()

    def set(self):
        glTranslatef(-self.pos.x, -self.pos.y, -self.pos.z) # negative for inverse