from oc_chess_club.models.tournament import Tournament
from oc_chess_club.models.round import Round
from oc_chess_club.models.match import Match
from oc_chess_club.models.player import Player

from oc_chess_club.controller.tournament_generator import TournamentGenerator
from oc_chess_club.controller.database_handler import DatabaseHandler


class TournamentHandler:
    """Handles a tournament's generation and progression.

    Attributes:
        tournament (Tournament): Corresponding tournament object.
        generator (TournamentGenerator): Object to generate matchmaking.
        current_round_num (int): Number of the round currently played.
        current_round_id (int): Unique id of the round currently played.
        current_match_num (int): Number of the match currently played.
        current_match_id (int): Unique id of the match currently played.
    """

    def __init__(self, tournament_id: int):
        """Constructor for TournamentHandler.

        Args:
            tournament_id (int): Unique id of the tournament to be resumed.
        """

        self.tournament = DatabaseHandler().database.tournaments[tournament_id]
        self.generator = TournamentGenerator(players=self.tournament.players)

        self.current_round_num = 0
        self.current_round_id = 0
        self.current_match_num = 0
        self.current_match_id = 0

        self.resume_tournament()

    def load_rounds_and_matches(self):
        """Uses database handler to load tournament's rounds and matches objects into memory."""

        DatabaseHandler().load_rounds(tournament_id=self.tournament.id_num)
        DatabaseHandler().load_matches(tournament_id=self.tournament.id_num)

    def resume_tournament(self):
        """Creates the first round if needed and requests a first progression update."""

        self.load_rounds_and_matches()

        if len(self.tournament.rounds) == 0:
            self.create_round()

        self.update_tournament_progression()

    def match_generator(self):
        """Returns a new match until tournament completion.

        Returns:
            Match: Next match to be played.
        """

        self.update_tournament_progression()

        current_round = self.tournament.rounds[self.current_round_id]

        if self.is_round_finished(round_=current_round):
            if self.is_tournament_finished():
                return None

            self.create_round()
            self.update_tournament_progression()
            current_round = self.tournament.rounds[self.current_round_id]

        return current_round.matches[self.current_match_id]

    def create_round(self):
        """Creates a new round and its matches based on current tournament progression."""

        if len(self.tournament.rounds) == 0:
            matches = self.generator.generate_first_round()
        else:
            all_matches_list = DatabaseHandler().helper.get_all_matches(tournament=self.tournament)
            matches = self.generator.generate_other_round(
                matches=all_matches_list, leaderboard=self.tournament.leaderboard
            )

        round_id = DatabaseHandler().create_round(
            round_number=len(self.tournament.rounds) + 1, tournament_id=self.tournament.id_num
        )

        self.current_round_id = round_id

        for players in matches:
            DatabaseHandler().create_match(
                players=players, tournament_id=self.tournament.id_num, round_id=round_id, winner=None
            )

    def update_tournament_progression(self):
        """Requests an update on tournament's rounds and matches progession."""

        self.update_current_round()
        self.update_current_match()

    def update_current_round(self):
        """Updates current round number and unique id based on tournament's rounds completion."""

        for round_id in self.tournament.rounds:
            round_object = self.tournament.rounds[round_id]
            if not self.is_round_finished(round_=round_object):
                self.current_round_id = round_object.id_num
                self.current_round_num = round_object.round_number
            else:
                if round_object.round_number > self.current_round_num:
                    self.current_round_num = round_object.round_number
                    self.current_round_id = round_object.id_num

    def update_current_match(self):
        """Updates current match number and unique id based on round's matches completion."""

        self.current_match_num = 0
        current_round = self.tournament.rounds[self.current_round_id]

        # Search if a match is not yet finished
        for match in current_round.matches:
            self.current_match_num += 1
            if current_round.matches[match].winner is None:
                self.current_match_id = current_round.matches[match].id_num
                return

        # If all round's matches are finished, arbitrarily take the first match
        # as none of them will be played.
        first_match_id = list(current_round.matches.keys())[0]
        self.current_match_id = first_match_id

    def is_round_finished(self, round_: Round):
        """Verifies if a round is finished by iterating through its matches' winners.

        Args:
            round_ (Round): Round object to be verified.

        Returns:
            bool: Match is finished.
        """

        matches = round_.matches

        for match_id in matches:
            match_object = self.tournament.rounds[round_.id_num].matches[match_id]
            if match_object.winner is None:
                return False

        return True

    def is_tournament_finished(self):
        """Verifies if a tournament is finished by iterating through its rounds.

        Returns:
            bool: Tournament is finished.
        """

        if len(self.tournament.rounds) < self.tournament.number_of_rounds:
            return False

        for round_id in self.tournament.rounds:
            round_object = self.tournament.rounds[round_id]
            if not self.is_round_finished(round_=round_object):
                return False

        DatabaseHandler().database.tournaments[self.tournament.id_num].is_finished = True
        DatabaseHandler().save_tournament(tournament=DatabaseHandler().database.tournaments[self.tournament.id_num])
        return True

    def save_winner(self, match: Match, winner: str):
        """Takes the winner input by the user and saves it to the database.

        Args:
            match (Match): Match to be considered.
            winner (str): Input of the user.
        """

        if winner == "1":
            winner = 1
            DatabaseHandler().update_leaderboard(
                tournament_id=match.tournament_id, player_id=match.player_1.id_num, points_earned=1
            )
        elif winner == "2":
            winner = 2
            DatabaseHandler().update_leaderboard(
                tournament_id=match.tournament_id, player_id=match.player_2.id_num, points_earned=1
            )
        elif winner == "nul":
            winner = 0
            DatabaseHandler().update_leaderboard(
                tournament_id=match.tournament_id, player_id=match.player_1.id_num, points_earned=0.5
            )
            DatabaseHandler().update_leaderboard(
                tournament_id=match.tournament_id, player_id=match.player_2.id_num, points_earned=0.5
            )

        self.tournament.rounds[self.current_round_id].matches[match.id_num].winner = winner
        DatabaseHandler().save_match(self.tournament.rounds[self.current_round_id].matches[match.id_num])
