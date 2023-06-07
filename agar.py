import src.networking.client as client
import src.networking.server as server
import pygame
import pygame_menu
pygame.init()
"""
    Runs main.
"""
WIDTH = 1920
HEIGHT = 1080
THEME = pygame_menu.themes.THEME_BLUE
window = None

def set_ip_and_port():
    client_menu = pygame_menu.menu.Menu("Connect", WIDTH, HEIGHT, theme=THEME)
    input_args = {"font_size":80}
    ip = client_menu.add.text_input("IP: ", default="0.0.0.0", **input_args)
    port = client_menu.add.text_input("Port: ", default=0, **input_args)
    name = client_menu.add.text_input("Enter Name: ", default="Johnny", **input_args)
    client_menu.add.vertical_margin(100)
    client_menu.add.button("Connect!", start_client, *(name, ip, port))
    client_menu.mainloop(window)

def main_menu():
    main_menu = pygame_menu.menu.Menu("agar.py!", 1920, 1080, theme=THEME)
    main_menu.add.button("Play", set_ip_and_port).scale(4, 4, False)
    main_menu.add.button("Host", start_server).scale(4, 4, False)
    main_menu.add.button("Quit", pygame.quit).scale(4, 4, False)
    main_menu.mainloop(window)

def death_menu():
    death = pygame_menu.menu.Menu("agar.py!", 1920, 1080, theme=THEME)
    death.add.label("You Died").scale(4,4,False)
    death.add.button("Play Again!", main_menu).scale(4,4,False)
    death.add.button("Quit", pygame.quit).scale(4, 4, False)
    death.mainloop(window)

def start_server():
    pygame.quit()
    server.start()

def start_client(name, ip, port):
    try:
        client.start(name.get_value(), ip.get_value().strip(), int(port.get_value().strip()), window)
    except:
        print("Invalid Parameters!")
        set_ip_and_port()
if __name__ == '__main__':
    window = pygame.display.set_mode((1920, 1080))
    main_menu()
