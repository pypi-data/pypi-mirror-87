class Dual:

    def __init__(self, name):  # name, eyes or ears
        self.path = "body.head." + name
        self.right = self.path + ".right"
        self.left = self.path + ".left"

    def __repr__(self):
        return self.path


class Head:
    eyes = Dual("eyes")
    ears = Dual("ears")

    def __str__(self):
        return "body.head"


class Limb:

    def __init__(self, name, side):
        self.path = "body." + name + "." + side
        self.upper = self.path + ".upper"
        self.lower = self.path + ".lower"
        self.hand = self.path + ".hand"

    def __repr__(self):
        return self.path


class Arms:
    leftArm = Limb("arm", "left")
    rightArm = Limb("arm", "right")

    def __repr__(self):
        return "body.arms"


class Legs:
    leftLeg = Limb("leg", "left")
    rightLeg = Limb("leg", "right")

    def __repr__(self):
        return "body.legs"


class Body:
    head = Head()
    arms = Arms()
    torso = "body.torso"
    tail = "body.tail"

    def __repr__(self):
        return "body"
