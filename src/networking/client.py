import random
import socket
import sys
import threading

import pygame

from src.constants import GameSettings, PlayerConstants, EdibleConstants, PlatformConstants
from src.networking.helpers import game_protocol
from src.edible import Edible
from src.networking.information.player_information import PlayerInformation
from src.networking.helpers.game_protocol import Protocol
from src.player import Player
from src.player_camera import PlayerCamera
from src.networking.helpers.utils import recv_by_size, send_with_size

window = None
pygame.init()
score = 0
FONT = pygame.font.SysFont('arial', 40)
running = True
player : Player = None
class WorldInformation:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.edibles = []
        self.players : [PlayerInformation] = []

    def initiate_edibles(self, edibles: [Edible]):
        self.edibles = edibles

    def __add_edible(self, edible):
        self.edibles.append(edible)

    def add_edibles(self, edibles: [Edible]):
        for edible in edibles:
            self.__add_edible(edible)

    def remove_edibles(self, edibles_removed):
        for edible in edibles_removed:
            self.edibles.remove(edible)

    def set_players(self, other_players):
        self.players = other_players

class Client:
    def __init__(self, host, port, world_information: WorldInformation, player_information: PlayerInformation):
        self.socket = socket.socket()
        self.thread = None
        try:
            self.socket.connect((host, port))
            print("Connected")
        except:
            print("Connection error, please check ip or port!")
            sys.exit()

        # To Handle sending data
        self.world_information = world_information
        self.player_information = player_information
        self.edible_eaten_list = list()

    """
        Starts recieving and sending messages, opens a seperate thread
    """

    def start_client(self):
        message = recv_by_size(self.socket)
        world_size, edibles = game_protocol.Protocol.parse_server_initiate_world(message)
        self.world_information.initiate_edibles(edibles)
        self.world_information.width, self.world_information.height = world_size

        self.thread = threading.Thread(target=self.__handle_connection, args=())
        self.thread.start()


    """
        Main client func, communicates with the server and updates the server on relevant information
    """
    def __handle_connection(self):
        global running
        while running:
            message = Protocol.generate_client_status_update(self.player_information.x, self.player_information.y,
                                                             self.player_information.radius,
                                                             self.player_information.name,
                                                             self.edible_eaten_list.copy())
            self.edible_eaten_list.clear()

            send_with_size(self.socket, message)  # update the server on relevant information
            server_reply = recv_by_size(self.socket)

            if Protocol.parse_server_status_update(server_reply) == "EATEN":
                running = False
                break

            edibles_created, other_players, edibles_removed, ate_inc = Protocol.parse_server_status_update(server_reply)

            self.world_information.remove_edibles(edibles_removed)
            self.world_information.add_edibles(edibles_created)
            self.world_information.set_players(other_players)

            global player
            player.radius += ate_inc




    """
        Will add to a queue for the thread to send to the server
    """

    def notify_eaten_edible(self, edible: Edible):
        self.edible_eaten_list.append(edible)

    """
        This information is sent to the server to update location
    """

    def update_player_information(self, x, y, radius):
        self.player_information.x = x
        self.player_information.y = y
        self.player_information.radius = radius




def update_window(player, player_camera, edibles, client: Client, other_player_information):
    player_camera.update_window(player.get_position())
    update_edibles(player, player_camera, edibles, client)
    draw_other_players(other_player_information, player_camera.coordinate_helper)
    player.execute(PlayerConstants.PLAYER_COLOR, window, player_camera.coordinate_helper)
    update_score()
    client.update_player_information(player.x, player.y, player.radius)
    pygame.display.flip()


def draw_other_players(other_player_information : [PlayerInformation], coords):
    for player_information in other_player_information:
        print("drawing")
        draw_other_player(player_information.x, player_information.y, player_information.radius, PlayerConstants.PLAYER_COLOR, coords)

def draw_other_player(x, y, radius, color, coordinate_helper):
    screen_radius = coordinate_helper.platform_to_screen_radius(radius)
    screen_x, screen_y = coordinate_helper.platform_to_screen_coordinates((x, y))

    if not screen_x < 0:
        pygame.draw.circle(window, color, (screen_x, screen_y), screen_radius)
        pygame.draw.circle(window, PlayerConstants.PLAYER_OUTLINE_COLOR, (screen_x, screen_y),
                           screen_radius,
                           PlayerConstants.PLAYER_STARTING_OUTLINE_THICKNESS)



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


def update_score():
    global score
    text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    text_rect = text.get_rect()
    window.blit(text, text_rect)


def update_edibles(player, player_camera, edibles, client):
    global score

    for edible in edibles:
        player_camera.draw_edible(edible)
        if edible.should_be_eaten(player.get_position(), player.radius):
            score += 1
            client.notify_eaten_edible(edible)  # notify the server that the player has eaten an edible
            scale = player.radius / PlayerConstants.PLAYER_STARTING_RADIUS
            player_camera.edible_eaten(scale,
                                       scale)
            player.eat()
            edibles.remove(edible)


def start(width, height, name):

    global window
    window = pygame.display.set_mode((width, height))

    global player
    player = Player(name)
    player_camera = PlayerCamera(window)
    world_information = WorldInformation()
    player_information = PlayerInformation(player.x, player.y, player.radius, player.name)

    client = Client("192.168.1.29", 34197, world_information, player_information)
    client.start_client()

    clock = pygame.time.Clock()
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # TODO: terminate the client server connection

        update_window(player, player_camera, world_information.edibles, client, world_information.players)
        clock.tick(GameSettings.FPS)
    pygame.quit()
