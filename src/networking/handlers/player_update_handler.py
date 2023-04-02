from src.networking.information.player_information import PlayerInformation

""" 
    This class holds a dict that has the information about all the players in the map
"""


class PlayerUpdateHandler:

    def __init__(self):
        self.players_dict = dict()

    def update_player(self, player_information: PlayerInformation):
        self.players_dict[player_information.name] = player_information

    """
        Returns the information about all of the players except player given as parameter
        
        If nothing in dict returns -> []
    """

    def get_players(self, player_information: PlayerInformation = None):
        if player_information is None:
            return self.players_dict
        return [v for k, v in self.players_dict.items() if k != player_information.name and not isinstance(v, str)]

    def remove_player(self, player_name):
        self.players_dict[player_name] = "KILLED"
