from tinydb import TinyDB, Query, table

from oc_chess_club.models.database import Database
from oc_chess_club.models.player import Player
from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match
from oc_chess_club.controller.database_helper import DatabaseHelper


class DatabaseHandler:
    """Handles all operations related to the database including loading, creating and saving the different elements.

    Attributes:
        database (Database): Object encapsulating the database in TinyDB format and usable tournament related objects.
        helper (DatabaseHelper): Object with helper methods to manipulate and transform db objects.
        players_table (table.Table): Instance of TinyDB "Players" Table.
        tournaments_table (table.Table): Instance of TinyDB "Tournaments" Table.
        rounds_table (table.Table): Instance of TinyDB "Rounds" Table.
        matches_table (table.Table): Instance of TinyDB "Matches" Table.
    """

    def __init__(self):
        """Constructor for DatabaseHandler Class. Initiates database loading."""

        self.database = Database("/home/pablo/openclassrooms/oc_chess_club/oc_chess_club/bdd_test.json")
        self.helper = DatabaseHelper()

        self.players_table = None
        self.tournaments_table = None
        self.rounds_table = None
        self.matches_table = None
        self.load_database()

    def load_database(self):
        """Instantiates the different tables as object attributes and loads their content by creating corresponding objects."""

        self.players_table = self.database.db.table("players")
        self.tournaments_table = self.database.db.table("tournaments")
        self.rounds_table = self.database.db.table("rounds")
        self.matches_table = self.database.db.table("matches")

        self.load_players()
        self.load_tournaments()
        self.load_rounds()
        self.load_matches()

    def load_players(self):
        """Uses TinyDB "Players" table to create Player objects."""

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
        """Creates a Player object and saves it into Database attributes.

        Args:
            first_name (str): Player's first name.
            last_name (str): Player's last name.
            dob (str): Player's date of birth.
            gender (str): Player's gender.
            elo (str): Player's ELO ranking.
            id_num (int, optional): Player's id. Defaults to 0.
        """

        if id_num == 0:
            id_num = self.find_next_id(self.players_table)

        player = Player(first_name, last_name, dob, gender, elo, id_num)
        self.database.players[player.id_num] = player

    def save_player(self, player: Player):
        """Saves a Player object to TinyDB.

        Args:
            player (Player): Player object to be saved.
        """
        # TO DO
        pass

    def load_tournaments(self):
        """Uses TinyDB "Tournaments" table to create Player objects."""

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
        players: list[int],
        leaderboard: dict,
        id_num: int = 0,
        is_finished: bool = False,
    ):
        """Creates a Tournament object and saves it into Database attributes.

        Args:
            name (str): Tournament's name.
            location (str): Tournament's physical location.
            date (str): Tournament's date.
            number_of_rounds (int): Number of rounds to be played.
            time_control (str): Type of time control chosen.
            description (str): Tournament's description.
            players (list[int]): Participating players ids.
            leaderboard (dict): Tournament's leaderboard.
            id_num (int, optional): Tournament's id. Defaults to 0.
            is_finished (bool, optional): Is tournament finished.. Defaults to False.

        Returns:
            int: Created tournament's id.
        """

        if id_num == 0:
            id_num = self.find_next_id(self.tournaments_table)

        player_objects = []

        for player in players:
            player_objects.append(self.database.players[player])

        if len(leaderboard) == 0:
            for player in players:
                leaderboard[str(player)] = 0

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

        self.save_tournament(tournament=tournament)

        return id_num

    def save_tournament(self, tournament: Tournament):
        """Saves a Tournament object to TinyDB.

        Args:
            tournament (Tournament): Tournament object to be saved.
        """

        self.database.tournaments[tournament.id_num] = tournament

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

    def load_rounds(self):
        """Uses TinyDB "Rounds" table to create Player objects."""

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
        """Creates a Round object and saves it into Database attributes.

        Args:
            round_number (int): Ordered round number.
            tournament_id (int): Round's tournament id.
            id_num (int, optional): Round id. Defaults to 0.

        Returns:
            int: Created round id.
        """

        if id_num == 0:
            id_num = self.find_next_id(self.rounds_table)

        created_round = Round(round_number=round_number, tournament_id=tournament_id, id_num=id_num)

        self.save_round(round_=created_round)

        return id_num

    def save_round(self, round_: Round):
        """Saves a Round object to TinyDB.

        Args:
            round_ (Round): Round object to be saved. Underscore added because of reserved keyword.
        """

        self.database.tournaments[round_.tournament_id].rounds[round_.id_num] = round_

        query = Query()

        self.rounds_table.upsert(
            {
                "Round number": round_.round_number,
                "Tournament id": int(round_.tournament_id),
                "id": int(round_.id_num),
            },
            query.id == int(round_.id_num),
        )

    def load_matches(self):
        """Uses TinyDB "Matches" table to create Player objects."""

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
        """Creates a Match object and saves it into Database attributes.

        Args:
            players (tuple): Tuple of the two facing players.
            tournament_id (int): Match's tournament id.
            round_id (int): Match's round id..
            winner (int): Match's winner. Either 1 (first player), 2 (second player) or 0 (draw).
            id_num (int, optional): Match's id. Defaults to 0.
        """

        if id_num == 0:
            id_num = self.find_next_id(self.matches_table)

        match = Match(players=players, tournament_id=tournament_id, round_id=round_id, winner=winner, id_num=id_num)

        self.save_match(match=match)

    def save_match(self, match: Match):
        """Saves a Match object to TinyDB.

        Args:
            match (Match): Match object to be saved.
        """

        self.database.tournaments[match.tournament_id].rounds[match.round_id].matches[match.id_num] = match

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

    def find_next_id(self, table: table.Table):
        """Searches through a TinyDB table for the next biggest id number.

        Args:
            table (table.Table): TinyDB table to search in.

        Returns:
            int: Next biggest id to be used.
        """

        if len(table) == 0:
            return 1

        query = Query()

        biggest = 1

        while len(table.search(query.id >= biggest)) > 0:
            biggest += 1

        return biggest

    def update_leaderboard(self, tournament_id: int, player_id: int, points_earned: float):
        """Updates a tournament's leaderboard by adding points to a player.

        Args:
            tournament_id (int): Tounament's id.
            player_id (int): Player's id.
            points_earned (float): Points earned by the player.
        """

        tournament = self.database.tournaments[tournament_id]
        tournament.leaderboard[str(player_id)] += points_earned
        self.save_tournament(tournament=tournament)

    def find_unfinished_tournaments(self):
        """Searches through the Tournaments table for unfinished tournament.

        Returns:
            list[table.Document]: Unfinished tournaments.
        """

        query = Query()

        result = self.tournaments_table.search(query["Is Finished"] == False)

        return result


_DATABASE_HANDLER = DatabaseHandler()