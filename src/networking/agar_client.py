
import socket
import sys
import threading
import uuid


from src.networking.encryption.aes import AES
from src.networking.helpers.world_information import WorldInformation
from src.networking.encryption.diffie_hellman import DiffieHelman
from src.constants import PlayerConstants
from src.networking.helpers import game_protocol
from src.edible import Edible
from src.networking.information.player_information import PlayerInformation
from src.networking.helpers.game_protocol import Protocol
from src.networking.helpers.utils import recv_by_size, send_with_size
from typing import List


class Client:
    def __init__(self, host: str, port: int, world_information: WorldInformation,
                 player_information: PlayerInformation, player_camera, player):
        self.socket: socket.socket = socket.socket()
        self.thread: threading.Thread = None  # type: ignore
        try:
            self.socket.connect((host, port))
            print("Connected")
        except:
            print("Connection error, please check ip or port!")
            sys.exit()

        self.diffie_hellman = DiffieHelman()
        # To Handle sending data
        self.world_information: WorldInformation = world_information
        self.player_information: PlayerInformation = player_information
        self.edible_eaten_list: List[Edible] = list()
        self.player_camera = player_camera
        self.player = player
        self.running = True

    """
        Starts recieving and sending messages, opens a seperate thread
    """

    def start_client(self):
        self.diffie_hellman.key_exchange(self.socket)
        aes: AES = AES(self.diffie_hellman.final_secret)

        message: str = aes.decrypt(recv_by_size(
            self.socket, return_type="bytes"))
        world_size, edibles = game_protocol.Protocol.parse_server_initiate_world(
            message)
        self.world_information.initiate_edibles(edibles)
        self.world_information.width, self.world_information.height = world_size  # type: ignore

        self.thread = threading.Thread(
            target=self.__handle_connection, args=(aes,))
        self.thread.start()

    """
        Main client func, communicates with the server and updates the server on relevant information
    """

    def __handle_connection(self, aes):
        unique_id = uuid.uuid4().hex

        while self.running:
            message = Protocol.generate_client_status_update(self.player_information.x, self.player_information.y,
                                                             self.player_information.radius,
                                                             self.player_information.name,
                                                             unique_id,
                                                             self.edible_eaten_list.copy())
            self.edible_eaten_list.clear()

            # update the server on relevant information
            send_with_size(self.socket, aes.encrypt(message))
            server_reply = aes.decrypt(recv_by_size(
                self.socket, return_type="bytes"))

            if Protocol.parse_server_status_update(server_reply) == "EATEN":
                self.running = False
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

                self.player.radius += ate_inc  # type: ignore
                self.player_camera.edible_eaten(self.player.radius / PlayerConstants.PLAYER_STARTING_RADIUS,
                                                self.player.radius / PlayerConstants.PLAYER_STARTING_RADIUS)

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
