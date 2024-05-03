from src.database.database_client import DatabaseClient
from src.constants import PlayerCameraConstants
from src.database.database import DatabaseHelper
import src.networking.client as client
import src.networking.server as server
import pygame
import pygame_menu
import traceback
pygame.init()
"""
    Runs main.
"""
WIDTH = PlayerCameraConstants.SCREEN_WIDTH
HEIGHT = PlayerCameraConstants.SCREEN_HEIGHT
THEME = pygame_menu.themes.THEME_BLUE  # type: ignore
window = None
database = None


def set_ip_and_port():
    try:
        client_menu = pygame_menu.menu.Menu(
            "Connect", WIDTH, HEIGHT, theme=THEME)  # type: ignore
        input_args = {"font_size": 80}
        ip = client_menu.add.text_input(
            "IP: ", default="0.0.0.0", **input_args)
        port = client_menu.add.text_input("Port: ", default=0, **input_args)
        name = client_menu.add.text_input(
            "Enter Name: ", default="Johnny", **input_args)
        client_menu.add.vertical_margin(100)
        client_menu.add.button("Connect!", start_client, *(name, ip, port))
        client_menu.mainloop(window)
    except:
        print("Menu Crashed!")


def login_menu():
    try:
        login_menu = pygame_menu.menu.Menu("Login", WIDTH, HEIGHT, theme=THEME)
        input_args = {"font_size": 80}

        db_ip = login_menu.add.text_input(
            "Database IP:", default="0.0.0.0", **input_args
        )

        db_port = login_menu.add.text_input(
            "Database port:", default="0.0.0.0", **input_args)

        username = login_menu.add.text_input(
            "Username: ", default="username", **input_args)

        password = login_menu.add.text_input(
            "Password: ", default="password", **input_args)

        login_menu.add.vertical_margin(100)

        login_menu.add.button("Log in", check_login_info, *
                              (db_ip, db_port, username, password)).scale(4, 4, False)

        login_menu.add.button("Register", check_register_info,
                              *(db_ip, db_port, username, password)).scale(4, 4, False)

        login_menu.mainloop(window)
    except:
        print(f"Exception! {traceback.print_exc()}")


def main_menu():
    try:
        print("dsadasdsasad")
        main_menu = pygame_menu.menu.Menu(
            "agar.py!", WIDTH, HEIGHT, theme=THEME)  # type: ignore
        main_menu.add.button("Play", set_ip_and_port).scale(4, 4, False)
        main_menu.add.button("Host", start_server).scale(4, 4, False)
        main_menu.add.button("Quit", pygame.quit).scale(4, 4, False)
        main_menu.mainloop(window)
    except:
        print("Menu Crashed!")


def death_menu():
    try:
        death = pygame_menu.menu.Menu(
            "agar.py!", WIDTH, HEIGHT, theme=THEME)  # type: ignore
        death.add.label("You Died!").scale(4, 4, False)
        death.add.button("Play Again!", main_menu).scale(3, 3, False)
        death.add.button("Quit", pygame.quit).scale(3, 3, False)
        death.mainloop(window)
    except:
        print("Menu Crashed!")


def start_server():
    pygame.quit()
    server.start()


def start_client(name, ip, port):
    try:
        client.start(name.get_value(), ip.get_value().strip(), int(
            port.get_value().strip()), window)  # type: ignore
    except:
        print("Invalid Parameters!")
        set_ip_and_port()
    death_menu()


def check_login_info(db_ip, db_port, username, password):
    db_ip = db_ip.get_value()
    db_port = int(db_port.get_value())
    username = username.get_value()  # By reference
    password = password.get_value()
    if not DatabaseClient.login(db_ip, db_port, username, password):
        print("Account not valid")
        login_menu()
        return
    main_menu()


def check_register_info(db_ip, db_port, username, password):
    db_ip = db_ip.get_value()
    db_port = int(db_port.get_value())
    username = username.get_value()  # By reference
    password = password.get_value()
    print(f"Register Info: {username}, {password}")
    if not DatabaseClient.register(db_ip, db_port, username, password):
        print("Account already exists!")
        login_menu()
        return
    database.add_account(username, password)
    main_menu()


if __name__ == '__main__':
    try:
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        database = DatabaseHelper()
        login_menu()
    except:
        print(f"Menu Crashed! trace: {traceback.print_exc()}")
