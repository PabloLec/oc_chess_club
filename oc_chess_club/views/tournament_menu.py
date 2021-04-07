import typer

from oc_chess_club.views.new_tournament import NewTournamentMenu
from oc_chess_club.views.load_tournament import LoadTournamentMenu


class TournamentMenu:
    def __init__(self):
        self.print_menu()
        self.user_selection()

    def print_menu(self):
        number = typer.style("1. ", bold=True)
        typer.echo(number + "Commencer un nouveau tournoi")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Charger un tournoi")

    def user_selection(self):
        selection = typer.prompt("Entrez votre sélection: ")

        if selection == "1":
            self.create_new_tournament()
        elif selection == "2":
            self.load_tournament()
        else:
            self.user_selection()

    def create_new_tournament(self):
        NewTournamentMenu()

    def load_tournament(self):
        LoadTournamentMenu()