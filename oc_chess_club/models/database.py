from tinydb import TinyDB


class Database:
    def __init__(self, location: str):
        self.location = location
        self.players = []
        self.tournaments = None

        self.db = None

    def load_database(self):
        self.db = TinyDB(self.location)
