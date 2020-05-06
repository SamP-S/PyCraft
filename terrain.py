from random import random
print("terrain.py")

CONST_WIDTH = 2
CONST_DEPTH = 2
CONST_HEIGHT = 1

class chunk:

    def __init__(self):
        self.data = [[[0 for i in range(CONST_WIDTH)] for j in range(CONST_HEIGHT)] for k in range(CONST_DEPTH)]
        self.generate()

    def generate(self):
        for k in range(CONST_DEPTH):
            for j in range(CONST_HEIGHT):
                for i in range(CONST_WIDTH):
                    self.data[k][j][i] = random()

    def print(self):
        for k in range(CONST_DEPTH):
            print ()
            for j in range(CONST_HEIGHT):
                print()
                for i in range(CONST_WIDTH):
                    print(self.data[k][j][i])

def main():
    print("terrain.py main")
    c = chunk()
    c.print()

if __name__ == "__main__":
    main()
