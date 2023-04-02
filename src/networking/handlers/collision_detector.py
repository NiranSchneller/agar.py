

"""
    Runs on seperate thread on the server

"""
from src.networking.helpers.players_eaten_helper import PlayersEatenHelper
from src.networking.information.player_information import PlayerInformation




class CollisionDetector:

    def __init__(self):
        self.players_eaten_helper : PlayersEatenHelper = PlayersEatenHelper()
