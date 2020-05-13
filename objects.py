from maths3d import *


class object:

    def __init__(self, name="object", parent=None):
        self.name = name
        self.parent = parent
        self.children = []


class transform:

    def __init__(self, pos=vec3(), rot=vec3(), scl=vec3()):
        self.position = pos
        self.rotation = rot
        self.scale = scl

    def getModel(self):
        return m4_translatev(self.position).m


class game_object(object):

    def __init__(self, name="game_object", parent=None, transform=transform()):
        super().__init__(name, parent)
        self.transform = transform
