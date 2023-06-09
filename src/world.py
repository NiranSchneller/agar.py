
"""
    Represents the world, all edibles and players
"""
import random

from src.constants import EdibleConstants, PlatformConstants
from src.edible import Edible





class World:

    def __init__(self, width, height):
        self.edibles = []
        self.players = []
        self.width = width
        self.height = height

    def spawn_edibles(self, amount):
        for i in range(amount):
            self.edibles.append(self.spawn_edible(EdibleConstants.EDIBLE_RADIUS, EdibleConstants.EDIBLE_COLOR))

    def spawn_edible(self, radius, color):
        return Edible(random.randint(radius, self.width - radius),
                      random.randint(radius, self.height - radius), color)

    """
        Deletes edible
        returns new edible that has spawned in the world
    """
    def delete_edible(self, edible):
        # eq overridden in edible class
        self.edibles.remove(edible)
        new_edible = self.spawn_edible(EdibleConstants.EDIBLE_RADIUS, EdibleConstants.EDIBLE_COLOR)
        self.edibles.append(new_edible)
        print(f"Edible at location: ({edible.platform_x},{edible.platform_y}) has been removed")
        print(f"Created new edible at location: ({new_edible.platform_x},{new_edible.platform_y})")
        return new_edible
