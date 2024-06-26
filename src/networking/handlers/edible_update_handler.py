


"""
    Handles updating each thread about changing status of edibles
    Every thread has an index in the array from which it pulls the relevant edible information
"""
from typing import List, Tuple
from src.edible import Edible
from src.networking.helpers.thread_update_helper import ThreadUpdateHelper

class EdibleUpdateHandler:

    def __init__(self):
        self.edible_updates: List[ThreadUpdateHelper] = []

    def make_space_for_new_thread(self):
        self.edible_updates.append(ThreadUpdateHelper())

    """
        Adds to the indices of all OTHER threads that they should update the client about the edibles
    """
    def notify_threads_changing_edible_status(self, edibles_created, edibles_removed, thread_id):
        if edibles_created or edibles_removed:
            print(f"Notifying all other threads of edibles status, current thread: {thread_id}")
        for i in range(len(self.edible_updates)):
            if i != thread_id:
                self.edible_updates[i].update_edible_statuses(edibles_created, edibles_removed)

    """
        Fetches for the thread required information about the edibles created and removed by other players
    """
    def fetch_thread_specific_edible_updates(self, thread_id: int) -> Tuple[List[Edible], List[Edible]]:
        return self.edible_updates[thread_id].fetch_edibles_removed(), self.edible_updates[thread_id].fetch_edibles_created()
