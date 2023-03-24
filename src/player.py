import math
from constants import *


"""
    Function derived from x**2
    when at distance threshold, value should be 1
    so: (1/xx) * xx = 1
    
"""
def mathematical_velocity_stretcher(distance):
    return (1/DISTANCE_THRESHOLD**2) * (distance**2)

"""
    Returns Euclidean distance between two points
    positions in: (x,y)
"""
def get_distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5


"""
    Player class
    Used for drawing and moving the player
"""
class Player:
    def __init__(self, name): # velocity measured in pixels per second
        self.name = name
        self.velocity = math.fabs(PLAYER_VELOCITY)
        # actual player pos goes by the platform he is on
        self.x = PLATFORM_WIDTH / 2
        self.y = PLATFORM_HEIGHT / 2
        self.radius = PLAYER_STARTING_RADIUS


    """
        Function calculates current position change with respect to the mouse (follower)
        and current velocity
        The player doesn't actually move, because of that the position should be with respect to actual screen coords
        But when taking into account the mouse, the change in the position should be with respect to the playerCamera
    """
    def move(self):
        dx, dy = pygame.mouse.get_pos()
        # Magnitude of velocity with direction of mouse

        angle = math.atan2(dy - PLAYER_CAMERA_HEIGHT / 2, dx - PLAYER_CAMERA_WIDTH / 2)
        distance = get_distance((PLAYER_CAMERA_WIDTH / 2, PLAYER_CAMERA_HEIGHT / 2), (dx, dy))
        if distance < DISTANCE_THRESHOLD:
            self.velocity = 0
        else:
            self.velocity = PLAYER_VELOCITY

        self.x += self.velocity * math.cos(angle)
        self.y += self.velocity * math.sin(angle)

    def draw(self, color, surface):
        pygame.draw.circle(surface, color, (PLAYER_CAMERA_WIDTH / 2, PLAYER_CAMERA_HEIGHT / 2), self.radius)

    """
        Runs periodically, HAS to be called by the game handler
    """
    def execute(self, drawColor, surface):
        self.move()
        self.draw(drawColor, surface)

    def get_position(self):
        return self.x, self.y