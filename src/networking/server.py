import threading

from src.constants import EdibleConstants, PlatformConstants
from src.world import  World
import socket
from src.networking.helpers.utils import send_with_size, recv_by_size
from src.networking.helpers.game_protocol import Protocol

world : World = None

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
        # Send first message
        message = Protocol.server_initiate_world((world.width, world.height), world.edibles)
        send_with_size(client_socket, message)

        # start getting status updates from the client
        while True:
            message = recv_by_size(client_socket) # recieve update
            player_information, edibles_eaten = Protocol.parse_client_status_update(message)


            new_edibles = []
            for edible in edibles_eaten:
                new_edibles.append(world.delete_edible(edible))
            # handled edible statuses
            # TODO: NOTIFY threads about location!
            player_locations = []
            edibles_removed = []
            send_with_size(client_socket, Protocol.generate_server_status_update(new_edibles, player_locations, edibles_removed))








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
    global world
    world = World(PlatformConstants.PLATFORM_WIDTH, PlatformConstants.PLATFORM_HEIGHT)
    world.spawn_edibles(EdibleConstants.AMOUNT_OF_EDIBLES)

    server = Server(2)

    while True:
        # wait for new clients.
        server.accept()





