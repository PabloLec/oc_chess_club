from oc_chess_club.models.round import Round
from oc_chess_club.models.player import Player


class Tournament:
    def __init__(self):
        self.participating_players = []

        self.name = ""
        self.location = ""
        self.date = ""
        self.number_of_rounds = 4
        self.time_control = ""
        self.description = ""

        self.rounds = []

        self.is_finished = False

    def add_player(self, player: Player):

        self.participating_players.append(player)

    def is_tournament_full(self):

        if self.participating_players >= 8:
            return True
        else:
            return False

    def add_round(self, round_object: Round):
        self.rounds.append(round_object)