from constants import *


"""
    This class represents the player camera.
    It manages every 'Drawable', including the functionality of making the camera bigger and smaller.
    To do this, it's position is modified when the player gets bigger, 
"""

class PlayerCamera:


    def __init__(self):
        self.window = pygame.display.set_mode((PlayerCameraConstants.SCREEN_WIDTH,
                                               PlayerCameraConstants.SCREEN_HEIGHT))
        pygame.display.set_caption(GameSettings.GAME_NAME)
        self.x = 0
        self.y = 0
        self.width = PlayerCameraConstants.SCREEN_WIDTH
        self.height = PlayerCameraConstants.SCREEN_HEIGHT


    """
        Periodic function, player camera moves with player
        because of this, new pos should be player pos
    """
    def update_window(self, player_pos):
        self.window.fill(PlayerCameraConstants.BACKGROUND_COLOR)
        self.update_position(player_pos)
        #self.draw_grids(player_pos)
        #print(f"{self.width},{self.height}")


    """
        Increases height and width of the camera
    """
    def edible_eaten(self, increase_width, increase_height):
        self.width += increase_width
        self.height += increase_height


    def draw_edible(self, edible):
        camera_relative_position, edible_radius = self.platform_to_player_camera(self.get_position(), edible)
        if not camera_relative_position[0] < 0:

           edible.draw(self.window, camera_relative_position, edible_radius)

    """
        transforms world coordinates to screen coordinates, takes into account camera size
    """
    def platform_to_player_camera(self, camera_pos, edible):
        # Get ratio
        width_ratio = 1 / (self.width / PlayerCameraConstants.SCREEN_WIDTH)
        camera_relative_x = edible.platform_x - self.x
        camera_relative_y = edible.platform_y - self.y
        # scale by ratio (screen top left 0,0)
        screen_relative_x = camera_relative_x * width_ratio
        screen_relative_y = camera_relative_y * width_ratio

        edible_radius = edible.radius * width_ratio
        return (screen_relative_x, screen_relative_y), edible_radius

    """
        Updates position according to player coords
        Position is saved in Platform coordinates, to determine actual location
    """
    def update_position(self, player_pos):
        self.x = player_pos[0] - self.width / 2
        self.y = player_pos[1] - self.height / 2

    """
     Draws grid lines in players FOV
     this is important because it simulates the players movement on the screen by changing the arrangement of the lines
    """
    def draw_grids(self, player_pos):
        # Amount of lines that need to be drawn in order to simulate changing camera size
        amount_of_lines_x = self.width / PlayerCameraConstants.WINDOW_GRID_SPACING
        amount_of_lines_y = self.height / PlayerCameraConstants.WINDOW_GRID_SPACING

        # Scaling spacing by the width and height of the screen.
        window_grid_spacing_x = PlayerCameraConstants.SCREEN_WIDTH / amount_of_lines_x
        window_grid_spacing_y = PlayerCameraConstants.SCREEN_HEIGHT / amount_of_lines_y
        print(f"Spacing: {window_grid_spacing_x},{window_grid_spacing_y}")

        x = PlayerCameraConstants.WINDOW_GRID_SPACING - (player_pos[0] % PlayerCameraConstants.WINDOW_GRID_SPACING)
        y = PlayerCameraConstants.WINDOW_GRID_SPACING - (player_pos[1] % PlayerCameraConstants.WINDOW_GRID_SPACING)
        while x < PlayerCameraConstants.SCREEN_WIDTH:
            pygame.draw.line(self.window, PlayerCameraConstants.GRID_LINE_COLOR, (x, 0),
                             (x, PlayerCameraConstants.SCREEN_HEIGHT))
            x += window_grid_spacing_x
        while y < PlayerCameraConstants.SCREEN_HEIGHT:
            pygame.draw.line(self.window, PlayerCameraConstants.GRID_LINE_COLOR, (0, y),
                             (PlayerCameraConstants.SCREEN_WIDTH, y))
            y += window_grid_spacing_y

    def get_position(self):
        return self.x, self.y
