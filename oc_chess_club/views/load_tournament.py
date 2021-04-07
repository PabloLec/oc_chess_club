import typer

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER
from oc_chess_club.views.game import GameMenu


class LoadTournamentMenu:
    def __init__(self):
        self.available_tournaments = []

        self.display_unfinished_tournaments()
        self.user_selection()

    def display_unfinished_tournaments(self):

        unfinished_tournaments = _DATABASE_HANDLER.find_unfinished_tournaments()

        for tournament in unfinished_tournaments:
            self.available_tournaments.append(tournament["id"])

            typer.secho(f" - Tournoi n°{tournament['id']} -", fg=typer.colors.CYAN)
            parameter = typer.style("Nom: ", bold=True)
            typer.echo(parameter + tournament["Name"])
            parameter = typer.style("Date: ", bold=True)
            typer.echo(parameter + tournament["Date"] + "\n")

    def user_selection(self):
        selection = typer.prompt("Entrez un numéro de tournoi")

        while not selection.isnumeric() or int(selection) not in self.available_tournaments:
            typer.secho(f"Pas de tournoi avec le numéro {selection}", fg=typer.colors.RED)
            self.user_selection()
            return

        self.start_tournament(int(selection))

    def start_tournament(self, tournament_id):
        GameMenu(tournament_id)