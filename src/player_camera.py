from typing import Tuple
from src.constants import *
from src.interpolator import Interpolator
from src.coordinate_system import CoordinateSystemHelper
"""
    This class represents the player camera.
    It manages every 'Drawable', including the functionality of making the camera bigger and smaller.
    To do this, it's position is modified when the player gets bigger, 
"""


class PlayerCamera:
    def __init__(self, window):
        self.window = window
        pygame.display.set_caption(GameSettings.GAME_NAME)
        self.x = 0
        self.y = 0
        self.width = PlayerCameraConstants.SCREEN_WIDTH
        self.height = PlayerCameraConstants.SCREEN_HEIGHT

        self.coordinate_helper = CoordinateSystemHelper(self)

        self.width_interpolator = Interpolator(0.05, self.width)
        self.height_interpolator = Interpolator(0.05, self.height)

    """
        Periodic function, player camera moves with player
        because of this, new pos should be player pos
    """

    def update_window(self, player_pos):
        self.window.fill(PlayerCameraConstants.BACKGROUND_COLOR)
        self.update_position(player_pos)
        self.width = self.width_interpolator.lerp()
        self.height = self.height_interpolator.lerp()

    """
        Scales height and width of the camera,
        the scalars scale the size by the size of the screen
        
    """

    def edible_eaten(self, width_scalar, height_scalar):
        self.width_interpolator.init_lerp(
            self.width, PlayerCameraConstants.SCREEN_WIDTH * width_scalar)
        self.height_interpolator.init_lerp(
            self.height, PlayerCameraConstants.SCREEN_HEIGHT * height_scalar)

    def draw_edible(self, edible):
        screen_relative_position, edible_radius = self.coordinate_helper.platform_to_screen(
            edible.get_position(),
            edible.radius)
        if PlayerCamera.is_blob_position_on_screen((screen_relative_position[0], screen_relative_position[1]),
                                                   edible_radius, self.window, EdibleConstants.EDIBLE_COLOR):
            edible.draw(self.window, screen_relative_position, edible_radius)

    """
        Updates position according to player coords
        Position is saved in Platform coordinates, to determine actual location
    """

    def update_position(self, player_pos):
        self.x = player_pos[0] - self.width / 2
        self.y = player_pos[1] - self.height / 2

    def get_position(self):
        return self.x, self.y

    @staticmethod
    def is_blob_position_on_screen(pos: Tuple[float, float], radius: float, window, color) -> bool:
        pos_x = pos[0]
        pos_y = pos[1]

        return (pos_x + radius > 0) and pos_x - radius < PlayerCameraConstants.SCREEN_WIDTH \
            and pos_y + radius > 0 and pos_y - radius < PlayerCameraConstants.SCREEN_HEIGHT
