from typing import List
from src.networking.information.players_eaten_information import PlayersEatenInformation


"""
    Class is used by collision detector to store info for each thread
"""
class PlayersEatenHelper:

    def __init__(self):
        self.handler_list: List[PlayersEatenInformation] = []

    def make_space_for_thread(self):
        self.handler_list.append(PlayersEatenInformation())

    def ate_player(self, thread_id: int, eaten_radius: float):
        self.handler_list[thread_id].ate_player(eaten_radius)

    def player_killed(self, thread_id: int):
        self.handler_list[thread_id].killed()

    def get_eaten_status(self, thread_id: int) -> PlayersEatenInformation:
        return self.handler_list[thread_id]

