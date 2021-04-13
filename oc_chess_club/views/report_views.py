import typer


from oc_chess_club.controller.database_handler import DatabaseHandler
from oc_chess_club.controller.report_handler import ReportHandler
import oc_chess_club.views.helper as _HELPER

from oc_chess_club.models.tournament import Tournament


class ReportMenu:
    """View for report related operations."""

    def __init__(self):
        """Constructor for TournamentMenu."""

        typer.secho("MENU DES RAPPORTS", fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_CYAN, bold=True, underline=True)

        self.print_menu()
        self.user_selection()

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

        typer.secho(
            "RAPPORT DES JOUEURS", fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_CYAN, bold=True, underline=True
        )

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

        typer.secho(f"\nRapport enregistré sous: {save_path}\n", fg=typer.colors.GREEN)


class TournamentReportMenu:
    """View for tournament related reports."""

    def __init__(self):
        """Constructor for TournamentReportMenu."""

        typer.secho(
            "RAPPORT DES TOURNOIS", fg=typer.colors.BLACK, bg=typer.colors.BRIGHT_CYAN, bold=True, underline=True
        )

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
        elif selection == "1":
            typer.echo("\n\n")
            self.report_handler.all_tournaments()
        elif selection == "2":
            self.tournament_players_sub_menu()
        elif selection == "3":
            selected_tournament = _HELPER.select_tournament()
            self.report_handler.tournament_rounds(tournament=selected_tournament)
        elif selection == "4":
            selected_tournament = _HELPER.select_tournament()
            self.report_handler.tournament_matches(tournament=selected_tournament)
        else:
            self.user_selection()
            return

        _HELPER.print_report(self.report_handler.data)
        export_format = _HELPER.report_export_prompt()

        if export_format is not None:
            save_path = self.report_handler.init_export(export_format)

        typer.secho(f"\nRapport enregistré sous: {save_path}\n", fg=typer.colors.GREEN)

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