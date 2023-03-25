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
        self.radius = PlayerConstants.PLAYER_STARTING_RADIUS / 10
        self.x = x
        self.y = y
        self.color = color

    """
        Runs periodically, takes in camera coords and decides if to draw or not
    """
    def run(self, surface, camera_pos):
        camera_relative_position = self.platform_to_player_camera(camera_pos)
        if not camera_relative_position[0] < 0:
            self.draw(surface, camera_relative_position)

    def should_be_eaten(self, player_pos, player_radius):
        return get_distance(player_pos, (self.x, self.y)) < player_radius

    """
        Defines the position in player camera coords
    """
    def platform_to_player_camera(self, camera_pos):
        return (self.x - camera_pos[0]), (self.y - camera_pos[1])

    """
        Draw on screen, accepts camera relative coords
    """
    def draw(self, surface, camera_relative_pos):
        pygame.draw.circle(surface, self.color, (camera_relative_pos[0],
                                                 camera_relative_pos[1]), EdibleConstants.EDIBLE_RADIUS)

