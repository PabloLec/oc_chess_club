from tinydb import TinyDB, Query

from oc_chess_club.models.database import Database
from oc_chess_club.models.player import Player
from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match
from oc_chess_club.controller.database_helper import DatabaseHelper


class DatabaseHandler:
    def __init__(self):
        self.database = Database("/home/pablo/openclassrooms/oc_chess_club/oc_chess_club/bdd_test.json")
        self.helper = DatabaseHelper()

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
        self.load_tournaments()
        self.load_rounds()
        self.load_matches()

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

    def create_player(self, first_name: str, last_name: str, dob: str, gender: str, elo: str, id_num: int = 0):
        player = Player(first_name, last_name, dob, gender, elo, id_num)
        self.database.players[player.id_num] = player

    def load_tournaments(self):
        for tournament in self.tournaments_table:
            self.create_tournament(
                name=tournament["Name"],
                location=tournament["Location"],
                date=tournament["Date"],
                number_of_rounds=tournament["Number of rounds"],
                time_control=tournament["Time Control"],
                description=tournament["Description"],
                id_num=tournament["id"],
                is_finished=tournament["Is Finished"],
                players=tournament["Players"],
                leaderboard=tournament["Leaderboard"],
            )

    def create_tournament(
        self,
        name: str,
        location: str,
        date: str,
        number_of_rounds: int,
        time_control: str,
        description: str,
        players: list,
        leaderboard: dict = {},
        id_num: int = 0,
        is_finished: bool = False,
    ):

        if id_num == 0:
            id_num = self.find_next_id(self.tournaments_table)

        player_objects = []

        for player in players:
            player_objects.append(self.database.players[player])

        if leaderboard == {}:
            for player in players:
                leaderboard[player] = 0

        tournament = Tournament(
            name=name,
            location=location,
            date=date,
            number_of_rounds=number_of_rounds,
            time_control=time_control,
            description=description,
            id_num=id_num,
            is_finished=is_finished,
            players=player_objects,
            leaderboard=leaderboard,
        )
        self.database.tournaments[tournament.id_num] = tournament
        self.save_tournament(tournament=tournament)

    def load_rounds(self):
        for round_ in self.rounds_table:
            self.create_round(
                round_number=round_["Round number"], tournament_id=round_["Tournament id"], id_num=round_["id"]
            )

    def create_round(
        self,
        round_number: int,
        tournament_id: int,
        id_num: int = 0,
    ):
        if id_num == 0:
            id_num = self.find_next_id(self.rounds_table)

        created_round = Round(round_number=round_number, tournament_id=tournament_id, id_num=id_num)

        # self.database.rounds[created_round.id_num] = created_round
        self.database.tournaments[created_round.tournament_id].rounds[id_num] = created_round
        self.save_round(round_=created_round)

        return id_num

    def load_matches(self):
        for match in self.matches_table:

            player_1 = self.database.players[match["Player 1"]]
            player_2 = self.database.players[match["Player 2"]]

            players = (player_1, player_2)

            self.create_match(
                players=players,
                tournament_id=match["Tournament id"],
                round_id=match["Round id"],
                winner=match["Winner"],
                id_num=match["id"],
            )

    def create_match(self, players: tuple, tournament_id: int, round_id: int, winner: int, id_num: int = 0):
        if id_num == 0:
            id_num = self.find_next_id(self.matches_table)

        match = Match(players=players, tournament_id=tournament_id, round_id=round_id, winner=winner, id_num=id_num)

        # self.database.matches[match.id_num] = match
        self.database.tournaments[match.tournament_id].rounds[round_id].matches[id_num] = match
        self.save_match(match=match)

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

    def save_tournament(self, tournament: Tournament):
        query = Query()

        players_id = []

        for player in tournament.players:
            players_id.append(player.id_num)

        self.tournaments_table.upsert(
            {
                "Name": tournament.name,
                "Location": tournament.location,
                "Date": tournament.date,
                "Number of rounds": int(tournament.number_of_rounds),
                "Time Control": tournament.time_control,
                "Description": tournament.description,
                "Players": players_id,
                "Leaderboard": tournament.leaderboard,
                "Is Finished": tournament.is_finished,
                "id": int(tournament.id_num),
            },
            query.id == int(tournament.id_num),
        )

    def save_round(self, round_: Round):
        query = Query()

        self.rounds_table.upsert(
            {
                "Round number": round_.round_number,
                "Tournament id": int(round_.tournament_id),
                "id": int(round_.id_num),
            },
            query.id == int(round_.id_num),
        )

    def save_match(self, match: Match):
        query = Query()

        self.matches_table.upsert(
            {
                "Player 1": match.player_1.id_num,
                "Player 2": match.player_2.id_num,
                "Winner": match.winner,
                "Tournament id": int(match.tournament_id),
                "Round id": int(match.round_id),
                "id": int(match.id_num),
            },
            query.id == int(match.id_num),
        )

    def update_leaderboard(self, tournament_id: int, player_id: int, points_earned: float):
        tournament = self.database.tournaments[tournament_id]
        tournament.leaderboard[str(player_id)] += points_earned
        self.save_tournament(tournament=tournament)

    def find_unfinished_tournaments(self):
        query = Query()

        result = self.tournaments_table.search(query["Is Finished"] == False)

        return result


_DATABASE_HANDLER = DatabaseHandler()