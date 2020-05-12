import maths3d

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360
FOV = 45
Z_NEAR = 0.1
Z_FAR = 100

class RenderEngine:

    settings = {
        "fov" : FOV,
        "resolution" : { "width" : WINDOW_WIDTH, "height" : WINDOW_HEIGHT }
    }

    def __init__(self):
        w = self.settings.get("resolution").get("width")
        h = self.settings.get("resolution").get("height")
        aspect =  w / h
        self.projection = maths3d.m4_perspective(45, aspect, Z_NEAR, Z_FAR)

    # pass in world tree with all gameobjects ("scene")
    def render(world):
        print("render engine render call")
