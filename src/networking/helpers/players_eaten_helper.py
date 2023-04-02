from src.networking.information.players_eaten_information import PlayersEatenInformation


"""
    Class is used by collision detector to store info for each thread
"""
class PlayersEatenHelper:

    def __init__(self):
        self.handler_list: [PlayersEatenInformation] = []

    def make_space_for_thread(self):
        self.handler_list.append(PlayersEatenInformation())

    def ate_player(self, thread_id, eaten_radius):
        self.handler_list[thread_id].ate_player(eaten_radius)

    def player_killed(self, thread_id):
        self.handler_list[thread_id].killed()

    def get_eaten_status(self, thread_id):
        return self.handler_list[thread_id]

