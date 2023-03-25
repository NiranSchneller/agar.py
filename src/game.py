from constants import *
from player import Player
from playerCamera import PlayerCamera
from edible import Edible

pygame.init()
score = 0
FONT = pygame.font.SysFont('arial', 40)

def update_window(player, playerCamera, edibles):
    playerCamera.update_window(player.get_position())
    update_edibles(player, playerCamera, edibles)
    player.execute(PlayerConstants.PLAYER_COLOR, playerCamera.window)
    update_score(playerCamera.window)
    pygame.display.flip()


def update_score(player_camera_window):
    global score
    text = FONT.render(f"Score: {score}", True, (255,255,255))
    text_rect = text.get_rect()
    player_camera_window.blit(text, text_rect)


def update_edibles(player, playerCamera, edibles):
    for edible in edibles:
        edible.run(playerCamera.window, playerCamera.get_position())
        if edible.should_be_eaten(player.get_position(), player.radius):
            eat_edible(edible)
            edibles.remove(edible)

def eat_edible(edible):
    global score
    score += 1



"""
    Random distribution of edibles across the map
"""
def init_edibles():
    edibles = []




def generate_random_edible():

    return Edible(x,y,EdibleConstants.EDIBLE_COLOR)

"""
    Runs main.
"""
if __name__ == '__main__':
    running = True
    player = Player("Niran")
    playerCamera = PlayerCamera()
    edible = Edible(PlatformConstants.PLATFORM_WIDTH / 2 + 100, PlatformConstants.PLATFORM_HEIGHT / 2 + 100,
                    EdibleConstants.EDIBLE_COLOR)
    edibles = [edible]
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_window(player, playerCamera, edibles)
        clock.tick(GameSettings.FPS)
    pygame.quit()
