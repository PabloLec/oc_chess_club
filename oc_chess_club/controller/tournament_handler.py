from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match
from oc_chess_club.models.player import Player

from oc_chess_club.controller.tournament_generator import TournamentGenerator
from oc_chess_club.controller.database_handler import _DATABASE_HANDLER


class TournamentHandler:
    def __init__(self, tournament_id):
        self.tournament = _DATABASE_HANDLER.database.tournaments[tournament_id]
        self.current_round_num = 0
        self.current_round_id = 0
        self.current_match_num = 0

        self.generator = TournamentGenerator(players=self.tournament.players)
        self.resume_tournament()

    def resume_tournament(self):
        if len(self.tournament.rounds) == 0:
            self.create_round()

        self.find_next_round()
        self.find_next_match()
        self.update_tournament_progression()

    def match_generator(self):
        while not self.is_tournament_finished():
            next_match = self.find_next_match()
            if next_match is not None:
                return next_match
            else:
                self.create_round()

    def find_next_round(self):
        # Search if a round is not yet finished to resume it
        for round_id in self.tournament.rounds:
            round_object = self.tournament.rounds[round_id]
            if not self.is_round_finished(round_=round_object):
                self.current_round_id = round_object.id_num
                self.current_round_num = round_object.round_number
                return round_object

        return self.tournament.rounds[self.current_round_id]

    def create_round(self):
        if len(self.tournament.rounds) == 0:
            matches = self.generator.generate_first_round()
        else:
            pass

        round_id = _DATABASE_HANDLER.create_round(
            round_number=len(self.tournament.rounds) + 1, tournament_id=self.tournament.id_num
        )

        _DATABASE_HANDLER.database.tournaments[self.tournament.id_num].rounds[round_id]
        self.current_round_id = round_id
        print(" ->", self.current_round_id, round_id)

        for players in matches:
            _DATABASE_HANDLER.create_match(players=players, tournament_id=self.tournament.id_num, round_id=round_id)

    def find_next_match(self):
        matches = self.tournament.rounds[self.current_round_id].matches
        for match_id in matches:
            match_object = self.tournament.rounds[self.current_round_id].matches[match_id]
            if match_object.winner is None:
                return match_object
        return None

    def update_tournament_progression(self):
        self.current_round_num = self.tournament.rounds[self.current_round_id].round_number

        self.current_match_num = 1
        current_round = self.tournament.rounds[self.current_round_id]
        for match in current_round.matches:
            if current_round.matches[match].winner is not None:
                self.current_match_num += 1

    def is_tournament_full(self):

        if len(self.tournament.players) == 8:
            return True
        else:
            return False

    def is_round_finished(self, round_: Round):
        matches = round_.matches

        for match_id in matches:
            match_object = self.tournament.rounds[round_.id_num].matches[match_id]
            if match_object.winner is None:
                return False

        return True

    def is_tournament_finished(self):
        if len(self.tournament.rounds) < self.tournament.number_of_rounds:
            return False

        for round_id in self.tournament.rounds:
            round_object = self.tournament.rounds[round_id]
            if not self.is_round_finished(round_=round_object):
                return False

        return True

    def save_winner(self, match: Match, winner: str):
        if winner == "1":
            winner = 1
        elif winner == "2":
            winner = 2
        elif winner == "nul":
            winner = 0

        self.tournament.rounds[self.current_round_id].matches[match.id_num].winner = winner
        _DATABASE_HANDLER.save_match(match=match)