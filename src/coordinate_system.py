from constants import *
import math
"""
    This class is a helper that transforms platform coords and sizes to fit to the screen


"""
class CoordinateSystemHelper:

    def __init__(self, player_camera):
        self.player_camera = player_camera


    """
        platform_pos -> tuple
        
        accepts a position in the platform coordinate system (world coords), and squeezes pos into screen (1920, 1080)
    """
    def platform_to_screen_coordinates(self, platform_pos):
        # Get ratio
        width_ratio = 1 / (self.player_camera.width / PlayerCameraConstants.SCREEN_WIDTH)
        camera_relative_x = platform_pos[0] - self.player_camera.x
        camera_relative_y = platform_pos[1] - self.player_camera.y
        # scale by ratio (screen top left 0,0)
        screen_relative_x = camera_relative_x * width_ratio
        screen_relative_y = camera_relative_y * width_ratio

        return screen_relative_x, screen_relative_y

    def platform_to_screen_radius(self, platform_radius):
        width_ratio = 1 / (self.player_camera.width / PlayerCameraConstants.SCREEN_WIDTH)
        platform_area = math.pi * platform_radius**2
        screen_area = platform_area * width_ratio
        screen_radius = (screen_area/math.pi)**0.5
        return screen_radius

    def platform_to_screen(self, platform_pos, platform_radius):
        return (self.platform_to_screen_coordinates(platform_pos)), self.platform_to_screen_radius(platform_radius)