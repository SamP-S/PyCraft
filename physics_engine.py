from enum import IntEnum


################################################################################
# COLLIDERS

class COLLIDER(IntEnum):
    BASE = 0
    BOX = 1
    SPHERE = 2

class collider:

    def __init(self, parent=None):
        # if true, then physics will no longer physics and only raise collision events
        self.isTrigger = False
        # easy way to disable the collider if ya want
        self.isEnabled = False
        # set with physics material to determine how physics objects interact:
        # 1. bouciness (e)
        # 2. static friction
        # 3. dynamic friction
        self.material = None
        self.type = COLLIDER.BASE
        self.parent

    # collision events
    def onCollisionEnter(self):
        None
    def onCollisionExit(self):
        None
    def onCollisionStay(self):
        None

    # trigger events
    def onTriggerEnter(self):
        None
    def onTriggerExit(self):
        None
    def onTriggerStay(self):
        None

class box_collider(collider):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.type = COLLIDER.BOX
        self.isEnabled = True

class sphere_collider(collider):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.type = COLLIDER.SPHERE
        self.isEnabled = True

################################################################################
# ENGINE

class physics_engine:

    def __init__(self):
        print("init physics")
        
    def raycast(self, origin, direction, length=-1):
        None
