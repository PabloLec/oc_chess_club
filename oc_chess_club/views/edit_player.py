import typer

from typing import Any
from datetime import datetime

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER
import oc_chess_club.views.helper as _HELPER


class EditPlayerMenu:
    """View for player editing.

    Attributes:
        selected_player (Player): Player selected by user for edit.
        modification_made (bool): Flag indicating whether a modification was made.
    """

    def __init__(self):
        """Constructor for EditPlayerMenu."""

        self.selected_player = _HELPER.select_player()
        self.modification_made = False

        self.select_edit()

        if self.modification_made:
            self.confirm_settings()
            self.save_player()
        else:
            typer.secho("\nAucune modification effectuée.\n", fg=typer.colors.GREEN)

    def select_edit(self):
        """Enumerates all player's informations and asks for edit."""

        typer.secho("\nInformations actuelles du joueur:\n", fg=typer.colors.BLUE)

        self.select_first_name()
        self.select_last_name()
        self.select_dob()
        self.select_gender()
        self.select_elo()

    def select_first_name(self):
        """Handles player's first name edit."""

        self.display_current_value(field_title="Prénom", value=self.selected_player.first_name)

        if self.ask_for_edit():
            self.selected_player.first_name = ""
            while len(self.selected_player.first_name) == 0:
                self.selected_player.first_name = self.enter_new_value(field_title="Prénom")

    def select_last_name(self):
        """Handles player's last name edit."""

        self.display_current_value(field_title="Nom de famille", value=self.selected_player.last_name)

        if self.ask_for_edit():
            self.selected_player.last_name = ""
            while len(self.selected_player.last_name) == 0:
                self.selected_player.last_name = self.enter_new_value(field_title="Nom de famille")

    def select_dob(self):
        """Handles player's date of birth edit."""

        self.display_current_value(field_title="Date de naissance", value=self.selected_player.dob)

        if self.ask_for_edit():
            self.selected_player.dob = ""
            while not self.dob_is_valid():
                self.selected_player.dob = self.enter_new_value(field_title="Date de naissance")

    def select_gender(self):
        """Handles player's gender edit."""

        self.display_current_value(field_title="Genre", value=self.selected_player.gender)

        if self.ask_for_edit():
            self.selected_player.gender = ""
            while not self.gender_is_valid():
                self.selected_player.gender = self.enter_new_value(field_title="Genre")

    def select_elo(self):
        """Handles player's ELo ranking edit."""

        self.display_current_value(field_title="ELO", value=str(self.selected_player.elo))

        if self.ask_for_edit():
            self.selected_player.elo = ""
            while not self.selected_player.elo.isnumeric():
                self.selected_player.elo = self.enter_new_value(field_title="ELO")

    def display_current_value(self, field_title: str, value: Any):
        """Displays the current value of a player's information.

        Args:
            field_title (str): Title to display.
            value (Any): Value to display.
        """

        parameter = typer.style(f"\n{field_title}: ", bold=True)
        typer.echo(parameter + value)

    def ask_for_edit(self):
        """Asks the user for information edit.

        Returns:
            bool: User want to edit this field.
        """

        confirm = typer.confirm("Modifier cette information?")

        if confirm:
            self.modification_made = True

        return confirm

    def enter_new_value(self, field_title: str):
        """Displays a prompt for a new value.

        Args:
            field_title (str): Title to display.

        Returns:
            str: New value given by the user.
        """

        new_value = typer.prompt(f"Entrez une nouvelle valeur pour '{field_title}'")

        return new_value

    def dob_is_valid(self):
        """Verifies if the date entered by the user is valid using datetime library.

        Returns:
            bool: The date exists.
        """

        try:
            datetime.strptime(self.selected_player.dob, "%d/%m/%Y")
            return True
        except ValueError:
            if len(self.selected_player.dob) > 0:
                typer.secho("Date incorrecte", fg=typer.colors.RED)
            return False

    def gender_is_valid(self):
        """Verifies if the gender entered by the user is valid.

        Returns:
            bool: The gender is valid.
        """

        if len(self.selected_player.gender) == 0:
            return False
        elif self.selected_player.gender.lower() == "h":
            self.selected_player.gender = "H"
            return True
        elif self.selected_player.gender.lower() == "f":
            self.selected_player.gender = "F"
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

        confirm = typer.confirm("\nSouhaitez vous confirmer la modification de ce joueur ?")
        if not confirm:
            typer.secho("Annulation. Le joueur n'a pas été modifié.", fg=typer.colors.RED)
            raise typer.Exit

    def list_settings(self):
        """Displays all previously entered player settings."""

        typer.secho("\nNouvelles informations du joueur:", fg=typer.colors.BLUE)

        parameter = typer.style("Prénom: ", bold=True)
        typer.echo(parameter + self.selected_player.first_name)
        parameter = typer.style("Nom de famille: ", bold=True)
        typer.echo(parameter + self.selected_player.last_name)
        parameter = typer.style("Date de naissance: ", bold=True)
        typer.echo(parameter + self.selected_player.dob)
        parameter = typer.style("Genre: ", bold=True)
        typer.echo(parameter + self.selected_player.gender)
        parameter = typer.style("ELO: ", bold=True)
        typer.echo(parameter + str(self.selected_player.elo))

    def save_player(self):
        """Uses database handler to save edited player."""

        _DATABASE_HANDLER.create_player(
            first_name=self.selected_player.first_name,
            last_name=self.selected_player.last_name,
            dob=self.selected_player.dob,
            gender=self.selected_player.gender,
            elo=self.selected_player.elo,
            id_num=self.selected_player.id_num,
        )

        typer.secho(f"Le joueur n°{str(self.selected_player.id_num)} a été modifié.", fg=typer.colors.GREEN)