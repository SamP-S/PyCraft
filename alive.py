from camera import *

class alive:

    def __init__(self, pos):
         self.pos = pos

class player(alive):

    def __init__(self, pos, camera):
        super().__init__(pos)
        self.camera = camera()
