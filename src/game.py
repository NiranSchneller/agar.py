import math

from constants import *
from player import Player
from player_camera import PlayerCamera
from edible import Edible
from coordinate_system import CoordinateSystemHelper
import random
pygame.init()
score = 0
FONT = pygame.font.SysFont('arial', 40)

def update_window(player, player_camera, edibles):
    player_camera.update_window(player.get_position())
    update_edibles(player, player_camera, edibles)
    player.execute(PlayerConstants.PLAYER_COLOR, player_camera.window)
    update_score(player_camera.window)
    pygame.display.flip()


def update_score(player_camera_window):
    global score
    text = FONT.render(f"Score: {score}", True, (255,255,255))
    text_rect = text.get_rect()
    player_camera_window.blit(text, text_rect)


def update_edibles(player, player_camera, edibles):
    global score

    for edible in edibles:
        player_camera.draw_edible(edible)
        if edible.should_be_eaten(player.get_position(), player.radius):
            score += 1
            radius_change = player.eat()
            edible.print_distance(player.get_position(), player.radius)
            player_camera.edible_eaten(player.radius / PlayerConstants.PLAYER_STARTING_RADIUS,
                                       player.radius / PlayerConstants.PLAYER_STARTING_RADIUS)
            edibles.remove(edible)
            edibles.append(generate_random_edible())


"""
    Random distribution of edibles across the map
"""
def init_edibles():
    edibles = []

    for i in range(EdibleConstants.AMOUNT_OF_EDIBLES):
        edibles.append(generate_random_edible())
    return edibles

def generate_random_edible():
    radius = EdibleConstants.EDIBLE_RADIUS
    return Edible(random.randint(radius, PlatformConstants.PLATFORM_WIDTH - radius),
                  random.randint(radius, PlatformConstants.PLATFORM_HEIGHT - radius), EdibleConstants.EDIBLE_COLOR)

"""
    Runs main.
"""
if __name__ == '__main__':
    running = True
    player = Player("Niran")
    player_camera = PlayerCamera()
    edibles = init_edibles()
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_camera.edible_eaten(500, 500)

        update_window(player, player_camera, edibles)
        clock.tick(GameSettings.FPS)
    pygame.quit()
