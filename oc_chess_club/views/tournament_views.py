import typer

from datetime import datetime
from copy import deepcopy

from oc_chess_club.controller.database_handler import DatabaseHandler
import oc_chess_club.views.helper as _HELPER
from oc_chess_club.views.game import GameMenu


class TournamentMenu:
    """View for tournament related operations."""

    def __init__(self):
        """Constructor for TournamentMenu."""

        _HELPER.print_title("menu des tournois")

        self.print_menu()
        self.user_selection()

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Reprendre un tournoi")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Créer un nouveau tournoi")

        number = typer.style("3. ", bold=True)
        typer.echo(number + "Modifier un tournoi")

        number = typer.style("4. ", bold=True)
        typer.echo(number + "Supprimer un tournoi")

        number = typer.style("5. ", bold=True)
        typer.echo(number + "Afficher tous les tournois")

        number = typer.style("\n0. ", bold=True)
        typer.echo(number + "Retour")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("Entrez votre sélection: ")

        if selection == "0":
            typer.echo("\n\n")
            _HELPER.go_back(current_view=self.__class__.__name__)
        elif selection == "1":
            typer.echo("\n\n")
            LoadTournamentMenu()
        elif selection == "2":
            typer.echo("\n\n")
            NewTournamentMenu()
        elif selection == "3":
            typer.echo("\n\n")
            EditTournamentMenu()
        elif selection == "4":
            typer.echo("\n\n")
            DeleteTournamentMenu()
        elif selection == "5":
            typer.echo("\n\n")
            _HELPER.list_all_tournaments()
            typer.echo("\n")
            self.user_selection()
        else:
            self.user_selection()


class LoadTournamentMenu:
    """View displayed for tournament loading.

    Attributes:
        available_tournaments (list): Unfinished tournaments available for loading.
    """

    def __init__(self, tournament_id: int = None):
        """Constructor for LoadTournamentMenu.

        Args:
            tournament_id (int, optional): Optional tournament id to be loaded. Defaults to None.
        """

        _HELPER.print_title("chargement d'un tournoi")

        self.available_tournaments = DatabaseHandler().helper.get_unfinished_tournaments()

        self.cli_argument_handler(tournament_id=tournament_id)

        self.display_unfinished_tournaments()

        if len(self.available_tournaments) == 0:
            _HELPER.print_error("aucun tournoi en cours.")
            _HELPER.go_back(current_view=self.__class__.__name__)
            return

        self.user_selection()

        _HELPER.go_back(current_view=self.__class__.__name__)

    def cli_argument_handler(self, tournament_id: str):
        """Handles eventual tournament id passed at instantiation.

        Args:
            tournament_id (str): Optional tournament id to be loaded.
        """

        tournament_is_available = (
            DatabaseHandler().helper.get_tournament_object_from_id_str(tournament_id=str(tournament_id))
            in self.available_tournaments
        )

        if tournament_id is not None and not tournament_is_available:
            _HELPER.print_error(
                f"le tournoi n°{tournament_id} n'est pas disponible.",
            )
        elif tournament_id is not None and tournament_is_available:
            self.start_tournament(tournament_id=tournament_id)
            _HELPER.go_back(current_view=self.__class__.__name__)

    def display_unfinished_tournaments(self):
        """Uses database handler to find and display unfinished tournament for the user to choose from."""
        for tournament in self.available_tournaments:

            typer.secho(f" - Tournoi n°{tournament.id_num} -", fg=typer.colors.CYAN)
            parameter = typer.style("Nom: ", bold=True)
            typer.echo(parameter + tournament.name)
            parameter = typer.style("Date: ", bold=True)
            typer.echo(parameter + tournament.date + "\n")

    def user_selection(self):
        """Prompts the user to select a tournament to be loaded."""

        selection = typer.prompt("Entrez un numéro de tournoi")

        available_ids = [x.id_num for x in self.available_tournaments]

        while not selection.isnumeric() or int(selection) not in available_ids:
            _HELPER.print_error(f"pas de tournoi avec le numéro {selection}")
            self.user_selection()
            return

        self.start_tournament(int(selection))

    def start_tournament(self, tournament_id):
        """Opens the Game Menu for selected tournament.

        Args:
            tournament_id (int): Unique id of the tournament to be loaded.
        """

        GameMenu(tournament_id)


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

        _HELPER.print_title("création d'un tournoi")

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

        _HELPER.print_info("entrez les informations du tournoi.")

        while len(self.tournament_name) == 0:
            self.tournament_name = typer.prompt("Nom du tournoi")

        while len(self.location) == 0:
            self.location = typer.prompt("Lieu")

        while not _HELPER.date_is_valid(date=self.date):
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

        _HELPER.list_all_players()

        while len(self.players) < 8:
            selection = typer.prompt(f"Joueur ({str(len(self.players))}/8)")

            if _HELPER.player_exists(selected_id=selection, already_taken_ids=self.players):
                self.players.append(int(selection))

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
                _HELPER.print_error("entrée incorrect. Entrez Bullet, Blitz ou Coup Rapide.")
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
            typer.print_error("annulation. Le tournoi n'a pas été créé.")
            raise typer.Exit

    def list_settings(self):
        """Displays all previously entered tournament settings."""

        _HELPER.print_info("paramètres du tournoi:")

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

        _HELPER.print_info("liste des joueurs: ")

        players_name = DatabaseHandler().helper.get_players_names(players_sample=self.players)

        for name in players_name:
            typer.echo(f" - {name}")

    def save_tournament(self):
        """Uses database handler to save created tournament."""

        self.created_tournament_id = DatabaseHandler().create_tournament(
            name=self.tournament_name,
            location=self.location,
            date=self.date,
            number_of_rounds=int(self.number_of_rounds),
            time_control=self.time_control,
            description=self.description,
            players=self.players,
            leaderboard={},
        )

        _HELPER.print_success("le tournoi a été créé.")

    def start_tournament(self):
        """Starts created tournament if the user select so."""

        confirm = typer.confirm("\nSouhaitez vous commencer le tournoi ?")

        if confirm:
            GameMenu(tournament_id=self.created_tournament_id)
        else:
            _HELPER.go_back(current_view=self.__class__.__name__)


class EditTournamentMenu:
    """View for tournament editing.

    Attributes:
        selected_tournament (Tournament): Tournament selected by user for edit.
        original_tournament_copy (Tournament): Deep copy of initial Tournament state for modification check.
    """

    def __init__(self, tournament_id: int = None):
        """Constructor for EditTournamentMenu.

        Args:
            tournament_id (int, optional): Optional tournament id to be loaded. Defaults to None.
        """

        _HELPER.print_title("modification d'un tournoi")

        self.cli_argument_handler(tournament_id=tournament_id)

        if self.selected_tournament is None:
            _HELPER.print_error("aucun tournoi créé.")
            _HELPER.go_back(current_view=self.__class__.__name__)
            return

        self.original_tournament_copy = deepcopy(self.selected_tournament)

        self.select_edit()

        if self.is_tournament_edited():
            self.confirm_settings()
            self.save_tournament()
        else:
            _HELPER.print_success("aucune modification effectuée.")

        _HELPER.go_back(current_view=self.__class__.__name__)

    def cli_argument_handler(self, tournament_id: str):
        """Handles eventual tournament id passed at instantiation.

        Args:
            tournament_id (str): Optional tournament id to be loaded.
        """

        tournament_exists = DatabaseHandler().helper.is_tournament_id_in_database(tournament_id=tournament_id)

        if tournament_id is not None and not tournament_exists:
            _HELPER.print_error(f"le tournoi n°{tournament_id} n'est pas disponible.")

        if tournament_id is not None and tournament_exists:
            self.selected_tournament = DatabaseHandler().helper.get_tournament_object_from_id_str(
                tournament_id=str(tournament_id)
            )
        else:
            self.selected_tournament = _HELPER.select_tournament()

    def select_edit(self):
        """Enumerates all tournament's settings and asks for edit."""

        _HELPER.print_info("informations actuelles du tournoi:")

        self.selected_tournament.name = _HELPER.edit_prompt(field_title="Nom", value=self.selected_tournament.name)
        self.selected_tournament.location = _HELPER.edit_prompt(
            field_title="Lieu", value=self.selected_tournament.location
        )
        self.selected_tournament.date = _HELPER.edit_prompt(field_title="Date", value=self.selected_tournament.date)
        self.selected_tournament.description = _HELPER.edit_prompt(
            field_title="Description", value=self.selected_tournament.description
        )

    def is_tournament_edited(self):
        """Compares selected tournament object and original tournament copy for difference.

        Returns:
            bool: The Tournament attributes were modified.
        """

        if self.selected_tournament.name != self.original_tournament_copy.name:
            return True
        elif self.selected_tournament.location != self.original_tournament_copy.location:
            return True
        elif self.selected_tournament.date != self.original_tournament_copy.date:
            return True
        elif self.selected_tournament.description != self.original_tournament_copy.description:
            return True
        else:
            return False

    def confirm_settings(self):
        """Prompts the user to confirm the settings previously entered.

        Raises:
            typer.Exit: Exits if the user cancels the creation.
        """

        self.list_settings()

        confirm = typer.confirm("\nSouhaitez vous confirmer la modification de ce tournoi ?")
        if not confirm:
            _HELPER.print_error("annulation. Le tournoi n'a pas été modifié.")
            raise typer.Exit

    def list_settings(self):
        """Displays all previously entered tournament settings."""

        _HELPER.print_info("nouvelles informations du tournoi:")

        parameter = typer.style("Nom: ", bold=True)
        typer.echo(parameter + self.selected_tournament.name)
        parameter = typer.style("Lieu: ", bold=True)
        typer.echo(parameter + self.selected_tournament.location)
        parameter = typer.style("Date: ", bold=True)
        typer.echo(parameter + self.selected_tournament.date)
        parameter = typer.style("Description: ", bold=True)
        typer.echo(parameter + self.selected_tournament.description)

    def save_tournament(self):
        """Uses database handler to save edited tournament."""

        # Tranform list of Player objects to list of player ids
        self.selected_tournament.players = [x.id_num for x in self.selected_tournament.players]

        DatabaseHandler().create_tournament(
            name=self.selected_tournament.name,
            location=self.selected_tournament.location,
            date=self.selected_tournament.date,
            number_of_rounds=int(self.selected_tournament.number_of_rounds),
            time_control=self.selected_tournament.time_control,
            description=self.selected_tournament.description,
            players=self.selected_tournament.players,
            leaderboard=self.selected_tournament.leaderboard,
            is_finished=self.selected_tournament.is_finished,
            id_num=self.selected_tournament.id_num,
        )

        _HELPER.print_success(f"le tournoi n°{str(self.selected_tournament.id_num)} a été modifié.")


class DeleteTournamentMenu:
    """View for tournament deletion

    Attributes:
        selected_tournament (Tournament): Tournament selected by user for deletion.
    """

    def __init__(self, tournament_id: int = None):
        """Constructor for DeleteTournamentMenu.

        Args:
            tournament_id (int, optional): Optional tournament id to be loaded. Defaults to None.
        """

        _HELPER.print_title("suppression d'un tournoi")

        self.cli_argument_handler(tournament_id=tournament_id)

        if self.selected_tournament is None:
            _HELPER.print_error("aucun tournoi créé.")
            _HELPER.go_back(current_view=self.__class__.__name__)
            return

        self.confirm_selection()

        _HELPER.go_back(current_view=self.__class__.__name__)

    def cli_argument_handler(self, tournament_id: str):
        """Handles eventual tournament id passed at instantiation.

        Args:
            tournament_id (str): Optional tournament id to be loaded.
        """

        tournament_exists = DatabaseHandler().helper.is_tournament_id_in_database(tournament_id=tournament_id)

        if tournament_id is not None and not tournament_exists:
            _HELPER.print_error(f"le tournoi n°{tournament_id} n'est pas disponible.")

        if tournament_id is not None and tournament_exists:
            self.selected_tournament = DatabaseHandler().helper.get_tournament_object_from_id_str(
                tournament_id=str(tournament_id)
            )
        else:
            self.selected_tournament = _HELPER.select_tournament()

    def confirm_selection(self):
        """Prompts the user to confirm tournament deletion."""

        _HELPER.print_warning(f"Vous allez supprimer définitivement le tournoi '{self.selected_tournament.name}'")

        confirm = typer.confirm("Confirmer la suppression ?")

        if confirm:
            self.delete_tournament()
        else:
            typer.secho("\n Le tournoi n'a pas été supprimé", fg=typer.colors.GREEN)

    def delete_tournament(self):
        """Uses database handler to delete tournament."""

        DatabaseHandler().delete_tournament(tournament=self.selected_tournament)