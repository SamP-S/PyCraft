import pygame
from pygame.locals import *

class keyboard:

    keys = {
    "Q" : False,
    "W" : False,
    "E" : False,
    "R" : False,
    "T" : False,
    "Y" : False,
    "U" : False,
    "I" : False,
    "O" : False,
    "P" : False,

    "A" : False,
    "S" : False,
    "D" : False,
    "F" : False,
    "G" : False,
    "H" : False,
    "J" : False,
    "K" : False,
    "L" : False,

    "Z" : False,
    "X" : False,
    "C" : False,
    "V" : False,
    "B" : False,
    "N" : False,
    "M" : False,

    "SPACE" : False,
    "TAB" : False,
    "LSHIFT" : False,
    "LCTRL" : False,
    "ESC" : False
    }

    def __init__(self):
        print("keyboard init")

    def processEvent(self, event):
        if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP:
            return

        #print(event)

        state = False
        if event.type == pygame.KEYDOWN:
            state = True

        for i in range(26):
            keycode = ord('a') + i
            if event.key == keycode:
                self.keys[chr(keycode)] = state
                print(chr(keycode), "                    ", state)
                return

        if event.key == 32:
            self.keys["SPACE"] = state
        elif event.key == 27:
            self.keys["ESC"] = state
        else:
            print(event)



    def processEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                for key in self.keys:
                    print(key)
