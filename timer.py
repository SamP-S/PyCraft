import time

class timer:

    def __init__(self):
        self.start = time.time()
        #print("init timer")

    def start(self):
        self.reset()

    def reset(self):
        self.start = time.time()

    def getTime(self, isMilliseconds = True):
        t = time.time() - self.start
        if isMilliseconds:
            return t * 1000
        else:
            return t

    def print(self):
        print(self.getTime())
