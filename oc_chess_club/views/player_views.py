import typer

from datetime import datetime
from copy import deepcopy

from oc_chess_club.controller.database_handler import DatabaseHandler
import oc_chess_club.views.helper as _HELPER


class PlayerMenu:
    """View for player related operations."""

    def __init__(self):
        """Constructor for PlayerMenu."""

        typer.secho("MENU DES JOUEURS", fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_CYAN, bold=True, underline=True)

        self.print_menu()
        self.user_selection()

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Créer un nouveau joueur")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Modifier un joueur")

        number = typer.style("3. ", bold=True)
        typer.echo(number + "Supprimer un joueur")

        number = typer.style("4. ", bold=True)
        typer.echo(number + "Afficher tous les joueurs")

        number = typer.style("\n0. ", bold=True)
        typer.echo(number + "Retour")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("\nEntrez votre sélection: ")

        if selection == "0":
            _HELPER.go_back(current_view=self.__class__.__name__)
        elif selection == "1":
            typer.echo("\n\n")
            NewPlayerMenu()
        elif selection == "2":
            typer.echo("\n\n")
            EditPlayerMenu()
        elif selection == "3":
            typer.echo("\n\n")
            DeletePlayerMenu()
        elif selection == "4":
            typer.echo("\n\n")
            _HELPER.list_all_players()
            typer.echo("\n")
            self.user_selection()
        else:
            self.user_selection()


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

        typer.secho(
            "CREATION D'UN JOUEUR", fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_CYAN, bold=True, underline=True
        )

        self.first_name = ""
        self.last_name = ""
        self.dob = ""
        self.gender = ""
        self.elo = ""

        self.settings_prompt()
        self.confirm_settings()
        self.save_player()

        _HELPER.go_back(current_view=self.__class__.__name__)

    def settings_prompt(self):
        """Prompts the user to input the different player settings."""

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

        created_player_id = DatabaseHandler().create_player(
            first_name=self.first_name,
            last_name=self.last_name,
            dob=self.dob,
            gender=self.gender,
            elo=int(self.elo),
        )

        typer.secho(f"Le joueur a été créé avec le numéro {created_player_id}.", fg=typer.colors.GREEN)


class EditPlayerMenu:
    """View for player editing.

    Attributes:
        selected_player (Player): Player selected by user for edit.
        original_player_copy (Player): Deep copy of initial Player state for modification check.
    """

    def __init__(self):
        """Constructor for EditPlayerMenu."""

        typer.secho(
            "MODIFICATION D'UN JOUEUR", fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_CYAN, bold=True, underline=True
        )

        self.selected_player = _HELPER.select_player()

        if self.selected_player is None:
            typer.secho(f"Aucun joueur créé.\n", fg=typer.colors.RED)
            _HELPER.go_back(current_view=self.__class__.__name__)
            return

        self.original_player_copy = deepcopy(self.selected_player)

        self.select_edit()

        if self.is_player_edited():
            self.confirm_settings()
            self.save_player()
        else:
            typer.secho("\nAucune modification effectuée.\n", fg=typer.colors.GREEN)

        _HELPER.go_back(current_view=self.__class__.__name__)

    def select_edit(self):
        """Enumerates all player's settings and asks for edit."""

        typer.secho("\nInformations actuelles du joueur:\n", fg=typer.colors.BLUE)

        self.selected_player.first_name = _HELPER.edit_prompt(
            field_title="Prénom", value=self.selected_player.first_name
        )
        self.selected_player.last_name = _HELPER.edit_prompt(
            field_title="Nom de famille", value=self.selected_player.last_name
        )
        self.selected_player.dob = _HELPER.edit_prompt(field_title="Date de naissance", value=self.selected_player.dob)
        self.selected_player.gender = _HELPER.edit_prompt(field_title="Genre", value=self.selected_player.gender)
        self.selected_player.elo = _HELPER.edit_prompt(field_title="ELO", value=str(self.selected_player.elo))

    def is_player_edited(self):
        """Compares selected player object and original player copy for difference.

        Returns:
            bool: The Player attributes were modified.
        """

        if self.selected_player.first_name != self.original_player_copy.first_name:
            return True
        elif self.selected_player.last_name != self.original_player_copy.last_name:
            return True
        elif self.selected_player.dob != self.original_player_copy.dob:
            return True
        elif self.selected_player.gender != self.original_player_copy.gender:
            return True
        elif int(self.selected_player.elo) != self.original_player_copy.elo:
            return True
        else:
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

        DatabaseHandler().create_player(
            first_name=self.selected_player.first_name,
            last_name=self.selected_player.last_name,
            dob=self.selected_player.dob,
            gender=self.selected_player.gender,
            elo=self.selected_player.elo,
            id_num=self.selected_player.id_num,
        )

        typer.secho(f"Le joueur n°{str(self.selected_player.id_num)} a été modifié.", fg=typer.colors.GREEN)


class DeletePlayerMenu:
    """View for player deletion

    Attributes:
        selected_player (Player): Player selected by user for deletion.
    """

    def __init__(self):
        """Constructor for DeletePlayerMenu."""

        typer.secho(
            "SUPPRESSION D'UN JOUEUR", fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_CYAN, bold=True, underline=True
        )

        self.selected_player = _HELPER.select_player()

        if self.selected_player is None:
            typer.secho(f"Aucun joueur créé.\n", fg=typer.colors.RED)
            _HELPER.go_back(current_view=self.__class__.__name__)
            return

        self.confirm_selection()

        _HELPER.go_back(current_view=self.__class__.__name__)

    def confirm_selection(self):
        """Prompts the user to confirm user deletion."""

        typer.secho(
            "\nVous allez supprimer définitivement {first_name} {last_name}".format(
                first_name=self.selected_player.first_name, last_name=self.selected_player.last_name
            ),
            fg=typer.colors.RED,
        )

        confirm = typer.confirm("Confirmer la suppression ?")

        if confirm:
            self.delete_player()
        else:
            typer.secho("\n L'utilisateur n'a pas été supprimé", fg=typer.colors.GREEN)

    def delete_player(self):
        """Uses database handler to delete player."""

        DatabaseHandler().delete_player(player=self.selected_player)