import numpy as np
from enum import IntEnum


class RENDER(IntEnum):
    NONE = 0
    ARRAYS = 1
    ARRAYS_INSTANCED = 2
    ELEMENTS = 3
    ELEMENTS_INTANCED = 4


################################################################################
# MATERIALS

class MATERIALS(IntEnum):
    NONE = 0
    SOLID_COLOUR = 1
    TEXTURED = 2


class material:

    def __init__(self, id=-1, name="material", type=MATERIALS.NONE):
        self.id = -1
        self.name = name
        self.type = type


class solid_material(material):

    def __init__(self, id=-1, name="solid colour material", type=MATERIALS.SOLID_COLOUR, colour=[0.8, 0.8, 0.8, 1.0]):
        super().__init__(id, name, type)
        self.colour = colour


################################################################################
# MESH

class instances:

    def __init__(self):
        # store as np arrays for 2 reasons:
        # 1. its the usable format for vbos
        # 2. can be used for both non-instanced and instanced rendering
        self.game_object_ids = np.array([], dtype=np.int32)
        self.model_projections = np.array([], dtype=np.float32)
        self.colours = np.array([], dtype=np.float32)

class mesh_data:

    def __init__(self, id=-1, name="mesh_data", vertices=None, indices=None):
        self.id = id
        self.name = name
        self.vertices = vertices
        self.indices = indices

class mesh:

    def __init__(self, id=-1, name="base_mesh", data=-1, mode=RENDER.NONE):
        self.id = id
        self.name = name
        self.data = data
        self.mode = mode
        if mode == RENDER.ARRAYS_INSTANCED or mode == RENDER.ELEMENTS_INTANCED:
            self.instances = instances()
        else:
            self.instances = None


################################################################################
## Remove ?
class model:

    def __init__(self, id=-1, name="model", mesh_id=None, material_id=None):
        self.id = id
        self.name = name
        self.mesh_id = mesh_id
        self.material_id = material_id
        self.mode = mode


################################################################################


# cube geometry data for blocks
cubeVertices = np.array([   0.0, 0.0, 0.0,
                            0.0, 0.0, 1.0,
                            1.0, 0.0, 1.0,
                            1.0, 0.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 1.0,
                            1.0, 1.0, 1.0,
                            1.0, 1.0, 0.0],
                            dtype=np.float32)

cubeIndices = np.array([   0, 1, 5, 5, 4, 0,   # left
                            2, 3, 7, 7, 6, 2,   # right
                            0, 3, 2, 2, 1, 0,   # bottom
                            4, 5, 6, 6, 7, 4,   # top
                            3, 0, 4, 4, 7, 3,   # back
                            1, 2, 6, 6, 5, 1],  # front
                            dtype=np.uint32)

# indicie data for drawing individual faces from triangles
cubeFaceIndices = np.array([   [0, 1, 5, 5, 4, 0],     # left
                                [2, 3, 7, 7, 6, 2],     # right
                                [0, 3, 2, 2, 1, 0],     # bottom
                                [4, 5, 6, 6, 7, 4],     # top
                                [3, 0, 4, 4, 7, 3],     # back
                                [1, 2, 6, 6, 5, 1]],    # front
                                dtype=np.uint32)

# indicie data for drawing individual faces from lines
cubeLineIndices = np.array([   [0, 1, 1, 5, 5, 4, 4, 0],     # left
                                [2, 3, 3, 7, 7, 6, 6, 2],     # right
                                [0, 3, 3, 2, 2, 1, 1, 0],     # bottom
                                [4, 5, 5, 6, 6, 7, 7, 4],     # top
                                [3, 0, 0, 4, 4, 7, 7, 3],     # back
                                [1, 2, 2, 6, 6, 5, 5, 1]],    # front
                                dtype=np.uint32)

################################################################################

# player geometry data
# same as cube except y is double
playerVertices = np.array([ 0.0, 0.0, 0.0,   0.0, 0.0, 1.0,
                            1.0, 0.0, 1.0,   1.0, 0.0, 0.0,
                            0.0, 2.0, 0.0,   0.0, 2.0, 1.0,
                            1.0, 2.0, 1.0,   1.0, 2.0, 0.0],
                            dtype=np.float32)

playerIndices = np.array([ 0, 1, 5, 5, 4, 0,   # left
                            2, 3, 7, 7, 6, 2,   # right
                            0, 3, 2, 2, 1, 0,   # bottom
                            4, 5, 6, 6, 7, 4,   # top
                            3, 0, 4, 4, 7, 3,   # back
                            1, 2, 6, 6, 5, 1],  # front
                            dtype=np.uint32)
