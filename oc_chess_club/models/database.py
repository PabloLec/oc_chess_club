from tinydb import TinyDB


class Database:
    def __init__(self, location: str):
        self.location = location
        self.players = {}
        self.tournaments = {}
        self.rounds = {}
        self.matches = {}

        self.db = None
        self.load_database()

    def load_database(self):
        self.db = TinyDB(self.location)
