from oc_chess_club.models.player import Player
from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match


class DatabaseHelper:
    def __init__(self):
        pass

    def list_all_matches(self, tournament: Tournament):
        match_list = []

        for round_id in tournament.rounds:
            for match_id in tournament.rounds[round_id].matches:
                player_1 = tournament.rounds[round_id].matches[match_id].player_1
                player_2 = tournament.rounds[round_id].matches[match_id].player_2
                match_list.append((player_1.id_num, player_2.id_num))

        return match_list

    def sort_players_by_id(self, players: dict):
        ordered_ids = sorted(players, key=lambda x: x)

        ordered_players = []
        for id_num in ordered_ids:
            ordered_players.append(players[id_num])

        return ordered_players

    def player_object_from_id_str(self, players: list, player_id: str):
        for player in players:
            if player.id_num == int(player_id):
                return player

    def player_name_from_id(self, players: dict, player_id: int):
        for player in players:
            if players[player].id_num == player_id:
                name = f"{players[player].first_name} {players[player].last_name}"
                return name