from maths3d import *


class transform:

    def __init__(self, pos=vec3(), rotation=vec3(), scale=vec3()):
        self.pos = pos
        self.rotation = rotation
        self.scale = scale


class game_object:

    def __init__(self, name="game_object", parent):
        self.transform = transform()
        self.name = name
        self.parent = parent
        self.children = []
