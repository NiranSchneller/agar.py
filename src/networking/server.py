import sys
import threading

from src.constants import EdibleConstants, PlatformConstants
from src.networking.handlers.collision_detector import CollisionDetector
from src.networking.handlers.player_update_handler import PlayerUpdateHandler
from src.networking.handlers.edible_update_handler import EdibleUpdateHandler
import traceback
import time
from src.world import World
import socket
from src.networking.helpers.utils import send_with_size, recv_by_size
from src.networking.helpers.game_protocol import Protocol
from threading import Lock

world: World = None
lock = Lock()

def collision_exists(player1, player2):
    dist = ((player1.x - player2.x) ** 2 + (player1.y - player2.y) ** 2) ** 0.5
    return dist < max(player1.radius, player2.radius)


class Server:
    """
        TCP Connection

        This server handles all clients added to him automatically (threading)

    """

    def __init__(self, max_waiting, ip='0.0.0.0', port=0):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(max_waiting)
        print(f"Socket addr and port: {self.socket.getsockname()}")
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threads = []


        self.player_update_handler = PlayerUpdateHandler()
        self.edible_update_handler = EdibleUpdateHandler()

        self.player_thread = dict()

        self.collision_detector = CollisionDetector()
        self.collision_detector_thread = threading.Thread(target=self.__handle_collisions, args=())
        self.collision_detector_thread.start()

        self.amount_of_clients = 0

    def __handle_client(self, client_socket, address, thread_id: int):
        # Send first message
        message = Protocol.server_initiate_world((world.width, world.height), world.edibles)
        send_with_size(client_socket, message)
        self.edible_update_handler.make_space_for_new_thread()
        self.collision_detector.players_eaten_helper.make_space_for_thread()

        should_continue = True
        # start getting status updates from the client
        try:
            while should_continue:
                try: 
                    message = recv_by_size(client_socket)  # recieve update
                    player_information, edibles_eaten = Protocol.parse_client_status_update(message)
                except:
                    print("Client disconnected. Terminating thread and player")
                    break
                self.player_thread[player_information.id] = thread_id  # for collision detection

                new_edibles = []
                for edible in edibles_eaten:
                    new_edibles.append(world.delete_edible(edible))

                lock.acquire()

                self.edible_update_handler.notify_threads_changing_edible_status(new_edibles, edibles_eaten, thread_id)
                self.player_update_handler.update_player(player_information)
                other_player_information = self.player_update_handler.get_players(player_information)
                edibles_removed, new_edibles_other = self.edible_update_handler.fetch_thread_specific_edible_updates(
                    thread_id)

                player_eaten_inf = self.collision_detector.players_eaten_helper.get_eaten_status(thread_id)
                rad_increase = player_eaten_inf.get_ate_radius()

                is_eaten = player_eaten_inf.get_killed()
                lock.release()
                if is_eaten:
                    should_continue = False
                new_edibles = new_edibles + new_edibles_other
                send_with_size(client_socket, Protocol.generate_server_status_update(new_edibles, other_player_information,
                                                                                    edibles_removed, rad_increase, is_eaten))
        except:
            print("Thread error, tracing")
            traceback.print_exc()
        # close resources
        lock.acquire() # one last time :/
        self.player_update_handler.remove_player(player_information.id)
        lock.release()

    def __handle_collisions(self):
        saved_collisions = set()
        while True:
            lock.acquire()
            players = self.player_update_handler.get_players()
            collisions = self.__detect_collisions(list(players.values()))
            for collision in collisions:
                if (collision[0].id, collision[1].id) not in saved_collisions:
                    if collision[0].radius > collision[1].radius:
                        eating_thread_id = self.player_thread[collision[0].id]
                        eaten_thread_id = self.player_thread[collision[1].id]
                        self.collision_detector.players_eaten_helper.ate_player(eating_thread_id,
                                                                                players[collision[1].id].radius)
                        self.collision_detector.players_eaten_helper.player_killed(eaten_thread_id)

                        saved_collisions.add((collision[0].id, collision[1].id))
                    else:
                        eating_thread_id = self.player_thread[collision[1].id]
                        eaten_thread_id = self.player_thread[collision[0].id]
                        self.collision_detector.players_eaten_helper.ate_player(eating_thread_id,
                                                                                players[collision[0].id].radius)
                        self.collision_detector.players_eaten_helper.player_killed(eaten_thread_id)
                        saved_collisions.add((collision[0].id, collision[1].id))
            lock.release()

    def __detect_collisions(self, players):
        collisions = []
        for player_information in players:
            for collision_search in players:
                if not (isinstance(collision_search, str) or isinstance(player_information, str)):
                    if player_information.id != collision_search.id and collision_exists(player_information,
                                                                                             collision_search) and player_information.radius != collision_search.radius:
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
    try: 
        global world
        world = World(PlatformConstants.PLATFORM_WIDTH, PlatformConstants.PLATFORM_HEIGHT)
        world.spawn_edibles(EdibleConstants.AMOUNT_OF_EDIBLES)
        print("Accepting Clients....")
        server = Server(2)
    except:
        print("Problem during server initialization, Printing stack trace")
        traceback.print_exc()
        time.sleep(5)
        sys.exit()
    
    try:
        while True:
            # wait for new clients.
            server.accept()
    except:
        print("Critical Server Crash! Printing stack trace")
        traceback.print_exc()
        time.sleep(5)
