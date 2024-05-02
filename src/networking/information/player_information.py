


class PlayerInformation:
    def __init__(self, x: int, y: int, radius: float, name: str, id: str = ""):
        self.x: int = x
        self.y: int = y
        self.radius: float = radius
        self.name: str = name
        self.id: str = id


    def set_information(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.radius == other.radius and self.name == other.name