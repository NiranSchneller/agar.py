import random
import threading

from src.constants import EdibleConstants, PlatformConstants
from src.edible import Edible
from src.world import  World
import socket

class Server:
    """
        TCP Connection

        This server handles all clients added to him automatically (threading)

    """
    def __init__(self, max_waiting, ip = '0.0.0.0', port = 34197):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(max_waiting)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threads = []

        self.amount_of_clients = 0

    def __handle_client(self, client_socket, address):
        while True:
            print("nice")

    """
        Accepts a new client (blocking)
        
    """
    def accept(self):
        client_socket, address = self.socket.accept()
        t = threading.Thread(target=self.__handle_client, args=(client_socket, address))
        t.start()
        self.threads.append(t)
        self.amount_of_clients += 1

def start():

    server = Server(2)

    world = World(PlatformConstants.PLATFORM_WIDTH, PlatformConstants.PLATFORM_HEIGHT)
    world.spawn_edibles(EdibleConstants.AMOUNT_OF_EDIBLES)

    while True:
        # wait for new clients.
        server.accept()




