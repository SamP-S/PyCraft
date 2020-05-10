
playerVertices = np.array([ 0.0, 0.0, 0.0,   0.0, 0.0, 1.0,
                            1.0, 0.0, 1.0,   1.0, 0.0, 0.0,
                            0.0, 2.0, 0.0,   0.0, 2.0, 1.0,
                            1.0, 2.0, 1.0,   1.0, 2.0, 0.0],
                            dtype=np.float32)

playerIndicies = np.array([ [0, 1, 5, 5, 4, 0],     # left
                            [2, 3, 7, 7, 6, 2],     # right
                            [0, 3, 2, 2, 1, 0],     # bottom
                            [4, 5, 6, 6, 7, 4],     # top
                            [3, 0, 4, 4, 7, 3],     # back
                            [1, 2, 6, 6, 5, 1]],    # front
                            dtype=np.uint32)

class alive:

    def __init__(self, pos):
         self.pos = pos

class person(alive):

    def __init__(self, pos, camera):
        super().__init__(pos)
        self.camera = camera
