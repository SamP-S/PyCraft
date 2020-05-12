
import noise

# the world is the root node of the "scene"
# must contain additional data about the world:
# seed
# noise type

class world:

    def __init__(self, seed=2, noise=noise.NOISE.PERLIN):
        print("init world")
        self.children = []
        self.seed = 2
        self.noise = noise
