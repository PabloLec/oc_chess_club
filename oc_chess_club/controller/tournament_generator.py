from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.player import Player


class TournamentGenerator:
    def __init__(self, players):
        self.players = players

    def sort_by_elo(self):
        return sorted(self.players, key=lambda x: x.elo)

    def sort_by_points(self, leaderboard: dict):
        return sorted(leaderboard, key=leaderboard.get, reverse=True)

    def player_object_from_id(self, player_id: str):
        for player in self.players:
            if player.id_num == int(player_id):
                return player

    def players_have_already_met(self, matches: list, id_1: str, id_2: str):
        player_1_vs_player_2 = (int(id_1), int(id_2))
        player_2_vs_player_1 = (int(id_2), int(id_1))

        if player_1_vs_player_2 in matches:
            return True
        elif player_2_vs_player_1 in matches:
            return True
        else:
            return False

    def generate_first_round(self):
        matches = []
        sorted_players = self.sort_by_elo()

        for i in range(0, int(len(self.players) / 2)):
            matches.append((sorted_players[i], sorted_players[i + int(len(self.players) / 2)]))

        return matches

    def generate_other_round(self, matches: list, leaderboard: dict):
        matches = []
        sorted_players = self.sort_by_points(leaderboard=leaderboard)

        while len(sorted_players) != 0:
            for opponent in range(1, len(sorted_players)):
                id_1 = sorted_players[0]
                id_2 = sorted_players[opponent]

                if not self.players_have_already_met(matches=matches, id_1=id_1, id_2=id_2):
                    matches.append(
                        (self.player_object_from_id(player_id=id_1), self.player_object_from_id(player_id=id_2))
                    )
                    del sorted_players[0]
                    del sorted_players[opponent - 1]
                    break

        return matches
