import numpy as np
from random import random

def perlin(x,y,seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi]+yi],xf,yf)
    n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = gradient(p[p[xi+1]+yi],xf-1,yf)
    # combine noises
    x1 = linearInterpolation(n00,n10,u)
    x2 = linearInterpolation(n01,n11,u)
    return linearInterpolation(x1,x2,v)

def linearInterpolation(a,b,x):
    return a + x * (b-a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h,x,y):
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h % 4]
    return g[:,:,0] * x + g[:,:,1] * y


def getPerlinIMG(seed):
    n = 16
    range = 8
    lin = np.linspace(0, range, n, endpoint=False)
    x,y = np.meshgrid(lin,lin)
    return perlin(x, y, seed)


def getPerlinVal(i, j, seed):
    img = getPerlinIMG(seed)
    return img[i][j]


"""

#%matplotlib inline
import matplotlib.pyplot as plt

def main():
    n = 16
    range = 8
    lin = np.linspace(0, range, n, endpoint=False)
    x,y = np.meshgrid(lin,lin)
    img = perlin(x,y,seed=2)

    plt.imshow(img, origin='lower')
    plt.show()


if __name__ == "__main__":
    main()
"""