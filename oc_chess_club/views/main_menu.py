import typer

from oc_chess_club.views.tournament_views import TournamentMenu
from oc_chess_club.views.player_views import PlayerMenu
from oc_chess_club.views.report_views import ReportMenu
import oc_chess_club.views.helper as _HELPER


class MainMenu:
    """First view displayed, main menu."""

    def __init__(self):
        """Constructor for MainMenu."""

        _HELPER.print_title("menu principal")

        self.print_menu()
        self.user_selection()

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Tournois")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Gérer les joueurs")

        number = typer.style("3. ", bold=True)
        typer.echo(number + "Générer un rapport")

        number = typer.style("\n0. ", bold=True)
        typer.echo(number + "Quitter")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("\nEntrez votre sélection: ")
        typer.echo("\n")

        if selection == "0":
            typer.Exit()
        elif selection == "1":
            TournamentMenu()
        elif selection == "2":
            PlayerMenu()
        elif selection == "3":
            ReportMenu()
        else:
            self.user_selection()