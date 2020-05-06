import math

def v3_add(a, b):
    return vec3(a.x + b.x, a.y + b.y, a.z + b.z)

def v3_addf(a, b):
    return vec3(a.x + b, a.y + b, a.z + b)

def v3_mul(a, b):
    return vec3(a.x * b.x, a.y * b.y, a.z * b.z)

def v3_mulf(a, b):
    return vec3(a.x * b, a.y * b, a.z * b)

def v3_cross(a, b):
    x = m2_determinant(a.y, a.z, b.y, b.z)
    y = -m2_determinant(a.x, a.z, b.x, b.z)
    z = m2_determinant(a.x, a.y, b.x, b.y)
    return vec3(x, y, z)

# determinant
#   a b
#   c d
def m2_determinant(a, b, c, d):
    return a * d - b * c

class vec3:

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
