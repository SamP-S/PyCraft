
class keyboard:

    keys = {
    "q" : False,
    "w" : False,
    "e" : False,
    "r" : False,
    "t" : False,
    "y" : False,
    "u" : False,
    "i" : False,
    "o" : False,
    "p" : False,

    "a" : False,
    "s" : False,
    "d" : False,
    "f" : False,
    "g" : False,
    "h" : False,
    "j" : False,
    "k" : False,
    "l" : False,

    "z" : False,
    "x" : False,
    "c" : False,
    "v" : False,
    "b" : False,
    "n" : False,
    "m" : False,

    "SPACE" : False,
    "TAB" : False,
    "LSHIFT" : False,
    "LCTRL" : False,
    "ESC" : False
    }

    def __init__(self):
        print("init keyboard")

    def processKey(self, event):
        if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP:
            return

        state = False
        if event.type == pygame.KEYDOWN:
            state = True

        for i in range(26):
            keycode = ord('a') + i
            if event.key == keycode:
                self.keys[chr(keycode)] = state
                return

        if event.key == pygame.K_SPACE:
            self.keys["SPACE"] = state
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
            #self.keys["ESC"] = state
        elif event.key == pygame.K_LCTRL:
            self.keys["LCTRL"] = state
        elif event.key == pygame.K_LSHIFT:
            self.keys["LSHIFT"] = state
        else:
            print(event)
