
import random
from src.networking.encryption.protocol import DHProtocol
from src.networking.helpers.utils import send_with_size, recv_by_size
import socket

LOG_PARAMETERS = True

"""
    Adheres to utils.py protocol
    
    An implementation of the encryption protocol diffie-hellman 
    (https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)

    For the case of simplicity, assume server is "Alice" and client is "Bob" (although it does not matter)
"""


class DiffieHelman():
    def __init__(self, server_side=False) -> None:
        self.server_side = server_side
        self.p = None
        self.g = None

    def key_exchange(self, socket: socket.socket):
        if self.server_side:
            self.__server_side_key_exchange(socket)
        else:
            self.__client_side_key_exchange(socket)

    def __server_side_key_exchange(self, server_socket: socket.socket):  # Alice
        self.p = 2**2048 - 2**224 + 2**192 + 2**96 - 1
        self.g = 2
        send_with_size(
            server_socket, DHProtocol.server_send_pg(self.p, self.g))
        if LOG_PARAMETERS:
            print(f"Server Side params sent: p:{self.p}, g:{self.g}")

        a = DiffieHelman.generate_private_key()  # Range for safe key exchange
        A = (self.g ** a) % self.p

        if LOG_PARAMETERS:
            print(f"Server side A calculation: {A}")
        send_with_size(server_socket, DHProtocol.server_send_A(A))

        bob_B = DHProtocol.server_recieve_B(recv_by_size(server_socket))
        if LOG_PARAMETERS:
            print(f"Server side B Recieved: {bob_B}")

        self.final_secret = (bob_B ** a) % self.p

        if LOG_PARAMETERS:
            print(f"Server Final: {self.final_secret}")

    def __client_side_key_exchange(self, client_socket: socket.socket):  # Bob
        self.p, self.g = DHProtocol.client_recieve_pg(
            recv_by_size(client_socket))

        if LOG_PARAMETERS:
            print(f"Client Side params recieved: p:{self.p}, g:{self.g}")

        alice_A = DHProtocol.client_recieve_A(recv_by_size(client_socket))

        if LOG_PARAMETERS:
            print(f"Client Side A recieved: {alice_A}")

        b = DiffieHelman.generate_private_key()
        B = (self.g ** b) % self.p
        if LOG_PARAMETERS:
            print(f"Client side B calculation: {B}")

        send_with_size(client_socket, DHProtocol.client_send_B(B))

        self.final_secret = (alice_A ** b) % self.p

        if LOG_PARAMETERS:
            print(f"Client Final: {self.final_secret}")

    @staticmethod
    def generate_private_key() -> int:
        return random.randint(10, 20)
