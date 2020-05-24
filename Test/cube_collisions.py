from math import *

class vec3:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def print(self):
        print("vec3: x", self.x, " y", self.y, " z", self.z)

def v3_mul(v, f):
    return vec3(v.x *f, v.y * f, v.z * f)

def v3_normalise(a):
    d = sqrt(a.x * a.x + a.y * a.y + a.z * a.z)
    return vec3(a.x / d, a.y / d, a.z / d)

##### REDO
def v3_tangent(v):
    return vec3(-v.y, v.x)

def v3_dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z

def v3_direction(a, b):
    return vec3(b.x - a.x, b.y - a.y, b.z - a.z)

def project(vertices, axis):
    dots = [ v3_dot(vertex, axis) for vertex in vertices]
    return vec2(min(dots), max(dots))

###### REDO
def contains(n, range):
    a = range.x
    b = range.y
    c = range.z
    if b < a:
        a = range.y
        b = range.x
    return (n >= a) and (n <= b)

def overlap(a, b):
    if contains(a.x, b):
        return True
    if contains(a.y, b):
        return True
    if contains(a.z, b):
        return True
    if contains(b.x, a):
        return True
    if contains(b.y, a):
        return True
    if contains(b.z, a):
        return True
    return False


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


class cube:

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
            self.points[i].z += self.t.pos.z

###### REDO
    def get_edges(self):
        return [ v3_direction(self.points[i], self.points[i + 2]) for i in range(int(len(self.points) / 2))]

a = square()
b = square()
b.t.set_pos(0.8, 1.8, 0.0)
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

    axes = [v3_normalise(v3_tangent(edge)) for edge in edges]

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
