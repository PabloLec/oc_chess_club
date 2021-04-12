import typer

from oc_chess_club.views.tournament_views import TournamentMenu
from oc_chess_club.views.player_views import PlayerMenu


class MainMenu:
    """First view displayed, main menu."""

    def __init__(self):
        """Constructor for MainMenu."""

        typer.echo("\n")
        typer.secho("MENU PRINCIPAL", fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_CYAN, bold=True, underline=True)

        self.print_menu()
        self.user_selection()

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Tournois")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Gérer les joueurs")

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
        else:
            self.user_selection()