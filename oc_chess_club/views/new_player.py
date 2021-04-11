import typer
from datetime import datetime

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER
import oc_chess_club.views.helper as _HELPER


class NewPlayerMenu:
    """View for new player creation.

    Attributes:
        first_name (str): Players's first name.
        last_name (str): Player's last name.
        dob (str): Player's date of birth.
        gender (str): Player's gender.
        elo (str): Player's ELO ranking.
    """

    def __init__(self):
        """Constructor for NewPlayerMenu."""

        self.first_name = ""
        self.last_name = ""
        self.dob = ""
        self.gender = ""
        self.elo = ""

        self.settings_prompt()
        self.confirm_settings()
        self.save_player()

    def settings_prompt(self):
        """Prompts the user to input the different player settings."""

        typer.secho("Création d'un nouveau joueur", fg=typer.colors.BLUE)
        typer.echo("Entrez les informations du joueur\n")

        while len(self.first_name) == 0:
            self.first_name = typer.prompt("Prénom du joueur")

        while len(self.last_name) == 0:
            self.last_name = typer.prompt("Nom de famille du joueur")

        while not _HELPER.date_is_valid(date=self.dob):
            self.dob = typer.prompt("Date de naissance (JJ/MM/AAAA)")

        while not _HELPER.gender_is_valid(gender=self.gender):
            self.gender = typer.prompt("Genre (H/F)")

        while not self.elo.isnumeric():
            self.elo = typer.prompt("ELO")

    def confirm_settings(self):
        """Prompts the user to confirm the settings previously entered.

        Raises:
            typer.Exit: Exits if the user cancels the creation.
        """

        self.list_settings()

        confirm = typer.confirm("\nSouhaitez vous confirmer la création de ce joueur ?")
        if not confirm:
            typer.secho("Annulation. Le joueur n'a pas été créé.", fg=typer.colors.RED)
            raise typer.Exit

    def list_settings(self):
        """Displays all previously entered player settings."""

        typer.secho("\nInformations du joueur:", fg=typer.colors.BLUE)

        parameter = typer.style("Prénom: ", bold=True)
        typer.echo(parameter + self.first_name)
        parameter = typer.style("Nom de famille: ", bold=True)
        typer.echo(parameter + self.last_name)
        parameter = typer.style("Date de naissance: ", bold=True)
        typer.echo(parameter + self.dob)
        parameter = typer.style("Genre: ", bold=True)
        typer.echo(parameter + self.gender)
        parameter = typer.style("ELO: ", bold=True)
        typer.echo(parameter + str(self.elo))

    def save_player(self):
        """Uses database handler to save created player."""

        created_player_id = _DATABASE_HANDLER.create_player(
            first_name=self.first_name,
            last_name=self.last_name,
            dob=self.dob,
            gender=self.gender,
            elo=int(self.elo),
        )

        typer.secho(f"Le joueur a été créé avec le numéro {created_player_id}.", fg=typer.colors.GREEN)