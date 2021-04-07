from tinydb import TinyDB, Query

from oc_chess_club.models.database import Database
from oc_chess_club.models.player import Player
from oc_chess_club.models.tournament import Tournament


class DatabaseHandler:
    def __init__(self):
        self.database = Database("/home/pablo/openclassrooms/oc_chess_club/oc_chess_club/bdd_test.json")

        self.players_table = None
        self.tournaments_table = None
        self.rounds_table = None
        self.matches_table = None
        self.load_database()

    def load_database(self):
        self.players_table = self.database.db.table("players")
        self.tournaments_table = self.database.db.table("tournaments")
        self.rounds_table = self.database.db.table("rounds")
        self.matches_table = self.database.db.table("matches")

        self.load_players()

    def load_players(self):
        for player in self.players_table:
            self.create_player(
                first_name=player["First Name"],
                last_name=player["Last Name"],
                dob=player["DOB"],
                gender=player["Gender"],
                elo=player["ELO"],
                id_num=player["id"],
            )

    def load_tournaments(self):
        for tournament in self.tournaments_table:
            pass

    def create_player(self, first_name: str, last_name: str, dob: str, gender: str, elo: str, id_num: int = 0):
        player = Player(first_name, last_name, dob, gender, elo, id_num)
        self.database.players.append(player)

    def create_tournament(
        self,
        name: str,
        location: str,
        date: str,
        number_of_rounds: int,
        time_control: str,
        description: str,
        id_num: int = 0,
        is_finished: bool = False,
    ):

        if id_num == 0:
            id_num = self.find_next_id(self.tournaments_table)

        tournament = Tournament(
            name=name,
            location=location,
            date=date,
            number_of_rounds=number_of_rounds,
            time_control=time_control,
            description=description,
            id_num=id_num,
            is_finished=is_finished,
        )
        self.database.tournaments.append(tournament)
        self.save_tournament(tournament)

    def find_next_id(self, table):

        if len(table) == 0:
            return 1

        query = Query()

        biggest = 1

        while len(table.search(query.id >= biggest)) > 0:
            biggest += 1

        return biggest

    def save_element(self, element):
        if type(element) == Tournament:
            self.save_tournament(element)

    def save_tournament(self, tournament):
        query = Query()
        self.tournaments_table.upsert(
            {
                "Name": tournament.name,
                "Location": tournament.location,
                "Date": tournament.date,
                "Number of rounds": int(tournament.number_of_rounds),
                "Time Control": tournament.time_control,
                "Description": tournament.description,
                "Players": tournament.players,
                "Is Finished": tournament.is_finished,
                "id": int(tournament.id_num),
            },
            query.id == int(tournament.id_num),
        )

    def find_unfinished_tournaments(self):
        query = Query()

        result = self.tournaments_table.search(query["Is Finished"] == False)

        return result