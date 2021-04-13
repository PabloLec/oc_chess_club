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

    def is_tournament_db_empty(self):
        """Verifies if there is no tournament in database.

        Returns:
            bool: No tournament in database.
        """

        if len(self.database.tournaments) == 0:
            return True
        else:
            return False

    def is_player_db_empty(self):
        """Verifies if there is no player in database.

        Returns:
            bool: No player in database.
        """

        if len(self.database.players) == 0:
            return True
        else:
            return False

    def is_tournament_id_in_database(self, tournament_id: int):
        """Verifies if a given tournament id exists in database.

        Args:
            tournament_id (int): Tournament id to verify.

        Returns:
            bool: Tournament id exists in database.
        """

        if tournament_id in self.database.tournaments:
            return True
        else:
            return False

    def is_player_id_in_database(self, player_id: int):
        """Verifies if a given player id exists in database.

        Args:
            player_id (int): Player id to verify.

        Returns:
            bool: Player id exists in database.
        """

        if player_id in self.database.players:
            if self.database.players[player_id].is_deleted:
                return False
            else:
                return True
        else:
            return False

    def get_all_matches(self, tournament: Tournament):
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

    def get_players_by_name(self, players_sample: dict = None):
        """Lists all players in sample by name.

        Args:
            players_sample (dict, optional): Sample to search in. Defaults to None.

        Returns:
            list:  List of all players ordered by ELO name.
        """

        if players_sample is None:
            players_sample = self.database.players

        print(players_sample)

        ordered_ids = sorted(players_sample, key=lambda x: players_sample[x].last_name)

        ordered_players = []
        for id_num in ordered_ids:
            if self.database.players[id_num].is_deleted:
                continue
            ordered_players.append(self.database.players[id_num])

        return ordered_players

    def get_players_by_elo(self, players_sample: dict = None):
        """Lists all players in sample by ELO ranking.

        Args:
            players_sample (dict, optional): Sample to search in. Defaults to None.

        Returns:
            list:  List of all players ordered by ELO ranking.
        """

        if players_sample is None:
            players_sample = self.database.players

        ordered_ids = sorted(players_sample, key=lambda x: players_sample[x].elo, reverse=True)

        ordered_players = []
        for id_num in ordered_ids:
            if self.database.players[id_num].is_deleted:
                continue
            ordered_players.append(self.database.players[id_num])

        return ordered_players

    def get_players_by_id(self):
        """Lists all database players sorted by id.

        Returns:
            list:  List of all players ordered by id.
        """

        ordered_ids = sorted(self.database.players, key=lambda x: x)

        ordered_players = []
        for id_num in ordered_ids:
            if self.database.players[id_num].is_deleted:
                continue
            ordered_players.append(self.database.players[id_num])

        return ordered_players

    def get_tournaments_by_id(self):
        """Lists all database tournaments sorted by id.

        Returns:
            list:  List of all tournaments ordered by id.
        """

        ordered_ids = sorted(self.database.tournaments, key=lambda x: x)

        ordered_tournaments = []
        for id_num in ordered_ids:
            ordered_tournaments.append(self.database.tournaments[id_num])

        return ordered_tournaments

    def get_tournament_object_from_id_str(self, tournament_id: str):
        """Searches through all of tournaments to find requested tournament.

        Args:
            tournament_id (str): Id of tournament to be searched.

        Returns:
            Tournament: Requested Tournament object.
        """

        for tournament in self.database.tournaments:
            if str(tournament) == tournament_id:
                return self.database.tournaments[tournament]

    def get_player_object_from_id_str(self, player_id: str):
        """Searches through all players to find requested player.

        Args:
            player_id (str): Id of player to be searched.

        Returns:
            Player: Requested Player object.
        """

        for player in self.database.players:
            if str(player) == player_id:
                return self.database.players[player]

    def get_player_name_from_id(self, player_id: int):
        """Searches through all players to find requested player's name.

        Args:
            player_id (int): Id of player to be searched.

        Returns:
            str: Player's first and last name.
        """

        for player in self.database.players:
            if self.database.players[player].id_num == player_id:
                name = f"{self.database.players[player].first_name} {self.database.players[player].last_name}"
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
            if self.database.players[id_num].is_deleted:
                continue
            players_list.append(self.database.players[player_id])

        return players_list

    def get_players_names(self, players_sample: list):
        """Return a list of players names from a list of Player objects.

        Args:
            players_sample (dict): Sample to search in.

        Returns:
            list: List of players name.
        """

        return [self.get_player_name_from_id(player_id=x) for x in players_sample]

    def get_formated_leaderboard(self, leaderboard: dict):
        """Formats a Leaderboard dict to a list of players names and scores, sorted by points.

        Args:
            leaderboard (dict): Leaderboard to be formated.

        Returns:
            list: List of players names and scores.
        """

        ordered_leaderboard = [(k, v) for k, v in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)]
        formated_leaderboard = []

        for player in ordered_leaderboard:
            formated_leaderboard.append((self.get_player_name_from_id(player_id=int(player[0])), player[1]))

        return formated_leaderboard