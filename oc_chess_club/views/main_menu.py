import typer

from oc_chess_club.views.tournament_menu import TournamentMenu


class MainMenu:
    """First view displayed, main menu."""

    def __init__(self):
        """Constructor for MainMenu."""

        self.print_menu()
        self.user_selection()

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Tournois")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Gérer les joueurs")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("Entrez votre sélection: ")
        typer.echo("\n")

        if selection == "1":
            self.open_tournament_menu()
        else:
            self.user_selection()

    def open_tournament_menu(self):
        """Opens the tournament menu."""

        TournamentMenu()