import typer

from oc_chess_club.views.new_tournament import NewTournamentMenu
from oc_chess_club.views.load_tournament import LoadTournamentMenu


class TournamentMenu:
    """View for tournament related operations."""

    def __init__(self):
        """Constructor for TournamentMenu."""

        self.print_menu()
        self.user_selection()

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Commencer un nouveau tournoi")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Charger un tournoi")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("Entrez votre sélection: ")

        if selection == "1":
            self.create_new_tournament()
        elif selection == "2":
            self.load_tournament()
        else:
            self.user_selection()

    def create_new_tournament(self):
        """Opens the tournament creation menu."""

        NewTournamentMenu()

    def load_tournament(self):
        """Opens the tournament loading menu."""

        LoadTournamentMenu()