from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match

from oc_chess_club.controller.tournament_generator import TournamentGenerator
from oc_chess_club.controller.database_handler import DatabaseHandler


class TournamentHandler:
    def __init__(self, resume_tournament: bool = False):
        self.tournament = None

        self.database_handler = DatabaseHandler()

        ## TO DO ##
        self.selected_players = self.database_handler.database.players[:8]
        ## ## ## ##

        self.generator = TournamentGenerator(players=self.selected_players)

        if not resume_tournament:
            self.start_tournament()

    def start_tournament(self):
        self.tournament = Tournament()
        self.create_round(round_number=1)

    def create_round(self, round_number: int):
        if round_number == 1:
            matches = self.generator.generate_first_round()
        else:
            pass

        current_round = Round(round_number=round_number)
        for match in matches:
            match_object = Match(players=match)
            current_round.add_match(match=match_object)

        self.tournament.add_round(round_object=current_round)

    def set_tournament_name(self, name: str):
        self.tournament.name = name

    def set_tournament_location(self, location: str):
        self.tournament.location = location

    def set_tournament_date(self, date: str):
        self.tournament.date = date

    def set_tournament_description(self, description: str):
        self.tournament.description = description

    def set_tournament_time_control(self, time_control: str):
        self.tournament.time_control = time_control

    def change_number_of_rounds(self, number_of_rounds: int):
        self.tournament.number_of_rounds = number_of_rounds