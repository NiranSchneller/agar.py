import pygame
from constants import *


class PlayerCamera:
    def __init__(self):
        self.window = pygame.display.set_mode((PLAYER_CAMERA_WIDTH, PLAYER_CAMERA_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.x = 0
        self.y = 0

    """
        Periodic function, player camera moves with player
        because of this, new pos should be player pos
    """
    def update_window(self, player_pos):
        self.window.fill(BACKGROUND_COLOR)
        self.draw_grids(player_pos)

    """
     Draws grid lines in players FOV
     this is important because it simulates the players movement on the screen by changing the arrangement of the lines
    """
    def draw_grids(self, player_pos):
        x = WINDOW_GRID_SPACING - (player_pos[0] % WINDOW_GRID_SPACING)
        y = WINDOW_GRID_SPACING - (player_pos[1] % WINDOW_GRID_SPACING)
        while x < PLAYER_CAMERA_WIDTH:
            pygame.draw.line(self.window, GRID_LINE_COLOR, (x, 0), (x, PLAYER_CAMERA_HEIGHT))
            x += WINDOW_GRID_SPACING
        while y < PLAYER_CAMERA_HEIGHT:
            pygame.draw.line(self.window, GRID_LINE_COLOR, (0, y), (PLAYER_CAMERA_WIDTH, y))
            y += WINDOW_GRID_SPACING
