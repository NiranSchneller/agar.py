

from email import message
import socket

from src.networking.helpers.utils import recv_by_size, send_with_size


class DatabaseClient():
    @staticmethod
    def connect_with_socket(ip: str, port: int) -> socket.socket:
        sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))

        return sock

    """
        If registration succeeded, returns True. else, False.
    """
    @staticmethod
    def register(ip: str, port: int, username: str, password: str) -> bool:
        sock = DatabaseClient.connect_with_socket(ip, port)

        send_with_size(sock, f"REGISTER~{username}~{password}")

        messsage = recv_by_size(sock)

        if "FAILED" in messsage:
            sock.close()
            return False
        else:
            sock.close()
            return True

    @staticmethod
    def login(ip: str, port: int, username: str, password: str):
        sock = DatabaseClient.connect_with_socket(ip, port)

        send_with_size(sock, f"LOGIN~{username}~{password}")

        message = recv_by_size(sock)

        if "FAILED" in message:
            sock.close()
            return False
        else:
            sock.close()
            return True
