from constants import *
from player import Player
from playerCamera import PlayerCamera
from edible import Edible
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
    for edible in edibles:
        player_camera.draw_edible(edible)
        if edible.should_be_eaten(player.get_position(), player.radius):
            eat_edible(edible, player)
            edibles.remove(edible)
            player_camera.edible_eaten(5, 5) # Reports to the player camera that an edible has been eaten
            edibles.append(generate_random_edible())

def eat_edible(edible, player):
    global score
    score += 1
    player.eat()

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
        update_window(player, player_camera, edibles)
        clock.tick(GameSettings.FPS)
    pygame.quit()
