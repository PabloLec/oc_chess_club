from tinydb import TinyDB


class Database:
    """Model for database, encapsulates a TinyDB object and the created objects.

    Attributes:
        location (str): The local path for the TinyDB JSON file.
        players (dict): The Player objects created from the database.
        tournaments (dict): The tournament objects created from the database.
        db (tinydb.database.TinyDB): The TinyDB object created from the JSON file.
    """

    def __init__(self, location: str):
        """Constructor for Database. Initiates TinyDB loading.

        Args:
            location (str): The local path for the TinyDB JSON file.
        """

        self.location = location
        self.players = {}
        self.tournaments = {}

        self.db = None
        self.load_database()

    def load_database(self):
        """Loads a TinyDB object from a JSON file."""

        self.db = TinyDB(self.location)
