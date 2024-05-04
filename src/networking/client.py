import sys
import threading
import traceback
import pygame
import pygame_menu

from src.minimap import Minimap
from src.networking.agar_client import Client
from src.networking.helpers.world_information import WorldInformation
from src.constants import GameSettings, PlayerCameraConstants, PlayerConstants, EdibleConstants
from src.coordinate_system import CoordinateSystemHelper
from src.edible import Edible
from src.networking.information.player_information import PlayerInformation
from src.player import Player
from src.player_camera import PlayerCamera
from typing import List
from src.networking.helpers.utils import get_max_font_size
THEME = pygame_menu.themes.THEME_BLUE  # type: ignore

window: pygame.Surface = None  # type: ignore
pygame.init()
client_thread: threading.Thread = None  # type: ignore
score = 0
FONT = pygame.font.SysFont('arial', 40)
running = True
player = None  # type: ignore
player_camera = None  # type: ignore


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


def update_score():
    global score
    text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    text_rect = text.get_rect()
    window.blit(text, text_rect)


def draw_bigger_players(other_player_information: List[PlayerInformation], coords: CoordinateSystemHelper,
                        player_radius: float):
    for player_information in other_player_information:
        if player_information.radius > player_radius:
            draw_other_player(player_information.x, player_information.y, player_information.radius,
                              PlayerConstants.PLAYER_COLOR, player_information.name, coords)


def draw_other_players(other_player_information: List[PlayerInformation], coords: CoordinateSystemHelper):
    for player_information in other_player_information:
        draw_other_player(player_information.x, player_information.y, player_information.radius,
                          PlayerConstants.PLAYER_COLOR, player_information.name, coords)


def draw_other_player(x: int, y: int, radius: float, color, name: str,
                      coordinate_helper: CoordinateSystemHelper):
    screen_radius = coordinate_helper.platform_to_screen_radius(radius)
    screen_x, screen_y = coordinate_helper.platform_to_screen_coordinates(
        (x, y))

    if PlayerCamera.is_position_on_screen((screen_x, screen_y)):
        pygame.draw.circle(window, color, (screen_x, screen_y), screen_radius)
        pygame.draw.circle(window, PlayerConstants.PLAYER_OUTLINE_COLOR, (screen_x, screen_y),
                           screen_radius,
                           PlayerConstants.PLAYER_STARTING_OUTLINE_THICKNESS)

        font_size = int(get_max_font_size(name, radius))
        font = pygame.font.SysFont("Arial", font_size)

        name_surface = font.render(name, True, (255, 255, 255))
        name_rect = name_surface.get_rect()
        name_rect.center = (screen_x, screen_y)
        window.blit(name_surface, name_rect)


def update_edibles(player: Player, player_camera: PlayerCamera, edibles: List[Edible], client: Client):
    global score

    for edible in edibles:
        player_camera.draw_edible(edible)
        if edible.should_be_eaten(player.get_position(), player.radius):
            score += 1
            # notify the server that the player has eaten an edible
            client.notify_eaten_edible(edible)
            scale = player.radius / PlayerConstants.PLAYER_STARTING_RADIUS
            player_camera.edible_eaten(scale,
                                       scale)
            player.eat()
            edibles.remove(edible)


def update_window(player: Player, player_camera: PlayerCamera, edibles: List[Edible], client: Client,
                  other_player_information: List[PlayerInformation], world_information_dimensions):

    player_camera.update_window(player.get_position())

    update_edibles(player, player_camera, edibles, client)

    draw_other_players(other_player_information,
                       player_camera.coordinate_helper)

    player.execute(PlayerConstants.PLAYER_COLOR, window,
                   player_camera.coordinate_helper)

    draw_bigger_players(other_player_information,
                        player_camera.coordinate_helper, player.radius)

    update_score()
    client.update_player_information(player.x, player.y, player.radius)

    Minimap.update_minimap(list(other_player_information),
                           world_information_dimensions, list(edibles), player, window)
    pygame.display.flip()


def start(name: str, ip: str, port: int, screen: pygame.Surface):
    try:
        global running
        global window
        global player
        global player_camera
        running = True  # for more than 1st run
        window = screen

        player = Player(name)
        player_camera = PlayerCamera(window)
        world_information: WorldInformation = WorldInformation()
        player_information = PlayerInformation(
            player.x, player.y, player.radius, player.name)

        print(f"Client will connect to: {ip}:{port}")

        client: Client = Client(
            ip, port, world_information, player_information, player_camera, player)
        client.start_client()
    except:
        print(f"Problem during initialization! {traceback.print_exc()}")
        sys.exit()
    try:
        clock = pygame.time.Clock()
        while client.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    client.running = False
                    client.thread.join()
            update_window(player, player_camera, world_information.edibles,
                          client, world_information.players, (world_information.width, world_information.height))
            clock.tick(GameSettings.FPS)
    except:
        print(f"Problem while running!, stacktrace: {traceback.print_exc()}")
        sys.exit()
