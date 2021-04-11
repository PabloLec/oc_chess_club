import typer
from datetime import datetime

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER


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

        while not self.dob_is_valid():
            self.dob = typer.prompt("Date de naissance (JJ/MM/AAAA)")

        while not self.gender_is_valid():
            self.gender = typer.prompt("Genre (H/F)")

        while not self.elo.isnumeric():
            self.elo = typer.prompt("ELO")

    def dob_is_valid(self):
        """Verifies if the date entered by the user is valid using datetime library.

        Returns:
            bool: The date exists.
        """

        try:
            datetime.strptime(self.dob, "%d/%m/%Y")
            return True
        except ValueError:
            if len(self.dob) > 0:
                typer.secho("Date incorrecte", fg=typer.colors.RED)
            return False

    def gender_is_valid(self):
        """Verifies if the gender entered by the user is valid.

        Returns:
            bool: The gender is valid.
        """

        if len(self.gender) == 0:
            return False
        elif self.gender.lower() == "h":
            self.gender = "H"
            return True
        elif self.gender.lower() == "f":
            self.gender = "F"
            return True
        else:
            typer.secho("Genre incorrect. Entrez H ou F.", fg=typer.colors.RED)
            return False

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
            elo=self.elo,
        )

        typer.secho(f"Le joueur a été créé avec le numéro {created_player_id}.", fg=typer.colors.GREEN)