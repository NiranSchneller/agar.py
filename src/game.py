from constants import *
from player import Player
from playerCamera import PlayerCamera
from edible import Edible

def update_window(player, playerCamera, edible):
    playerCamera.update_window(player.get_position())
    player.execute(PlayerConstants.PLAYER_COLOR, playerCamera.window)
    edible.run(playerCamera.window, playerCamera.get_position())
    pygame.display.flip()




"""
    Runs main.
"""
if __name__ == '__main__':
    running = True
    player = Player("Niran")
    playerCamera = PlayerCamera()
    edible = Edible(PlatformConstants.PLATFORM_WIDTH / 2, PlatformConstants.PLATFORM_HEIGHT / 2,
                    EdibleConstants.EDIBLE_COLOR)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_window(player, playerCamera, edible)
        clock.tick(GameSettings.FPS)
    pygame.quit()
