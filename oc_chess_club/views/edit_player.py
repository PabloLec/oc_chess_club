import typer

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

        new_value = _HELPER.edit_prompt(field_title="Prénom", value=self.selected_player.first_name)
        if new_value != self.selected_player.first_name:
            self.modification_made = True
            self.selected_player.first_name = new_value

    def select_last_name(self):
        """Handles player's last name edit."""

        new_value = _HELPER.edit_prompt(field_title="Nom de famille", value=self.selected_player.last_name)
        if new_value != self.selected_player.last_name:
            self.modification_made = True
            self.selected_player.last_name = new_value

    def select_dob(self):
        """Handles player's date of birth edit."""

        new_value = _HELPER.edit_prompt(field_title="Date de naissance", value=self.selected_player.dob)
        if new_value != self.selected_player.dob:
            self.modification_made = True
            self.selected_player.dob = new_value

    def select_gender(self):
        """Handles player's gender edit."""

        new_value = _HELPER.edit_prompt(field_title="Genre", value=self.selected_player.gender)
        if new_value != self.selected_player.gender:
            self.modification_made = True
            self.selected_player.gender = new_value

    def select_elo(self):
        """Handles player's ELo ranking edit."""

        new_value = _HELPER.edit_prompt(field_title="ELO", value=str(self.selected_player.elo))
        if new_value != str(self.selected_player.elo):
            self.modification_made = True
            self.selected_player.elo = new_value

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