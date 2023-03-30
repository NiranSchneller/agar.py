


class PlayerInformation:
    def __init__(self, x, y, radius, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.name = name


    def set_information(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __str__(self):
        return f'name:{self.name},x:{self.x},y:{self.y},radius:{self.radius}'

    def __repr__(self):
        return f'name:{self.name},x:{self.x},y:{self.y},radius:{self.radius}'