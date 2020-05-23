from math import *

class vec2:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def print(self):
        print("vec3: x", self.x, " y", self.y)

def v2_mul(v, f):
    return vec2(v.x *f, v.y * f)

def v2_normalise(a):
    d = sqrt(a.x * a.x + a.y * a.y)
    return vec2(a.x / d, a.y / d)

def v2_tangent(v):
    return vec2(-v.y, v.x)

def dot(a, b):
    return a.x * b.x + a.y * b.y

def v2_direction(a, b):
    return vec2(b.x - a.x, b.y - a.y)

def project(vertices, axis):
    dots = [ dot(vertex, axis) for vertex in vertices]
    return vec2(min(dots), max(dots))

def contains(n, range):
    a = range.x
    b = range.y
    if b < a:
        a = range.y
        b = range.x
    return (n >= a) and (n <= b);

def overlap(a, b):
    if contains(a.x, b):
        return True;
    if contains(a.y, b):
        return True;
    if contains(b.x, a):
        return True;
    if contains(b.y, a):
        return True;
    return False;


class transform:

    def __init__(self):
        self.pos = vec2()
        self.rot = 0
        self.scl = vec2()

    def set_pos(self, x, y):
        self.pos = vec2(x, y)

    def set_rot(self, angle):
        self.rot = angle

    def set_scl(self, x, y):
        self.scl = vec2(x, y)


class square:

    def __init__(self):
        self.t = transform()
        self.points = []
        self.update_points()

    def update_points(self):
        self.points = [
            vec2(0.5 * cos(radians(self.t.rot)), 0.5 * sin(radians(self.t.rot))),
            vec2(0.5 * cos(radians(self.t.rot + 90)), 0.5 * sin(radians(self.t.rot + 90))),
            vec2(0.5 * cos(radians(self.t.rot + 180)), 0.5 * sin(radians(self.t.rot + 180))),
            vec2(0.5 * cos(radians(self.t.rot + 270)), 0.5 * sin(radians(self.t.rot + 270)))
        ]
        for i in range(len(self.points)):
            self.points[i].x += self.t.pos.x
            self.points[i].y += self.t.pos.y

    def get_edges(self):
        return [ v2_direction(self.points[i], self.points[i + 2]) for i in range(int(len(self.points) / 2))]

a = square()
b = square()
b.t.set_pos(0.8, 1.8)
b.update_points()


# check if a is colliding with b
def check_collision(a, b):
    # x-axis "relative to original orientation"  dir = (1, 0)
    # SOHCAHTOA

    vertices_a = a.points
    vertices_b = b.points

    edges_a = a.get_edges()
    edges_b = b.get_edges()

    edges = edges_a + edges_b

    axes = [v2_normalise(v2_tangent(edge)) for edge in edges]

    print("edges")
    for edge in edges:
        edge.print()

    print("axes")
    for axis in axes:
        axis.print()

    for i in range(len(axes)):
        projection_a = project(vertices_a, axes[i])
        projection_a.print()
        projection_b = project(vertices_b, axes[i])
        projection_b.print()
        overlapping = overlap(projection_a, projection_b)
        if not overlapping:
            return False
    return True



print(check_collision(a, b))
