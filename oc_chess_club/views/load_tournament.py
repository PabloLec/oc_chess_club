import typer

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER
from oc_chess_club.views.game import GameMenu


class LoadTournamentMenu:
    """View displayed for tournament loading.

    Attributes:
        available_tournaments (list): Unfinished tournaments available for loading.
    """

    def __init__(self):
        """Constructor for LoadTournamentMenu."""

        self.available_tournaments = []

        self.display_unfinished_tournaments()
        self.user_selection()

    def display_unfinished_tournaments(self):
        """Uses database handler to find and display unfinished tournament for the user to choose from."""

        unfinished_tournaments = _DATABASE_HANDLER.helper.get_unfinished_tournaments()

        for tournament in unfinished_tournaments:
            self.available_tournaments.append(tournament.id_num)

            typer.secho(f" - Tournoi n°{tournament.id_num} -", fg=typer.colors.CYAN)
            parameter = typer.style("Nom: ", bold=True)
            typer.echo(parameter + tournament.name)
            parameter = typer.style("Date: ", bold=True)
            typer.echo(parameter + tournament.date + "\n")

    def user_selection(self):
        """Prompts the user to select a tournament to be loaded."""

        selection = typer.prompt("Entrez un numéro de tournoi")

        while not selection.isnumeric() or int(selection) not in self.available_tournaments:
            typer.secho(f"Pas de tournoi avec le numéro {selection}", fg=typer.colors.RED)
            self.user_selection()
            return

        self.start_tournament(int(selection))

    def start_tournament(self, tournament_id):
        """Opens the Game Menu for selected tournament.

        Args:
            tournament_id (int): Unique id of the tournament to be loaded.
        """

        GameMenu(tournament_id)