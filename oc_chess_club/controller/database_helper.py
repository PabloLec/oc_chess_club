from oc_chess_club.models.database import Database
from oc_chess_club.models.player import Player
from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match


class DatabaseHelper:
    """Helper class encapsulating methods to manipulate and transform database objects.

    Attributes:
        database (Database): Instance of database handler database."""

    def __init__(self, database: Database):
        """Constructor for DatabaseHelper.

        Args:
            database (Database): Instance of database handler database.
        """

        self.database = database

    def list_all_matches(self, tournament: Tournament):
        """Lists all matches of a tournament.

        Args:
            tournament (Tournament): Tournament objects to be considered.

        Returns:
            list[tuple[Player]]: List of all matches' player pairing.
        """

        match_list = []

        for round_id in tournament.rounds:
            for match_id in tournament.rounds[round_id].matches:
                player_1 = tournament.rounds[round_id].matches[match_id].player_1
                player_2 = tournament.rounds[round_id].matches[match_id].player_2
                match_list.append((player_1.id_num, player_2.id_num))

        return match_list

    def is_player_id_in_database(self, player_id: int):
        """Verifies if a given player id exists in database.

        Args:
            player_id (int): Player id to verify.

        Returns:
            bool: Player id exists in database.
        """

        if player_id in self.database.players:
            return True
        else:
            return False

    def get_players_by_id(self):
        """Takes a dict of players, typically from a round attribute, and sort them by id.

        Args:
            players (dict): Players to be sorted.

        Returns:
            list:  List og players ordered by id.
        """

        ordered_ids = sorted(self.database.players, key=lambda x: x)

        ordered_players = []
        for id_num in ordered_ids:
            ordered_players.append(self.database.players[id_num])

        return ordered_players

    def player_object_from_id_str(self, player_id: str):
        """Searches through a list of players to find requested player.

        Args:
            player_id (str): Id of player to be searched.

        Returns:
            Player: Requested Player object.
        """

        for player in self.database.players:
            if str(player) == player_id:
                return self.database.players[player]

    def player_name_from_id(self, players: dict, player_id: int):
        """Searches through a dict of players to find requested player's name.

        Args:
            players (dict): Dict of players to search in.
            player_id (int): Id of player to be searched.

        Returns:
            str: Player's first and last name.
        """

        for player in players:
            if players[player].id_num == player_id:
                name = f"{players[player].first_name} {players[player].last_name}"
                return name

    def get_all_tournament_objects(self):
        """Generates a list of all existing tournaments in database.

        Returns:
            list[Tournament]: All existing tournaments in database.
        """

        tournament_list = []

        for tournament_id in self.database.tournaments:
            tournament_list.append(self.database.tournaments[tournament_id])

        return tournament_list

    def get_unfinished_tournaments(self):
        """Searches through the database for unfinished tournament.

        Returns:
            list[Tournament]: Unfinished tournaments.
        """

        unfinished_tournaments = []

        for tournament in self.database.tournaments:
            if not self.database.tournaments[tournament].is_finished:
                unfinished_tournaments.append(self.database.tournaments[tournament])

        return unfinished_tournaments

    def get_all_player_objects(self):
        """Generates a list of all existing players in database.

        Returns:
            list[Player]: All existing players in database.
        """

        players_list = []

        for player_id in self.database.players:
            players_list.append(self.database.players[player_id])

        return players_list
