import pygame
from pygame.locals import *

class mouse:

    buttons = {
    "mouse1" : False,   # LMB
    "mouse2" : False,   # RMB
    "mouse3" : False,   # MMB
    "mouse4" : False,   # Page Up
    "mouse5" : False    # Page Down
    }

    def __init__(self):
        self.dx = 0;
        self.dy = 0;

    def processMotion(self, event):
        self.dx = event.rel[0]
        self.dy = event.rel[1]

    def processButton(self, event):
        state = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            state = True

        if event.button == 1:
            self.buttons["mouse1"] = state
        elif event.button == 2:
            self.buttons["mouse2"] = state
        elif event.button == 3:
            self.buttons["mouse3"] = state
        elif event.button == 4:
            self.buttons["mouse4"] = state
        elif event.button == 5:
            self.buttons["mouse5"] = state


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
        print("keyboard init")

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
