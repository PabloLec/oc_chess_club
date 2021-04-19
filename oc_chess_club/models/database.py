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

    def create_empty_database():
        """Creates an empty database JSON file if needed."""

        with open(self.location, "w+") as f:
            f.write("{}")

    def load_database(self):
        """Loads a TinyDB object from a JSON file."""

        try:
            self.db = TinyDB(self.location)
        except FileNotFoundError:
            self.create_empty_database()
            self.load_database()
