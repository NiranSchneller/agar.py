from constants import *
import math

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
    def __init__(self, x, y, color):
        self.radius = EdibleConstants.EDIBLE_RADIUS
        self.platform_x = x
        self.platform_y = y
        self.color = color

    def should_be_eaten(self, player_pos, player_radius):
        return get_distance(player_pos, (self.platform_x, self.platform_y)) < player_radius + self.radius

    def print_distance(self, player_pos, player_radius):
        print(f"Distance: {get_distance(player_pos, (self.platform_x, self.platform_y))}")

    """
        Draw on screen, accepts camera relative coords
    """
    def draw(self, surface, screen_relative_pos, radius):
        pygame.draw.circle(surface, self.color, (screen_relative_pos[0],
                                                 screen_relative_pos[1]), radius)
    def get_position(self):
        return self.platform_x, self.platform_y

    def __str__(self):
        return f"{self.x},{self.y}"
