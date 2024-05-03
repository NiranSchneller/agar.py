from typing import List
from src.edible import Edible
from src.networking.information.player_information import PlayerInformation

class WorldInformation:

    def __init__(self):
        self.width: int = 0
        self.height: int = 0
        self.edibles: List[Edible] = []
        self.players: List[PlayerInformation] = []

    def initiate_edibles(self, edibles: List[Edible]):
        self.edibles = edibles

    def __add_edible(self, edible: Edible):
        self.edibles.append(edible)

    def add_edibles(self, edibles: List[Edible]):
        for edible in edibles:
            self.__add_edible(edible)

    def remove_edibles(self, edibles_removed: List[Edible]):
        for edible in edibles_removed:
            self.edibles.remove(edible)

    def set_players(self, other_players: List[PlayerInformation]):
        self.players = other_players
