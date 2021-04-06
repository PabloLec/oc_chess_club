from tinydb import TinyDB, Query

from oc_chess_club.models.database import Database
from oc_chess_club.models.player import Player


class DatabaseHandler:
    def __init__(self):
        self.database = Database("/home/pablo/openclassrooms/oc_chess_club/oc_chess_club/bdd_test.json")
        self.database.load_database()

        self.load_players()

    def load_players(self):
        players = self.database.db.all()
        for player in players:
            self.create_player(
                first_name=player["First Name"],
                last_name=player["Last Name"],
                dob=player["DOB"],
                gender=player["Gender"],
                elo=player["ELO"],
                id_num=player["id"],
            )

    def create_player(self, first_name: str, last_name: str, dob: str, gender: str, elo: str, id_num: int):
        player = Player(first_name, last_name, dob, gender, elo, id_num)
        self.database.players.append(player)
