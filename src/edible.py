from typing import Tuple

from pygame import Surface
from src.constants import *
import math
import pygame
"""
    Returns Euclidean distance between two points
    positions in: (x,y)
"""


def get_distance(pos1, pos2):
    return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])


"""
    Edible class, can be eaten by a player.
    Accepts x,y in PLATFORM coords, so it can be determined whether or not to show the edible

"""


class Edible:
    def __init__(self, x: int, y: int, color, radius: float = EdibleConstants.EDIBLE_RADIUS):
        self.radius: float = radius
        self.platform_x: int = x
        self.platform_y: int = y
        self.color = color

    def should_be_eaten(self, player_pos: Tuple[int, int], player_radius: float):
        return get_distance(player_pos, (self.platform_x, self.platform_y)) < player_radius + self.radius

    """
        Draw on screen, accepts camera relative coords
    """

    def draw(self, surface: Surface, screen_relative_pos: Tuple[int, int], radius: float):
        pygame.draw.circle(surface, self.color, (screen_relative_pos[0],
                                                 screen_relative_pos[1]), radius)

    def get_position(self) -> Tuple[int, int]:
        return self.platform_x, self.platform_y

    def __str__(self):
        return f"{self.platform_x},{self.platform_y}"

    def __eq__(self, other):
        return isinstance(other, Edible) and other.platform_y == self.platform_y and other.platform_x == self.platform_x \
               and other.radius == self.radius
