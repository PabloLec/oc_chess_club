from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.player import Player


class TournamentGenerator:
    def __init__(self, players):
        self.players = players

    def sort_by_elo(self):
        return sorted(self.players, key=lambda x: x.elo)

    def generate_first_round(self):
        matches = []
        sorted_players = self.sort_by_elo()

        i = 0
        for i in range(0, 4):
            matches.append((sorted_players[i], sorted_players[i + 4]))

        return matches