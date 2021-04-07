import typer

from oc_chess_club.controller.tournament_handler import TournamentHandler


class GameMenu:
    def __init__(self, tournament_id):
        self.tournament_handler = TournamentHandler(tournament_id=tournament_id)
        self.display_next_round()

    def display_next_round(self):
        self.tournament_handler.create_round()
        current_round = self.tournament_handler.tournament.rounds[-1]