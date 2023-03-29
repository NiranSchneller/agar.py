import networking.client as client
import networking.server as server
"""
    Runs main.
"""
if __name__ == '__main__':
    if input("Enter client/server:") == 'client':
        client.start(1920, 1080)
    else:
        server.start()