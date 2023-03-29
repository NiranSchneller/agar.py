import random
import socket
import threading

import pygame

from src.constants import GameSettings, PlayerCameraConstants, PlayerConstants, EdibleConstants, PlatformConstants
from src.edible import Edible
from src.player import Player
from src.player_camera import PlayerCamera

window = None
pygame.init()
score = 0
FONT = pygame.font.SysFont('arial', 40)

class WorldInformation:

    def __init__(self):
        self.edibles = []
        self.players = []

    def initiate_edibles(self, edibles: [Edible]):
        self.edibles = edibles


class Client:
    def __init__(self, host, port):
        self.socket = socket.socket()
        self.thread = None
        try:
            self.socket.connect((host, port))
            print("Connected")
        except:
            print("Connection error, please check ip or port!")


    """
        Starts recieving and sending messages, opens a seperate thread
    """
    def start_client(self):
        self.thread = threading.Thread(target=self.__handle_connection, args=())

    def __handle_connection(self):
        pass



# Game Variables


def update_window(player, player_camera, edibles):
    player_camera.update_window(player.get_position())
    update_edibles(player, player_camera, edibles)
    player.execute(PlayerConstants.PLAYER_COLOR, window, player_camera.coordinate_helper)
    update_score()
    pygame.display.flip()


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

def update_score():
    global score
    text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    text_rect = text.get_rect()
    window.blit(text, text_rect)


def update_edibles(player, player_camera, edibles):
    global score

    for edible in edibles:
        player_camera.draw_edible(edible)
        if edible.should_be_eaten(player.get_position(), player.radius):
            score += 1
            edible.print_distance(player.get_position(), player.radius)
            scale = player.radius / PlayerConstants.PLAYER_STARTING_RADIUS
            player_camera.edible_eaten(scale,
                                       scale)
            player.eat()
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

def start(width, height):
    running = True

    global window
    window = pygame.display.set_mode((width, height))

    player = Player("Niran")
    player_camera = PlayerCamera(window)

    client = Client("192.168.1.29", 34197)

    edibles = init_edibles()

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_window(player, player_camera, edibles)
        clock.tick(GameSettings.FPS)
    pygame.quit()