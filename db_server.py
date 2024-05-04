from typing import Dict
import socket
import threading
import traceback

from src.networking.helpers.utils import recv_by_size, send_with_size
from src.database.database import DatabaseHelper


lock: threading.Lock = threading.Lock()
database_helper: DatabaseHelper = DatabaseHelper()


def accept(server_socket: socket.socket):
    client_socket, address = server_socket.accept()

    client_thread: threading.Thread = threading.Thread(
        target=handle_client, args=(client_socket, address))

    client_thread.start()


"""
    client_socket - the socket that will be used for client communication
"""


def handle_client(client_socket: socket.socket, address: str):
    global database_helper
    print(f"Client addr {address} connected!")
    try:
        message: str = recv_by_size(client_socket)

        mode, username, password = message.split("~")

        success = True

        print(
            f"Client {address} requested {mode}: username:{username}, password:{password}")

        lock.acquire()
        if mode == "REGISTER":
            if database_helper.account_exists(username):
                success = False
            else:
                database_helper.add_account(username, password)
                success = True
        elif mode == "LOGIN":  # Login
            if not database_helper.account_valid(username, password):
                success = False
            else:
                success = True
        else:
            print("Incorrect protocol! ")
            raise ValueError("Incorrect protocol!")
        lock.release()

        if success:  # Good user for database, exit thread
            send_with_size(client_socket, f"{mode}_SUCCESS")
        else:
            send_with_size(client_socket, f"{mode}_FAILED")
    except:
        print(f"error occurred! {traceback.print_exc()}")

    print(f"Thread for client {address} finished.")
    client_socket.close()


if __name__ == "__main__":
    try:
        server_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        server_socket.bind(("0.0.0.0", 0))
        server_socket.listen(2)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(
            f"Database server is on addr: {socket.gethostbyname(socket.gethostname())}:{server_socket.getsockname()[1]}")
    except:
        print(
            f"Problem during database server initiation! {traceback.print_exc()}")
        exit()

    while True:
        accept(server_socket)
