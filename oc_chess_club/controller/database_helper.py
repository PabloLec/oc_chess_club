from oc_chess_club.models.player import Player
from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match


class DatabaseHelper:
    """Helper class encapsulating methods to manipulate and transform database objects."""

    def __init__(self):
        pass

    def list_all_matches(self, tournament: Tournament):
        """Lists all matches of a tournament.

        Args:
            tournament (Tournament): Tounament objects.

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

    def sort_players_by_id(self, players: dict):
        """Takes a dict of players, typically from a round attribute, and sort them by id.

        Args:
            players (dict): Players to be sorted.

        Returns:
            list:  List og players ordered by id.
        """

        ordered_ids = sorted(players, key=lambda x: x)

        ordered_players = []
        for id_num in ordered_ids:
            ordered_players.append(players[id_num])

        return ordered_players

    def player_object_from_id_str(self, players: list[Player], player_id: str):
        """Searches through a list of players to find requested player.

        Args:
            players (list[Player]): List of players to search in.
            player_id (str): Id of player to be searched.

        Returns:
            Player: Requested Player object.
        """

        for player in players:
            if player.id_num == int(player_id):
                return player

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