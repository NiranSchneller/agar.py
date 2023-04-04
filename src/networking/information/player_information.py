


class PlayerInformation:
    def __init__(self, x, y, radius, name, id=""):
        self.x = x
        self.y = y
        self.radius = radius
        self.name = name
        self.id = id


    def set_information(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.radius == other.radius and self.name == other.name