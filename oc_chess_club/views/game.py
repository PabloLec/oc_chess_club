import typer

import oc_chess_club.views.helper as _HELPER

from oc_chess_club.controller.tournament_handler import TournamentHandler
from oc_chess_club.models.match import Match
from oc_chess_club.controller.database_handler import DatabaseHandler


class GameMenu:
    """View displayed during a game.

    Attributes:
        tournament_handler (TournamentHandler): Object handling tournament genration, progression and saving.
    """

    def __init__(self, tournament_id: int):
        """Constructor for GameMenu. Initiates the match generation.

        Args:
            tournament_id (int): Unique id of the tournament to be played.
        """

        self.tournament_handler = TournamentHandler(tournament_id=tournament_id)
        self.play()

        _HELPER.go_back(current_view=self.__class__.__name__)

    def play(self):
        """Uses the match generating method of the tournament handler to display a match until tournament's ending."""

        while self.tournament_handler.match_generator() is not None:
            self.display_next_match(self.tournament_handler.match_generator())

        self.ending_splash()

    def display_next_match(self, match: Match):
        """Initiates relevant info displays and prompts for a given Match.

        Args:
            match (Match): Match object to be displayed.
        """

        self.display_tournament_progression()
        self.introduce_match(match=match)
        winner = self.ask_for_winner()
        self.tournament_handler.save_winner(match=match, winner=winner)

    def display_tournament_progression(self):
        """Displays current tournament, round and match numbers."""

        self.tournament_handler.update_tournament_progression()
        decorator = typer.style(
            " - - ",
            bold=True,
        )
        separator = typer.style(
            " - ",
            bold=True,
        )

        tournament_num = typer.style(
            f"Tournoi {self.tournament_handler.tournament.id_num}",
            fg=typer.colors.BLUE,
        )
        round_num = typer.style(
            f"Round {self.tournament_handler.current_round_num}",
            fg=typer.colors.BLUE,
        )
        match_num = typer.style(
            f"Match {self.tournament_handler.current_match_num}",
            fg=typer.colors.BLUE,
        )

        typer.echo("\n" + decorator + tournament_num + separator + round_num + separator + match_num + decorator)

    def introduce_match(self, match: Match):
        """Displays current match's players names and ELO ranking.

        Args:
            match (Match): Match to be played.
        """

        player_1_title = typer.style(
            "Joueur 1: ",
            bold=True,
        )
        player_1_name = typer.style(
            "{f_name_1} {l_name_1} ".format(
                f_name_1=match.player_1.first_name,
                l_name_1=match.player_1.last_name,
            ),
            fg=typer.colors.GREEN,
        )
        player_1_elo = typer.style(
            f"({match.player_1.elo})",
            fg=typer.colors.BLUE,
        )

        player_1_full_presentation = player_1_title + player_1_name + player_1_elo

        versus = typer.style(
            " vs ",
            bold=True,
        )
        player_2_title = typer.style(
            "Joueur 2: ",
            bold=True,
        )
        player_2_name = typer.style(
            "{f_name_2} {l_name_2} ".format(
                f_name_2=match.player_2.first_name,
                l_name_2=match.player_2.last_name,
            ),
            fg=typer.colors.GREEN,
        )
        player_2_elo = typer.style(
            f"({match.player_2.elo})",
            fg=typer.colors.BLUE,
        )

        player_2_full_presentation = player_2_title + player_2_name + player_2_elo

        typer.echo(player_1_full_presentation + versus + player_2_full_presentation)

    def ask_for_winner(self):
        """Prompts the user to enter a winner.

        Returns:
            str: Winner of the match. ("1" for Player 1, "2" for Player 2, "nul" for a draw.)
        """

        winner = ""
        while winner.lower() not in ["1", "2", "nul"]:
            winner = typer.prompt("Entrez le gagnant (1, 2, ou nul)")

        return winner.lower()

    def ending_splash(self):
        """Displays final leaderboard."""

        typer.echo("\n")
        _HELPER.print_success("TOURNOI TERMINÉ")
        _HELPER.print_info("classement final:")

        leaderboard = DatabaseHandler().helper.get_formated_leaderboard(
            leaderboard=self.tournament_handler.tournament.leaderboard
        )

        i = 1
        for player in leaderboard:
            rank = typer.style(f"{i} -", bold=True)
            player_name = player[0]
            points = str(player[1])

            typer.echo(f"{rank} {player_name} ({points} points)")

            i += 1

        typer.echo("\n")
