from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match

from oc_chess_club.controller.tournament_generator import TournamentGenerator
from oc_chess_club.controller.database_handler import _DATABASE_HANDLER


class TournamentHandler:
    def __init__(self, tournament_id):
        self.tournament = _DATABASE_HANDLER.database.tournaments[tournament_id]
        self.current_round = len(self.tournament.rounds) + 1

        self.generator = TournamentGenerator(players=self.tournament.players)

    def create_round(self):
        if len(self.tournament.rounds) == 0:
            matches = self.generator.generate_first_round()
        else:
            pass

        round_id = _DATABASE_HANDLER.create_round(
            round_number=len(self.tournament.rounds) + 1, tournament_id=self.tournament.id_num
        )
        created_round = _DATABASE_HANDLER.database.rounds[round_id]

        for players in matches:
            match_id = _DATABASE_HANDLER.create_match(players=players, round_id=round_id)
            created_round.add_match(match=_DATABASE_HANDLER.database.matches[match_id])

        self.tournament.rounds.append(created_round)

    def is_tournament_full(self):

        if len(self.tournament.players) == 8:
            return True
        else:
            return False