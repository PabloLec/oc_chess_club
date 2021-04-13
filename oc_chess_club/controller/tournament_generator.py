from oc_chess_club.models.player import Player
from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.match import Match
from oc_chess_club.controller.database_handler import DatabaseHandler


class TournamentGenerator:
    """Generates rounds and their matches.

    Attributes:
        player (dict[Player]): Dict of participating players."""

    def __init__(self, players: dict[Player]):
        """Constructor for TournamentGenerator.

        Args:
            players (dict[Player]): Dict of participating players.
        """

        self.players = players

    def sort_by_elo(self):
        """Sorts players by their ELO ranking.

        Returns:
            list[Player]: List of players ordered by ELO (ascending).
        """

        return sorted(self.players, key=lambda x: x.elo)

    def sort_by_points(self, leaderboard: dict):
        """Sort players from a leaderboard by points.

        Args:
            leaderboard (dict): Dict of players to be sorted.

        Returns:
            list[Player]: List of players ordered by points (descending).
        """

        return sorted(leaderboard, key=leaderboard.get, reverse=True)

    def player_object_from_id(self, player_id: str):
        """Searches through participating players for given unique id.

        Args:
            player_id (str): Player's unique id to be searched.

        Returns:
            Player: Corresponding Player object.
        """

        for player in self.players:
            if player.id_num == int(player_id):
                return player

    def players_have_already_met(self, matches: list[tuple[Player]], id_1: str, id_2: str):
        """Searches through a list of matches for an already existing match between the two given players.

        Args:
            matches (list[tuple[Player]]): List of players pairing, corresponding to past matches.
            id_1 (str): First player unique id.
            id_2 (str): Second player unique id.

        Returns:
            bool: Players have already met.
        """

        player_1_vs_player_2 = (int(id_1), int(id_2))
        player_2_vs_player_1 = (int(id_2), int(id_1))

        if player_1_vs_player_2 in matches:
            return True
        elif player_2_vs_player_1 in matches:
            return True
        else:
            return False

    def generate_first_round(self):
        """Generates the first round following Swiss-system.

        Returns:
            list[Match]: List of generated matches.
        """

        matches = []
        sorted_players = self.sort_by_elo()

        for i in range(0, int(len(self.players) / 2)):
            matches.append((sorted_players[i], sorted_players[i + int(len(self.players) / 2)]))

        return matches

    def generate_other_round(self, matches: list[Match], leaderboard: dict):
        """Generates one round, other than the first one, following Swiss-system.

        Args:
            matches (list[Match]): List of past matches.
            leaderboard (dict): Current leaderboard.

        Returns:
            list[Match]: List of generated matches.
        """

        matches = []
        sorted_players = self.sort_by_points(leaderboard=leaderboard)

        while len(sorted_players) != 0:
            for opponent in range(1, len(sorted_players)):
                id_1 = sorted_players[0]
                id_2 = sorted_players[opponent]

                player_1 = DatabaseHandler().helper.get_player_object_from_id_str(player_id=id_1)
                player_2 = DatabaseHandler().helper.get_player_object_from_id_str(player_id=id_2)

                if not self.players_have_already_met(matches=matches, id_1=id_1, id_2=id_2):
                    matches.append((player_1, player_2))
                    del sorted_players[0]
                    del sorted_players[opponent - 1]
                    break

        return matches
