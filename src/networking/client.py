import math
import random
import socket
import sys
import threading
import uuid
import traceback
import pygame
import pygame_menu

from coordinate_system import CoordinateSystemHelper
from src.constants import GameSettings, PlayerConstants, EdibleConstants, PlatformConstants, PlayerCameraConstants
from src.networking.helpers import game_protocol
from src.edible import Edible
from src.networking.information.player_information import PlayerInformation
from src.networking.helpers.game_protocol import Protocol
from src.player import Player
from src.player_camera import PlayerCamera
from src.networking.helpers.utils import recv_by_size, send_with_size
from uuid import uuid4
from typing import List
THEME = pygame_menu.themes.THEME_BLUE # type: ignore

POSSIBLE_FONT_SIZES = range(10, 40)


def get_max_font_size(text, width):
    for size in reversed(POSSIBLE_FONT_SIZES):
        font = pygame.font.SysFont(None, size)  # type: ignore
        if font.size(text)[0] <= width:
            return size
    return POSSIBLE_FONT_SIZES[0]


window: pygame.Surface = None  # type: ignore
pygame.init()
client_thread: threading.Thread = None # type: ignore
score = 0
FONT = pygame.font.SysFont('arial', 40)
running = True
player = None  # type: ignore
player_camera = None  # type: ignore


class WorldInformation:

    def __init__(self):
        self.width: int = 0
        self.height: int = 0
        self.edibles: List[Edible] = []
        self.players: List[PlayerInformation] = []

    def initiate_edibles(self, edibles: List[Edible]):
        self.edibles = edibles

    def __add_edible(self, edible: Edible):
        self.edibles.append(edible)

    def add_edibles(self, edibles: List[Edible]):
        for edible in edibles:
            self.__add_edible(edible)

    def remove_edibles(self, edibles_removed: List[Edible]):
        for edible in edibles_removed:
            self.edibles.remove(edible)

    def set_players(self, other_players: List[PlayerInformation]):
        self.players = other_players


class Client:
    def __init__(self, host: str, port: int, world_information: WorldInformation, player_information: PlayerInformation):
        self.socket: socket.socket = socket.socket()
        self.thread: threading.Thread = None  # type: ignore
        try:
            self.socket.connect((host, port))
            print("Connected")
        except:
            print("Connection error, please check ip or port!")
            sys.exit()

        # To Handle sending data
        self.world_information: WorldInformation = world_information
        self.player_information: PlayerInformation = player_information
        self.edible_eaten_list: List[Edible] = list()

    """
        Starts recieving and sending messages, opens a seperate thread
    """

    def start_client(self):
        message: str = recv_by_size(self.socket)
        world_size, edibles = game_protocol.Protocol.parse_server_initiate_world(
            message)
        self.world_information.initiate_edibles(edibles)
        self.world_information.width, self.world_information.height = world_size  # type: ignore

        self.thread = threading.Thread(
            target=self.__handle_connection, args=())
        global client_thread
        client_thread = self.thread
        self.thread.start()

    """
        Main client func, communicates with the server and updates the server on relevant information
    """

    def __handle_connection(self):
        global running
        unique_id = uuid.uuid4().hex
        while running:
            message = Protocol.generate_client_status_update(self.player_information.x, self.player_information.y,
                                                             self.player_information.radius,
                                                             self.player_information.name,
                                                             unique_id,
                                                             self.edible_eaten_list.copy())
            self.edible_eaten_list.clear()

            # update the server on relevant information
            send_with_size(self.socket, message)
            server_reply = recv_by_size(self.socket)

            if Protocol.parse_server_status_update(server_reply) == "EATEN":
                running = False
            else:
                edibles_created, other_players, edibles_removed, ate_inc = Protocol.parse_server_status_update(
                    server_reply)
                # If we got here then the reply can't be a string
                self.world_information.remove_edibles(
                    edibles_removed)  # type: ignore
                self.world_information.add_edibles(
                    edibles_created)  # type: ignore
                self.world_information.set_players(
                    other_players)  # type: ignore

                global player
                player.radius += ate_inc  # type: ignore
                player_camera.edible_eaten(player.radius / PlayerConstants.PLAYER_STARTING_RADIUS,
                                           player.radius / PlayerConstants.PLAYER_STARTING_RADIUS)

    """
        Will add to a queue for the thread to send to the server
    """

    def notify_eaten_edible(self, edible: Edible):
        self.edible_eaten_list.append(edible)

    """
        This information is sent to the server to update location
    """

    def update_player_information(self, x: int, y: int, radius: float):
        self.player_information.x = x
        self.player_information.y = y
        self.player_information.radius = radius


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
    update_minimap(list(other_player_information),
                   world_information_dimensions, list(edibles))
    pygame.display.flip()


MINIMAP_SIZE = (200, 200)
MINIMAP_POSE = (0, 0)  # (X,Y)
MINIMAP_BORDER_SIZE = 5


def update_minimap(other_player_information: List[PlayerInformation], world_information_dimensions, edibles):
    other_player_information.append(PlayerInformation(
        player.x, player.y, player.radius, player.name, "MyPlayer"))

    for edible in edibles:
        edible_clone = PlayerInformation(
            edible.platform_x, edible.platform_y, edible.radius, "iAmEdible", "Edible")
        other_player_information.append(edible_clone)

    global window
    # Border rectangle
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(
        MINIMAP_POSE[0], MINIMAP_POSE[1], MINIMAP_SIZE[0] +
        MINIMAP_BORDER_SIZE,
        MINIMAP_SIZE[1] + MINIMAP_BORDER_SIZE))

    pygame.draw.rect(window, (173, 216, 190), pygame.Rect(
        MINIMAP_POSE[0], MINIMAP_POSE[1],
        MINIMAP_SIZE[0], MINIMAP_SIZE[1]))

    world_width = world_information_dimensions[0]
    world_height = world_information_dimensions[1]
    for player_information in other_player_information[::-1]:
        x_scale_ratio = MINIMAP_SIZE[0] / int(world_width)
        y_scale_ratio = MINIMAP_SIZE[1] / int(world_height)

        absolute_player_minimap_x = player_information.x * x_scale_ratio
        absolute_player_minimap_y = player_information.y * y_scale_ratio

        player_minimap_x = MINIMAP_POSE[0] + absolute_player_minimap_x
        player_minimap_y = MINIMAP_POSE[1] + absolute_player_minimap_y
        player_minimap_radius = player_information.radius * y_scale_ratio * 6

        color = PlayerConstants.PLAYER_COLOR
        if player_information.name == "iAmEdible":
            color = EdibleConstants.EDIBLE_COLOR

        pygame.draw.circle(window, color,
                           (player_minimap_x, player_minimap_y), max(player_minimap_radius, MINIMAP_POSE[0]))
        # The appended player information has "" as its
        if player_information.id == "MyPlayer":
            font_size = Player.get_max_font_size("You", player_minimap_radius)
            font = pygame.font.SysFont("Arial", font_size)
            name_surface = font.render("You", True, (255, 255, 255))
            name_rect = name_surface.get_rect()
            name_rect.center = (player_minimap_x, player_minimap_y) # type: ignore
            window.blit(name_surface, name_rect)


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


def draw_other_player(x: int, y: int, radius: float, color, name: str, coordinate_helper: CoordinateSystemHelper):
    screen_radius = coordinate_helper.platform_to_screen_radius(radius)
    screen_x, screen_y = coordinate_helper.platform_to_screen_coordinates(
        (x, y))

    if not screen_x < 0:
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


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


def update_score():
    global score
    text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    text_rect = text.get_rect()
    window.blit(text, text_rect)


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


def start(name: str, ip: str, port: int, screen: pygame.Surface):
    try:
        global running
        global window
        global player
        global player_camera
        running = True  # for more than 1st run
        window = screen
        
        player: Player = Player(name)
        player_camera: PlayerCamera = PlayerCamera(window)
        world_information: WorldInformation = WorldInformation()
        player_information = PlayerInformation(
            player.x, player.y, player.radius, player.name)
        
        print(f"Client will connect to: {ip}:{port}")
        
        client: Client = Client(
            ip, port, world_information, player_information)
        client.start_client()
    except:
        print("Problem during initialization!")
        sys.exit()
    try:
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            update_window(player, player_camera, world_information.edibles,
                          client, world_information.players, (world_information.width, world_information.height))
            clock.tick(GameSettings.FPS)
    except:
        print(f"Problem while running!, stacktrace: {traceback.print_exc()}")

        sys.exit()
    global client_thread
    client_thread.join()
