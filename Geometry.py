import numpy as np

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

cubeIndicies = np.array([   0, 1, 5, 5, 4, 0,   # left
                            2, 3, 7, 7, 6, 2,   # right
                            0, 3, 2, 2, 1, 0,   # bottom
                            4, 5, 6, 6, 7, 4,   # top
                            3, 0, 4, 4, 7, 3,   # back
                            1, 2, 6, 6, 5, 1],  # front
                            dtype=np.uint32)

# indicie data for drawing individual faces from triangles
cubeFaceIndicies = np.array([   [0, 1, 5, 5, 4, 0],     # left
                                [2, 3, 7, 7, 6, 2],     # right
                                [0, 3, 2, 2, 1, 0],     # bottom
                                [4, 5, 6, 6, 7, 4],     # top
                                [3, 0, 4, 4, 7, 3],     # back
                                [1, 2, 6, 6, 5, 1]],    # front
                                dtype=np.uint32)

# indicie data for drawing individual faces from lines
cubeLineIndicies = np.array([   [0, 1, 1, 5, 5, 4, 4, 0],     # left
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

playerIndicies = np.array([ 0, 1, 5, 5, 4, 0,   # left
                            2, 3, 7, 7, 6, 2,   # right
                            0, 3, 2, 2, 1, 0,   # bottom
                            4, 5, 6, 6, 7, 4,   # top
                            3, 0, 4, 4, 7, 3,   # back
                            1, 2, 6, 6, 5, 1],  # front
                            dtype=np.uint32)
