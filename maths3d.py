import math
import numpy as np

# class definitions (data structures)
class vec3:

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

class mat4:

    def __init__(self):
        self.m = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32)


# vec3 functions
def v3_add(a, b):
    return vec3(a.x + b.x, a.y + b.y, a.z + b.z)

def v3_addf(a, b):
    return vec3(a.x + b, a.y + b, a.z + b)

def v3_sub(a, b):
    return vec3(a.x - b.x, a.y - b.y, a.z - b.z)

def v3_subf(a, b):
    return vec3(a.x - b, a.y - b, a.z - b)

def v3_mul(a, b):
    return vec3(a.x * b.x, a.y * b.y, a.z * b.z)

def v3_mulf(a, b):
    return vec3(a.x * b, a.y * b, a.z * b)

def v3_normalise(v):
    tmp = math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
    return vec3(v.x / tmp, v.y / tmp, v.z / tmp)

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


# mat4 functions
def m4_translate(x, y, z):
    m = mat4()
    m.m[3,0] = x
    m.m[3,1] = y
    m.m[3,2] = z
    return m

def m4_translatev(v):
    return m4_translate(v.x, v.y, v.z)

def m4_scale(x, y, z):
    m = mat4()
    m.m[0,0] = x
    m.m[1,1] = y
    m.m[2,2] = z
    return m

def m4_scalev(v):
    return m4_scale(v.x, v.y, v.z)

def m4_mul(a, b):
    m = mat4()
    m.m = np.matmul(a.m, b.m)
    return m

if False: # comments out
    def m4_lookAt(eye=vec3(0.0, 0.0, 0.0), to=vec3(0.0, 0.0, -1.0), tmp=vec3(0.0, 1.0, 0.0)):
        forward = v3_normalise(v3_sub(to, eye))
        right = v3_cross(forward, v3_normalise(tmp))
        up = v3_cross(v3_normalise(right), forward)
        m = mat4()
        m.m[0,0] = right.x
        m.m[0,1] = right.y
        m.m[0,2] = right.z
        m.m[1,0] = up.x
        m.m[1,1] = up.y
        m.m[1,2] = up.z
        m.m[2,0] = -forward.x
        m.m[2,1] = -forward.y
        m.m[2,2] = -forward.z
        #print(m.m)
        return m

if True:
    def m4_lookAt(eye=vec3(0.0, 0.0, 0.0), to=vec3(0.0, 0.0, -1.0), tmp=vec3(0.0, 1.0, 0.0)):
        forward = v3_normalise(v3_sub(to, eye))
        right = v3_cross(forward, v3_normalise(tmp))
        up = v3_cross(v3_normalise(right), forward)
        m = mat4()
        m.m[0,0] = right.x
        m.m[0,1] = up.x
        m.m[0,2] = -forward.x
        m.m[1,0] = right.y
        m.m[1,1] = up.y
        m.m[1,2] = -forward.y
        m.m[2,0] = right.z
        m.m[2,1] = up.z
        m.m[2,2] = -forward.z
        #print(m.m)
        return m

if False:
    def m4_lookAt(forward, right, up):
        m = mat4()
        m.m[0,0] = right.x
        m.m[0,1] = right.y
        m.m[0,2] = right.z
        m.m[1,0] = up.x
        m.m[1,1] = up.y
        m.m[1,2] = up.z
        m.m[2,0] = -forward.x
        m.m[2,1] = -forward.y
        m.m[2,2] = -forward.z
        #print(m.m)
        return m


def m4_perspective(fov=45, aspect=(16/9), near=0.1, far=1000):
    m = mat4()
    f = 1 / math.tan(math.radians(fov) / 2  )
    m.m[0,0] = f / aspect
    m.m[1,1] = f

    m.m[2,2] = (far + near) / (near - far)
    m.m[2,3] = -1

    m.m[3,2] = 2 * far * near / (near - far)
    m.m[3,3] = 0
    #print(m.m)
    return m
