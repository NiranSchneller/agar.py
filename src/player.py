import math
from constants import *



class Player:
    def __init__(self, name): # velocity measured in pixels per second
        self.name = name
        self.velocity = math.fabs(PLAYER_VELOCITY)
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.radius = PLAYER_STARTING_RADIUS

    def move(self):
        dx, dy = pygame.mouse.get_pos()
        # Magnitude of velocity with direction of mouse
        angle = math.atan2(dy - self.y, dx - self.x) # heading angle (atan2 to determine direction)

        self.x += self.velocity * math.cos(angle)
        self.y += self.velocity * math.sin(angle)

    def draw(self, color):
        pygame.draw.circle(GAME_WINDOW, color, self.get_position(), self.radius)

    def execute(self, drawColor):
        self.move()
        self.draw(drawColor)

    def get_position(self):
        return self.x, self.y