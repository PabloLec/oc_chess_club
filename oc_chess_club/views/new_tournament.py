import typer
from datetime import datetime

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER
from oc_chess_club.views.game import GameMenu


class NewTournamentMenu:
    def __init__(self):

        self.tournament_name = ""
        self.location = ""
        self.date = ""
        self.number_of_rounds = ""
        self.time_control = ""
        self.description = ""
        self.players = []
        self.created_tournament_id = None

        self.settings_prompt()
        self.add_players()
        self.confirm_settings()
        self.save_tournament()
        self.start_tournament()

    def settings_prompt(self):
        typer.secho("Création d'un nouveau tournoi", fg=typer.colors.BLUE)
        typer.echo("Entrez les informations du tournoi\n")

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

    def add_players(self):

        typer.secho("\nEntrez le numéro d'un joueur à ajouter\n", fg=typer.colors.BLUE)

        available_players = _DATABASE_HANDLER.helper.sort_players_by_id(players=_DATABASE_HANDLER.database.players)
        for player in available_players:
            player_id = typer.style(str(player.id_num), bold=True)
            typer.echo(f"{player_id}. {player.first_name} {player.last_name}")

        while len(self.players) < 8:
            selection = typer.prompt(f"Joueur ({str(len(self.players))}/8)")
            if self.player_exists(available_players=available_players, selected_id=selection):
                self.players.append(int(selection))

    def player_exists(self, available_players: list, selected_id: str):
        if not selected_id.isnumeric():
            typer.secho("Entrez le numéro du joueur apparaissant devant son nom", fg=typer.colors.RED)
            return False

        if int(selected_id) in self.players:
            typer.secho(f"Le joueur numéro {selected_id} a déjà été ajouté", fg=typer.colors.RED)
            return False

        for player in available_players:
            if int(selected_id) == player.id_num:
                return True

        typer.secho(f"Pas de joueur avec le numéro {selected_id}", fg=typer.colors.RED)

        return False

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
        self.list_settings()
        self.list_participating_players()

        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce tournoi ?")
        if not confirm:
            typer.secho("Annulation. Le tournoi n'a pas été créé.", fg=typer.colors.RED)
            raise typer.Exit

    def list_settings(self):
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

    def list_participating_players(self):
        typer.secho("\n Liste des joueurs: ", bold=True)
        for player in self.players:
            name = _DATABASE_HANDLER.helper.player_name_from_id(
                players=_DATABASE_HANDLER.database.players, player_id=player
            )
            typer.echo(f" - {name}")

    def save_tournament(self):

        self.created_tournament_id = _DATABASE_HANDLER.create_tournament(
            name=self.tournament_name,
            location=self.location,
            date=self.date,
            number_of_rounds=int(self.number_of_rounds),
            time_control=self.time_control,
            description=self.description,
            players=self.players,
            leaderboard={},
        )

        typer.secho("Le tournoi a été créé.", fg=typer.colors.GREEN)

    def start_tournament(self):
        confirm = typer.confirm("\nSouhaitez vous commencer le tournoi ?")

        if confirm:
            GameMenu(tournament_id=self.created_tournament_id)