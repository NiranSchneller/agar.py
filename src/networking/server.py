import threading

from src.constants import EdibleConstants, PlatformConstants
from src.networking.handlers.collision_detector import CollisionDetector
from src.networking.handlers.player_update_handler import PlayerUpdateHandler
from src.networking.handlers.edible_update_handler import EdibleUpdateHandler

from src.world import  World
import socket
from src.networking.helpers.utils import send_with_size, recv_by_size
from src.networking.helpers.game_protocol import Protocol
from threading import Lock
world : World = None
lock = Lock()


def collision_exists(player1, player2):
    dist = ((player1.x - player2.x)**2 + (player1.y - player2.y)**2)**0.5
    return dist < max(player1.radius, player2.radius)

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
        self.collision_detector = CollisionDetector()
        self.collision_detector_thread = threading.Thread(target=self.__handle_collisions, args=())
        self.collision_detector_thread.start()

        self.player_update_handler = PlayerUpdateHandler()
        self.edible_update_handler = EdibleUpdateHandler()

        self.player_thread = dict()

        self.amount_of_clients = 0

    def __handle_client(self, client_socket, address, thread_id : int):
        # Send first message
        message = Protocol.server_initiate_world((world.width, world.height), world.edibles)
        send_with_size(client_socket, message)
        self.edible_update_handler.make_space_for_new_thread()
        # start getting status updates from the client
        while True:
            message = recv_by_size(client_socket) # recieve update
            player_information, edibles_eaten = Protocol.parse_client_status_update(message)

            self.player_thread[player_information.name] = thread_id # for collision detection

            new_edibles = []
            for edible in edibles_eaten:
                new_edibles.append(world.delete_edible(edible))

            if new_edibles:
                print(f"New edibles: {new_edibles}")
            if edibles_eaten:
                print(f"Edibles eaten: {edibles_eaten}")

            lock.acquire()
            self.edible_update_handler.notify_threads_changing_edible_status(new_edibles, edibles_eaten, thread_id)
            self.player_update_handler.update_player(player_information)
            other_player_information = self.player_update_handler.get_players(player_information)
            edibles_removed, new_edibles_other = self.edible_update_handler.fetch_thread_specific_edible_updates(thread_id)
            lock.release()
            if new_edibles_other:
                print(f"{new_edibles_other}")
            new_edibles = new_edibles + new_edibles_other
            send_with_size(client_socket, Protocol.generate_server_status_update(new_edibles, other_player_information, edibles_removed))

    def __handle_collisions(self):
        while True:
            lock.acquire()
            collisions = self.__detect_collisions(self.player_update_handler.get_players())
            lock.release()
            for collision in collisions:
                pass # to be continued

    def __detect_collisions(self, players):
        collisions = []
        for player_information in players:
            for collision_search in players:
                if player_information.name != collision_search.name and collision_exists(player_information,
                                                                                         collision_search):
                    collisions.append((player_information, collision_search))
        return collisions

    """
        Accepts a new client (blocking)
    """
    def accept(self):
        client_socket, address = self.socket.accept()
        t = threading.Thread(target=self.__handle_client, args=(client_socket, address, self.amount_of_clients))
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





