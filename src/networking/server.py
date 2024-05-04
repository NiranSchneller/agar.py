import sys
import threading
from typing import Dict, List

from src.networking.encryption.aes import AES
from src.networking.encryption.diffie_hellman import DiffieHelman
from src.networking.information.player_information import PlayerInformation
from src.networking.information.players_eaten_information import PlayersEatenInformation
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
world: World = None  # type: ignore
lock: Lock = Lock()


def collision_exists(player1, player2):
    dist = ((player1.x - player2.x) ** 2 + (player1.y - player2.y) ** 2) ** 0.5
    return dist < max(player1.radius, player2.radius)


class Server:
    """
    TCP Connection

    This server class manages client connections asynchronously.
    It provides methods for accepting client connections and handling client communication
    in separate threads.

    Attributes:
    - socket (socket.socket): The server socket object used for accepting client connections.
    - threads (List[threading.Thread]): A list of threads spawned to handle client connections.
    - player_update_handler (PlayerUpdateHandler): An instance of PlayerUpdateHandler for managing player updates.
    - edible_update_handler (EdibleUpdateHandler): An instance of EdibleUpdateHandler for managing edible updates.
    - player_thread (dict): A dictionary mapping player IDs to thread IDs.
    - diffie_hellman (DiffieHelman): An instance of DiffieHelman for secure communication.
    - collision_detector (CollisionDetector): An instance of CollisionDetector for detecting player collisions.
    - collision_detector_thread (threading.Thread): A thread for handling collision detection.
    - amount_of_clients (int): The number of connected clients.
    """

    def __init__(self, max_waiting: int, ip: str = '0.0.0.0', port: int = 0):
        self.socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((ip, port))
        self.socket.listen(max_waiting)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(
            f"Socket addr and port: {socket.gethostbyname(socket.gethostname())}:{self.socket.getsockname()[1]}")

        self.threads: List[threading.Thread] = []

        self.player_update_handler: PlayerUpdateHandler = PlayerUpdateHandler()
        self.edible_update_handler: EdibleUpdateHandler = EdibleUpdateHandler()

        self.player_thread: dict = dict()

        self.diffie_hellman = DiffieHelman(True)

        self.collision_detector: CollisionDetector = CollisionDetector()
        self.collision_detector_thread: threading.Thread = threading.Thread(
            target=self.__handle_collisions, args=())
        self.collision_detector_thread.start()

        self.amount_of_clients: int = 0

    def __handle_client(self, client_socket: socket.socket, address: str, thread_id: int):
        """
        Handles communication with a connected client in a separate thread.

        This method is called by the accept function to manage communication with a client
        connected to the server. It performs key exchange, sends initial messages, and
        continuously receives and processes status updates from the client.

        Parameters:
        - client_socket (socket.socket): The socket object used to communicate with the client.
        - address (str): The address of the client.
        - thread_id (int): The ID of the thread handling the client connection.

        Returns:
        None

        Uses:
        - Diffie-Hellman key exchange for secure communication.
        - AES encryption for encrypting and decrypting messages.
        - Protocol module for defining message formats and communication protocols.
        - Threading module for handling client communication in separate threads.
        - Locking mechanism for thread safety.
        - PlayerUpdateHandler, EdibleUpdateHandler, and CollisionDetector for updating game state.
        - World object for accessing game world information.
        """
        self.diffie_hellman.key_exchange(client_socket)
        aes: AES = AES(self.diffie_hellman.final_secret)

        # Send first message
        message: str = Protocol.server_initiate_world(
            (world.width, world.height), world.edibles)

        send_with_size(client_socket, aes.encrypt(message))

        self.edible_update_handler.make_space_for_new_thread()
        self.collision_detector.players_eaten_helper.make_space_for_thread()

        should_continue = True
        # start getting status updates from the client
        try:
            while should_continue:
                try:
                    message: bytes = recv_by_size(
                        client_socket, return_type="bytes")  # recieve update
                    message: str = aes.decrypt(message)
                    player_information, edibles_eaten = Protocol.parse_client_status_update(
                        message)
                except:
                    print("Client disconnected. Terminating thread and player")
                    break
                # for collision detection
                self.player_thread[player_information.id] = thread_id

                new_edibles = []
                for edible in edibles_eaten:
                    new_edibles.append(world.delete_edible(edible))

                lock.acquire()

                self.edible_update_handler.notify_threads_changing_edible_status(
                    new_edibles, edibles_eaten, thread_id)

                self.player_update_handler.update_player(player_information)

                other_player_information: List[PlayerInformation] = self.player_update_handler.get_players(
                    player_information)  # type: ignore

                edibles_removed, new_edibles_other = self.edible_update_handler.fetch_thread_specific_edible_updates(
                    thread_id)

                player_eaten_inf: PlayersEatenInformation = \
                    self.collision_detector.players_eaten_helper.get_eaten_status(
                        thread_id)

                rad_increase = player_eaten_inf.get_ate_radius()
                is_eaten = player_eaten_inf.get_killed()

                lock.release()

                if is_eaten:
                    should_continue = False

                new_edibles = new_edibles + new_edibles_other
                send_update = Protocol.generate_server_status_update(new_edibles, other_player_information,
                                                                     edibles_removed,
                                                                     rad_increase, is_eaten)

                send_with_size(client_socket, aes.encrypt(send_update))
        except:
            print("Thread error, tracing")
            traceback.print_exc()
        # close resources
        lock.acquire()  # one last time :/
        self.player_update_handler.remove_player(player_information.id)
        lock.release()

    def __collide(self, eating_thread_id: int, eaten_thread_id: int, eaten_radius: float) -> None:
        self.collision_detector.players_eaten_helper.ate_player(
            eating_thread_id, eaten_radius)
        self.collision_detector.players_eaten_helper.player_killed(
            eaten_thread_id)

    def __handle_collisions(self):
        """
        Detects and handles collisions between players.

        This method is responsible for detecting collisions between players and handling
        the consequences of these collisions, such as updating player states or triggering
        specific actions.

        Parameters:
        None

        Returns:
        None

        Uses:
        - PlayerUpdateHandler: to retrieve player information.
        - __detect_collisions method: to detect collisions between players.
        - __collide method: to handle individual collisions.
        - Locking mechanism (lock): for thread safety.
        """
        saved_collisions = set()
        while True:
            lock.acquire()
            # type: ignore
            players: Dict[str, PlayerInformation] = self.player_update_handler.get_players(
            )
            collisions = self.__detect_collisions(list(players.values()))
            for collision in collisions:
                if (collision[0].id, collision[1].id) not in saved_collisions:
                    if collision[0].radius > collision[1].radius:
                        self.__collide(
                            self.player_thread[collision[0].id],
                            self.player_thread[collision[1].id], players[collision[1].id].radius)

                        saved_collisions.add(
                            (collision[0].id, collision[1].id))
                    else:
                        self.__collide(
                            self.player_thread[collision[1].id],
                            self.player_thread[collision[0].id], players[collision[0].id].radius)

                        saved_collisions.add(
                            (collision[0].id, collision[1].id))
            lock.release()

    def __detect_collisions(self, players):
        """
        Detects collisions between players.

        This method iterates over the provided list of player information and identifies
        pairs of players that are in collision with each other.

        Parameters:
        - players (list): A list of PlayerInformation objects representing players.

        Returns:
        list: A list of tuples representing pairs of players involved in collisions.

        Uses:
        - collision_exists function: to determine if two players are in collision with each other.
        """
        collisions = []
        for player_information in players:
            for collision_search in players:
                if (not isinstance(collision_search, str)) and \
                        (not isinstance(player_information, str)):

                    # Handle "EATEN"
                    if player_information.id != collision_search.id \
                            and collision_exists(player_information, collision_search) and \
                            player_information.radius != collision_search.radius:
                        collisions.append(
                            (player_information, collision_search))
        return collisions

    def accept(self):
        """
        Accepts a new client connection and handles it in a separate thread.

        This method waits for a new client to connect to the server socket. Once a client
        connection is established, the client's socket and address are obtained. A new thread
        is then created to handle the client connection using the __handle_client method.

        Parameters:
        None

        Returns:
        None
        """
        client_socket, address = self.socket.accept()
        t = threading.Thread(target=self.__handle_client, args=(
            client_socket, address, self.amount_of_clients))
        t.start()
        self.threads.append(t)
        self.amount_of_clients += 1


def start():
    try:
        global world
        world = World(PlatformConstants.PLATFORM_WIDTH,
                      PlatformConstants.PLATFORM_HEIGHT)
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
