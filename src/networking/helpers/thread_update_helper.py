"""
    Stores reliable information for thread to use.
    used by: edible_update_handler
"""


from typing import List
from src.edible import Edible


class ThreadUpdateHelper:

    def __init__(self):
        self.edibles_created: List[Edible] = []
        self.edibles_removed: List[Edible] = []

    def update_edibles_removed(self, edibles_removed: List[Edible]):
        for edible in edibles_removed:
            self.edibles_removed.append(edible)

    def update_edibles_created(self, edibles_created: List[Edible]):
        for edible in edibles_created:
            self.edibles_created.append(edible)

    def update_edible_statuses(self, edibles_created: List[Edible], edibles_removed: List[Edible]):
        self.update_edibles_removed(edibles_removed)
        self.update_edibles_created(edibles_created)

    """
        To be used by the thread, will clear the list
    """
    def fetch_edibles_removed(self) -> List[Edible]:
        edibles_removed = self.edibles_removed.copy()
        self.edibles_removed.clear()
        return edibles_removed


    def fetch_edibles_created(self) -> List[Edible]:
        edibles_created = self.edibles_created.copy()
        self.edibles_created.clear()
        return edibles_created