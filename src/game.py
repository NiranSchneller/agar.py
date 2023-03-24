
from constants import *
from player import Player
from playerCamera import PlayerCamera


def update_window(player, playerCamera):
    playerCamera.update_window(player.get_position())
    player.execute(PlayerConstants.PLAYER_COLOR, playerCamera.window)
    pygame.display.flip()


if __name__ == '__main__':
    running = True
    player = Player("Niran")
    playerCamera = PlayerCamera()
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_window(player, playerCamera)
        clock.tick(GameSettings.FPS)
    pygame.quit()
