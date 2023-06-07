import math

import pygame.font
import random
from src.constants import *
from src.interpolator import Interpolator

"""
    Returns Euclidean distance between two points
    positions in: (x,y)
"""


def get_distance(pos1, pos2):
    return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])


"""
    Player class
    Used for drawing and moving the player
"""

POSSIBLE_FONT_SIZES = range(10, 40)


def get_max_font_size(text, width):
    for size in reversed(POSSIBLE_FONT_SIZES):
        font = pygame.font.SysFont(None, size)
        if font.size(text)[0] <= width:
            return size
    return POSSIBLE_FONT_SIZES[0]


class Player:
    def __init__(self, name):  # velocity measured in pixels per second
        self.name = name
        self.velocity = math.fabs(PlayerConstants.PLAYER_VELOCITY)
        # actual player pos goes by the platform he is on
        self.radius = PlayerConstants.PLAYER_STARTING_RADIUS
        self.x = random.randint(self.radius, PlatformConstants.PLATFORM_WIDTH - self.radius)
        self.y = random.randint(self.radius, PlatformConstants.PLATFORM_HEIGHT - self.radius)
    """
        Function calculates current position change with respect to the mouse (follower)
        and current velocity
        The player doesn't actually move, because of that the position should be with respect to actual screen coords
        But when taking into account the mouse, the change in the position should be with respect to the playerCamera
    """

    def move(self):
        dx, dy = pygame.mouse.get_pos()
        # Magnitude of velocity with direction of mouse

        angle = math.atan2(dy - PlayerCameraConstants.SCREEN_HEIGHT / 2,
                           dx - PlayerCameraConstants.SCREEN_WIDTH / 2)

        distance = get_distance((PlayerCameraConstants.SCREEN_WIDTH / 2,
                                 PlayerCameraConstants.SCREEN_HEIGHT / 2), (dx, dy))
        if distance < PlayerConstants.DISTANCE_THRESHOLD:
            self.velocity = 0
        else:
            self.velocity = PlayerConstants.PLAYER_VELOCITY

        if (self.x <= self.radius and (self.velocity * math.cos(angle)) < 0) or (self.x >= PlatformConstants.PLATFORM_WIDTH - self.radius and (self.velocity * math.cos(angle))  > 0):
            self.velocity = 0
        elif (self.y <= self.radius and (self.velocity * math.sin(angle)) < 0) or (self.y >= PlatformConstants.PLATFORM_HEIGHT - self.radius and (self.velocity * math.sin(angle)) > 0):
            self.velocity = 0
        self.x += self.velocity * math.cos(angle)
        self.y += self.velocity * math.sin(angle)

    def draw(self, color, surface, coordinate_helper):
        screen_radius = coordinate_helper.platform_to_screen_radius(self.radius)
        screen_x, screen_y = coordinate_helper.platform_to_screen_coordinates(self.get_position())
        pygame.draw.circle(surface, color, (screen_x, screen_y), screen_radius)
        pygame.draw.circle(surface, PlayerConstants.PLAYER_OUTLINE_COLOR, (screen_x, screen_y),
                           screen_radius,
                           PlayerConstants.PLAYER_STARTING_OUTLINE_THICKNESS)

        cell_size = self.radius*2
        font_size = int(get_max_font_size(self.name, self.radius))
        font = pygame.font.SysFont("Arial", font_size)
        name_surface = font.render(self.name, True, (255,255,255))
        name_rect = name_surface.get_rect()
        name_rect.center = (screen_x, screen_y)
        surface.blit(name_surface, name_rect)


    """
        Runs periodically, HAS to be called by the game handler
    """

    def execute(self, drawColor, surface, coordinate_helper):
        self.move()
        #print(f"Player pos: {self.x},{self.y}" )
        self.draw(drawColor, surface, coordinate_helper)

    """
        Increases size by area of edible, returns radius change
    """

    def eat(self):
        old_radius = self.radius
        self.radius = ((math.pi * self.radius ** 2 + math.pi * EdibleConstants.EDIBLE_RADIUS ** 2) / math.pi) ** 0.5
        old_area = old_radius ** 2 * math.pi
        area = self.radius ** 2 * math.pi
        return self.radius - old_radius

    def get_position(self):
        return self.x, self.y
