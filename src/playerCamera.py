import pygame
from constants import *


class PlayerCamera:
    def __init__(self):
        self.window = pygame.display.set_mode((PlayerCameraConstants.PLAYER_CAMERA_WIDTH,
                                               PlayerCameraConstants.PLAYER_CAMERA_HEIGHT))
        pygame.display.set_caption(GameSettings.GAME_NAME)
        self.x = 0
        self.y = 0

    """
        Periodic function, player camera moves with player
        because of this, new pos should be player pos
    """
    def update_window(self, player_pos):
        self.window.fill(PlayerCameraConstants.BACKGROUND_COLOR)
        self.update_position(player_pos)
        self.draw_grids(player_pos)

    """
        Updates position according to player coords
        Position is saved in Platform coordinates, to determine actual location
    """
    def update_position(self, player_pos):
        self.x = player_pos[0] - PlayerConstants.PLAYER_LOCATION_CAMERA[0]
        self.y = player_pos[1] - PlayerConstants.PLAYER_LOCATION_CAMERA[1]

    """
     Draws grid lines in players FOV
     this is important because it simulates the players movement on the screen by changing the arrangement of the lines
    """
    def draw_grids(self, player_pos):
        x = PlayerCameraConstants.WINDOW_GRID_SPACING - (player_pos[0] % PlayerCameraConstants.WINDOW_GRID_SPACING)
        y = PlayerCameraConstants.WINDOW_GRID_SPACING - (player_pos[1] % PlayerCameraConstants.WINDOW_GRID_SPACING)
        while x < PlayerCameraConstants.PLAYER_CAMERA_WIDTH:
            pygame.draw.line(self.window, PlayerCameraConstants.GRID_LINE_COLOR, (x, 0),
                             (x, PlayerCameraConstants.PLAYER_CAMERA_HEIGHT))
            x += PlayerCameraConstants.WINDOW_GRID_SPACING
        while y < PlayerCameraConstants.PLAYER_CAMERA_HEIGHT:
            pygame.draw.line(self.window, PlayerCameraConstants.GRID_LINE_COLOR, (0, y),
                             (PlayerCameraConstants.PLAYER_CAMERA_WIDTH, y))
            y += PlayerCameraConstants.WINDOW_GRID_SPACING

    def get_position(self):
        return self.x, self.y

