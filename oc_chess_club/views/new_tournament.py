import typer
from datetime import datetime

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER
from oc_chess_club.views.game import GameMenu


class NewTournamentMenu:
    """View for new tournament creation.

    Attributes:
        tournament_name (str): Name of the tournament.
        location (str): Location of the tournament.
        date (str): Date of the tournament.
        number_of_rounds (str): Number of rounds to be played.
        time_control (str): Type of time control.
        description (str): Description of the tournament.
        created_tournament_id (int): Unique id of the created tournament.
    """

    def __init__(self):
        """Constructor for NewTournamentMenu."""

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
        """Prompts the user to input the different tournament settings."""

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
        """Prompts the user to select the participating players."""

        typer.secho("\nEntrez le numéro d'un joueur à ajouter\n", fg=typer.colors.BLUE)

        available_players = _DATABASE_HANDLER.helper.get_players_by_id()

        for player in available_players:
            player_id = typer.style(str(player.id_num), bold=True)
            typer.echo(f"{player_id}. {player.first_name} {player.last_name}")

        while len(self.players) < 8:
            selection = typer.prompt(f"Joueur ({str(len(self.players))}/8)")

            if self.player_exists(selected_id=selection):
                self.players.append(int(selection))

    def player_exists(self, selected_id: str):
        """Verifies if the player selected by the user is available/exists.

        Args:
            selected_id (str): Player chosen by the user.

        Returns:
            bool: The user is selectable.
        """

        if not selected_id.isnumeric():
            typer.secho("Entrez le numéro du joueur apparaissant devant son nom", fg=typer.colors.RED)
            return False

        if int(selected_id) in self.players:
            typer.secho(f"Le joueur numéro {selected_id} a déjà été ajouté", fg=typer.colors.RED)
            return False

        if _DATABASE_HANDLER.helper.is_player_id_in_database(player_id=int(selected_id)):
            return True

        typer.secho(f"Pas de joueur avec le numéro {selected_id}", fg=typer.colors.RED)

        return False

    def date_is_valid(self):
        """Verifies if the date entered by the user is valid using datetime library.

        Returns:
            bool: The date exists.
        """

        try:
            datetime.strptime(self.date, "%d/%m/%Y")
            return True
        except ValueError:
            if len(self.date) > 0:
                typer.secho("Date incorrecte", fg=typer.colors.RED)
            return False

    def time_control_is_valid(self):
        """Verifies if the type of time control entered by the user is valid.

        Returns:
            bool: Time control is valid.
        """

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
        """Prompts the user to confirm the settings previously entered.

        Raises:
            typer.Exit: Exits if the user cancels the creation.
        """

        self.list_settings()
        self.list_participating_players()

        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce tournoi ?")
        if not confirm:
            typer.secho("Annulation. Le tournoi n'a pas été créé.", fg=typer.colors.RED)
            raise typer.Exit

    def list_settings(self):
        """Displays all previously entered tournament settings."""

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
        """Displays selected participating players by their name."""

        typer.secho("\n Liste des joueurs: ", bold=True)
        for player in self.players:
            name = _DATABASE_HANDLER.helper.player_name_from_id(
                players=_DATABASE_HANDLER.database.players, player_id=player
            )
            typer.echo(f" - {name}")

    def save_tournament(self):
        """Uses database handler to save created tournament."""

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
        """Starts created tournament if the user select so."""

        confirm = typer.confirm("\nSouhaitez vous commencer le tournoi ?")

        if confirm:
            GameMenu(tournament_id=self.created_tournament_id)