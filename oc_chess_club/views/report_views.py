import typer

from oc_chess_club.controller.config_loader import _CONFIG
from oc_chess_club.controller.database_handler import DatabaseHandler
from oc_chess_club.controller.report_handler import ReportHandler
import oc_chess_club.views.helper as _HELPER

from oc_chess_club.models.tournament import Tournament


class ReportMenu:
    """View for report related operations."""

    def __init__(self):
        """Constructor for TournamentMenu."""

        if not _CONFIG.report_save_path_exists():
            _HELPER.print_error(
                "Le chemin de sauvegarde des rapports n'existe pas, vous ne pouvez donc pas en générer."
            )
            _HELPER.go_back(current_view=self.__class__.__name__)

        _HELPER.print_title("menu des rapports")

        self.print_menu()
        self.user_selection()

        _HELPER.go_back(current_view=self.__class__.__name__)

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Joueurs")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Tournois")

        number = typer.style("\n0. ", bold=True)
        typer.echo(number + "Retour")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("Entrez votre sélection: ")

        if selection == "0":
            typer.echo("\n\n")
            _HELPER.go_back(current_view=self.__class__.__name__)
        elif selection == "1":
            PlayerReportMenu()
        elif selection == "2":
            TournamentReportMenu()
        else:
            self.user_selection()


class PlayerReportMenu:
    """View for player related reports."""

    def __init__(self):
        """Constructor for PlayerReportMenu."""

        _HELPER.print_title("rapport des joueurs")

        if DatabaseHandler().helper.is_player_db_empty():
            _HELPER.print_error("aucun joueur créé.")
            _HELPER.go_back(current_view=self.__class__.__name__)
            return

        self.report_handler = ReportHandler()

        self.print_menu()
        self.user_selection()

        _HELPER.go_back(current_view=self.__class__.__name__)

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Par Nom")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Par ELO")

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
            self.report_handler.all_players_by_name()
        elif selection == "2":
            typer.echo("\n\n")
            self.report_handler.all_players_by_elo()
        else:
            self.user_selection()
            return

        _HELPER.print_report(self.report_handler.data)
        export_format = _HELPER.report_export_prompt()

        if export_format is not None:
            save_path = self.report_handler.init_export(export_format)

        _HELPER.print_success(f"rapport enregistré sous: {save_path}")


class TournamentReportMenu:
    """View for tournament related reports."""

    def __init__(self):
        """Constructor for TournamentReportMenu."""

        _HELPER.print_title("rapport des tournois")

        if DatabaseHandler().helper.is_tournament_db_empty():
            _HELPER.print_error("aucun joueur créé.")
            _HELPER.go_back(current_view=self.__class__.__name__)
            return

        self.report_handler = ReportHandler()

        self.print_menu()
        self.user_selection()

        _HELPER.go_back(current_view=self.__class__.__name__)

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Tous les tournois")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Joueurs d'un tournoi")

        number = typer.style("3. ", bold=True)
        typer.echo(number + "Rounds d'un tournoi")

        number = typer.style("4. ", bold=True)
        typer.echo(number + "Matchs d'un tournoi")

        number = typer.style("\n0. ", bold=True)
        typer.echo(number + "Retour")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("Entrez votre sélection: ")

        if selection == "0":
            typer.echo("\n\n")
            _HELPER.go_back(current_view=self.__class__.__name__)
            return

        elif selection == "1":
            typer.echo("\n\n")
            self.report_handler.all_tournaments()

        elif selection == "2":
            self.tournament_players_sub_menu()

        elif selection == "3":
            selected_tournament = _HELPER.select_tournament()
            if len(selected_tournament.rounds) == 0:
                _HELPER.print_error("le tournoi ne comporte aucun round.")
                _HELPER.go_back(current_view=self.__class__.__name__)
                return
            self.report_handler.tournament_rounds(tournament=selected_tournament)

        elif selection == "4":
            selected_tournament = _HELPER.select_tournament()
            if len(selected_tournament.rounds) == 0:
                _HELPER.print_error("le tournoi ne comporte aucun match.")
                _HELPER.go_back(current_view=self.__class__.__name__)
                return
            self.report_handler.tournament_matches(tournament=selected_tournament)

        else:
            self.user_selection()
            return

        _HELPER.print_report(self.report_handler.data)
        export_format = _HELPER.report_export_prompt()

        if export_format is not None:
            save_path = self.report_handler.init_export(export_format)

        _HELPER.print_success(f"rapport enregistré sous: {save_path}")

    def tournament_players_sub_menu(self):
        """Sub-menu for tournament's players report."""

        selected_tournament = _HELPER.select_tournament()

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Par Nom")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Par ELO")

        number = typer.style("\n0. ", bold=True)
        typer.echo(number + "Retour")

        self.tournament_players_sub_menu_selection(selected_tournament=selected_tournament)

    def tournament_players_sub_menu_selection(self, selected_tournament: Tournament):
        """User prompt for tournament's players report sub-menu.

        Args:
            selected_tournament (Tournament): Tournament previously selected.
        """

        selection = typer.prompt("Entrez votre sélection: ")

        if selection == "0":
            typer.echo("\n\n")
            _HELPER.go_back(current_view=self.__class__.__name__)
        elif selection == "1":
            typer.echo("\n\n")
            self.report_handler.tournament_players_by_name(tournament=selected_tournament)
        elif selection == "2":
            self.report_handler.tournament_players_by_elo(tournament=selected_tournament)
        else:
            self.user_selection()
            return