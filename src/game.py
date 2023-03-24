
from constants import *
from player import Player

WIN = GAME_WINDOW


def draw_grids():
    x = WINDOW_GRID_SPACING
    y = WINDOW_GRID_SPACING
    while x < WINDOW_WIDTH:
        pygame.draw.line(WIN, GRID_LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        x += WINDOW_GRID_SPACING
    while y < WINDOW_HEIGHT:
        pygame.draw.line(WIN, GRID_LINE_COLOR, (0, y), (WINDOW_WIDTH, y))
        y += WINDOW_GRID_SPACING

def update_window():
    WIN.fill(BACKGROUND_COLOR)
    draw_grids()
    player.execute((0, 200, 200))
    pygame.display.flip()

if __name__ == '__main__':
    running = True
    player = Player("Niran")
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_window()
        clock.tick(FPS)
    pygame.quit()
