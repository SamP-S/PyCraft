
class mouse:

    buttons = {
    "mouse1" : False,   # LMB
    "mouse2" : False,   # RMB
    "mouse3" : False,   # MMB
    "mouse4" : False,   # Page Up
    "mouse5" : False    # Page Down
    }

    def __init__(self):
        print("init mouse")
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
