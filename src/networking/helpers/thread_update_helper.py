"""
    Stores reliable information for thread to use.
    used by: edible_update_handler
"""


class ThreadUpdateHelper:

    def __init__(self):
        self.edibles_created = []
        self.edibles_removed = []

    def update_edibles_removed(self, edibles_removed):
        for edible in edibles_removed:
            self.edibles_removed.append(edible)

    def update_edibles_created(self, edibles_created):
        for edible in edibles_created:
            self.edibles_created.append(edible)

    def update_edible_statuses(self, edibles_created, edibles_removed):
        self.update_edibles_removed(edibles_removed)
        self.update_edibles_created(edibles_created)

    """
        To be used by the thread, will clear the list
    """
    def fetch_edibles_removed(self):
        edibles_removed = self.edibles_removed.copy()
        self.edibles_removed.clear()
        return edibles_removed


    def fetch_edibles_created(self):
        edibles_created = self.edibles_created.copy()
        self.edibles_created.clear()
        return edibles_created