import typer
from datetime import datetime


class NewTournamentMenu:
    def __init__(self):
        self.tournament_name = ""
        self.location = ""
        self.date = ""
        self.number_of_rounds = ""
        self.time_control = ""
        self.description = ""

        self.settings_prompt()
        self.confirm_settings()

    def settings_prompt(self):
        typer.secho("Création d'un nouveau tournoi", fg=typer.colors.BLUE)
        typer.secho("Entrez les informations du tournoi\n")

        while len(self.tournament_name) == 0:
            self.tournament_name = typer.prompt("Nom du tournoi")

        while len(self.location) == 0:
            self.location = typer.prompt("Lieu")

        while not self.date_is_valid():
            self.date = typer.prompt("Date (JJ/MM/AAAA)")

        while not self.number_of_rounds.isnumeric():
            self.number_of_rounds = typer.prompt("Nombre de round")

        while not self.time_control_is_valid():
            self.time_control = typer.prompt("Contrôle du temps")

        while len(self.description) == 0:
            self.description = typer.prompt("Description")

    def date_is_valid(self):
        try:
            datetime.strptime(self.date, "%d/%m/%Y")
            return True
        except ValueError:
            if len(self.date) > 0:
                typer.secho("Date incorrecte", fg=typer.colors.RED)
            return False

    def time_control_is_valid(self):
        if self.time_control.lower() == "bullet":
            self.time_control = "Bullet"
            return True
        elif self.time_control.lower() == "blitz":
            self.time_control = "Blitz"
            return True
        elif self.time_control.lower() == "coup rapide":
            self.time_control = "Coup Rapide"
            return True
        else:
            if len(self.time_control) > 0:
                typer.secho("Entrée incorrect. Entrez Bullet, Blitz ou Coup Rapide.", fg=typer.colors.RED)
            return False

    def confirm_settings(self):
        typer.secho("\nParamètres du tournoi:", fg=typer.colors.BLUE)

        parameter = typer.style("Nom: ", bold=True)
        typer.echo(parameter + self.tournament_name)
        parameter = typer.style("Lieu: ", bold=True)
        typer.echo(parameter + self.location)
        parameter = typer.style("Date: ", bold=True)
        typer.echo(parameter + self.date)
        parameter = typer.style("Nombre de rounds: ", bold=True)
        typer.echo(parameter + self.number_of_rounds)
        parameter = typer.style("Contrôle du temps: ", bold=True)
        typer.echo(parameter + self.time_control)
        parameter = typer.style("Description: ", bold=True)
        typer.echo(parameter + self.description)

        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce tournoi ?")
        if not confirm:
            typer.secho("Annulation. Le tournoi n'est pas créé.", fg=typer.colors.RED)
            raise typer.Exit