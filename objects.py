from maths3d import *


class script:

    def __init__(self, parent=None):
        self.parent = parent

    def start(self):
        None

    def update(self):
        None


class object:

    def __init__(self, id=-1, name="object", parent=None):
        self.id = id
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

    def __init__(self, id=-1, name="game_object", parent=None, transform=transform(), scripts=[]):
        super().__init__(id, name, parent)
        self.transform = transform
        self.scripts = scripts
        self.mesh = None
        self.material = None
        self.camera = None
        self.start()

    def start(self):
        for script in self.scripts:
            script.start()

    def update(self):
        for script in self.scripts:
            script.update()
