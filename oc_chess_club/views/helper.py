import typer

from typing import Any
from datetime import datetime

from oc_chess_club.controller.database_handler import DatabaseHandler
import oc_chess_club.views.main_menu as _MAIN_MENU
import oc_chess_club.views.player_views as _PLAYER_VIEWS
import oc_chess_club.views.tournament_views as _TOURNAMENT_VIEWS
import oc_chess_club.views.report_views as _REPORT_VIEWS


def go_back(current_view: str):
    if current_view in ["TournamentMenu", "PlayerMenu", "ReportMenu", "GameMenu"]:
        _MAIN_MENU.MainMenu()
    elif current_view in ["NewTournamentMenu", "LoadTournamentMenu", "EditTournamentMenu", "DeleteTournamentMenu"]:
        _TOURNAMENT_VIEWS.TournamentMenu()
    elif current_view in ["NewPlayerMenu", "EditPlayerMenu", "DeletePlayerMenu"]:
        _PLAYER_VIEWS.PlayerMenu()
    elif current_view in ["PlayerReportMenu", "TournamentReportMenu"]:
        _REPORT_VIEWS.ReportMenu()


def select_player():
    """Prompts the user to select a player in database."""

    if DatabaseHandler().helper.is_player_db_empty():
        return None

    list_all_players()

    selection = ""
    while not player_exists(selected_id=selection):
        selection = typer.prompt(f"Sélectionnez un joueur")

    return DatabaseHandler().helper.get_player_object_from_id_str(player_id=selection)


def select_tournament():
    """Prompts the user to select a tournament in database."""

    if DatabaseHandler().helper.is_tournament_db_empty():
        return None

    list_all_tournaments()

    selection = ""
    while not tournament_exists(selected_id=selection):
        selection = typer.prompt(f"Sélectionnez un tournoi")

    return DatabaseHandler().helper.get_tournament_object_from_id_str(tournament_id=selection)


def list_all_tournaments():
    """Lists all existing tournaments."""

    if DatabaseHandler().helper.is_tournament_db_empty():
        typer.secho("Aucun tournoi créé.", fg=typer.colors.RED)
        return

    typer.secho("Liste des tournois existants:\n", fg=typer.colors.BLUE)

    all_tournaments = DatabaseHandler().helper.get_tournaments_by_id()

    for tournament in all_tournaments:
        tournament_id = typer.style(str(tournament.id_num), bold=True)
        if tournament.is_finished:
            is_finished = typer.style(" -> Terminé", fg=typer.colors.YELLOW)
        else:
            is_finished = ""
        typer.echo(f"{tournament.id_num}. {tournament.name} - {tournament.date}" + is_finished)


def list_all_players():
    typer.secho("Liste des joueurs existants:\n", fg=typer.colors.BLUE)

    all_players = DatabaseHandler().helper.get_players_by_id()

    for player in all_players:
        player_id = typer.style(str(player.id_num), bold=True)
        typer.echo(f"{player_id}. {player.first_name} {player.last_name}")


def tournament_exists(selected_id: str):
    """Verifies if the tournament selected by the user exists.

    Args:
        selected_id (str): Tournament chosen by the user.

    Returns:
        bool: The tournament is selectable.
    """

    if len(selected_id) == 0:
        return False

    if not selected_id.isnumeric():
        typer.secho("Entrez le numéro du tournoi apparaissant devant son nom", fg=typer.colors.RED)
        return False

    if DatabaseHandler().helper.is_tournament_id_in_database(tournament_id=int(selected_id)):
        return True

    typer.secho(f"Pas de tournoi avec le numéro {selected_id}", fg=typer.colors.RED)

    return False


def player_exists(selected_id: str, already_taken_ids: list = []):
    """Verifies if the player selected by the user exists.

    Args:
        selected_id (str): Player chosen by the user.
        already_taken_ids (list, optional): List of ids the user cannot choose from. Defaults to [].

    Returns:
        bool: The user is selectable.
    """

    if len(selected_id) == 0:
        return False

    if not selected_id.isnumeric():
        typer.secho("Entrez le numéro du joueur apparaissant devant son nom", fg=typer.colors.RED)
        return False

    if int(selected_id) in already_taken_ids:
        typer.secho(f"Le joueur numéro {selected_id} a déjà été ajouté", fg=typer.colors.RED)
        return False

    if DatabaseHandler().helper.is_player_id_in_database(player_id=int(selected_id)):
        return True

    typer.secho(f"Pas de joueur avec le numéro {selected_id}", fg=typer.colors.RED)

    return False


def edit_prompt(field_title: str, value: Any):
    display_current_value(field_title=field_title, value=value)

    if not ask_for_edit():
        return value

    value = ""

    if "date" in field_title.lower():
        while not date_is_valid(date=value):
            value = enter_new_value(field_title=field_title)
    elif "genre" in field_title.lower():
        while not gender_is_valid(gender=value):
            value = enter_new_value(field_title=field_title)
    elif "elo" in field_title.lower():
        while not value.isnumeric():
            value = enter_new_value(field_title=field_title)
    else:
        while len(value) == 0:
            value = enter_new_value(field_title=field_title)

    return value


def display_current_value(field_title: str, value: Any):
    """Displays the current value of a field.

    Args:
        field_title (str): Title to display.
        value (Any): Value to display.
    """

    parameter = typer.style(f"\n{field_title}: ", bold=True)
    typer.echo(parameter + str(value))


def ask_for_edit():
    """Asks the user for information edit.

    Returns:
        bool: User want to edit this field.
    """

    confirm = typer.confirm("Modifier cette information?")

    return confirm


def enter_new_value(field_title: str):
    """Displays a prompt for a new value.

    Args:
        field_title (str): Title to display.

    Returns:
        str: New value given by the user.
    """

    new_value = typer.prompt(f"Entrez une nouvelle valeur pour '{field_title}'")

    return new_value


def date_is_valid(date: str):
    """Verifies if the date entered by the user is valid using datetime library.

    Returns:
        bool: The date exists.
    """

    try:
        datetime.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        if len(date) > 0:
            typer.secho("Date incorrecte", fg=typer.colors.RED)
        return False


def gender_is_valid(gender: str):
    """Verifies if the gender entered by the user is valid.

    Returns:
        bool: The gender is valid.
    """

    if len(gender) == 0:
        return False
    elif gender.lower() == "h":
        gender = "H"
        return True
    elif gender.lower() == "f":
        gender = "F"
        return True
    else:
        typer.secho("Genre incorrect. Entrez H ou F.", fg=typer.colors.RED)
        return False


def print_report(data: dict):

    for element in data:
        for key in element:
            field_name = key + ": "
            value = typer.style(str(element[key]), bold=True)
            typer.echo(field_name + value)
        typer.echo("\n")


def report_export_prompt():
    if not ask_for_report_export():
        return None

    return select_export_format()


def ask_for_report_export():
    typer.secho("Souhaitez vous exporter ce rapport ?\n", fg=typer.colors.BLUE)

    number = typer.style("1. ", bold=True)
    typer.echo(number + "Oui")

    number = typer.style("2. ", bold=True)
    typer.echo(number + "Non")

    selection = ""

    while selection not in ["1", "2"]:
        selection = typer.prompt("Entrez votre sélection: ")

    if selection == "1":
        return True
    elif selection == "2":
        return False


def select_export_format():
    typer.secho("\nChoisissez un format d'export:\n", fg=typer.colors.BLUE)

    number = typer.style("1. ", bold=True)
    typer.echo(number + "Texte")

    number = typer.style("2. ", bold=True)
    typer.echo(number + "CSV")

    number = typer.style("\n0. ", bold=True)
    typer.echo(number + "Retour")

    selection = ""

    while selection not in ["1", "2", "0"]:
        selection = typer.prompt("Entrez votre sélection: ")

    if selection == "0":
        return None
    if selection == "1":
        return "txt"
    elif selection == "2":
        return "csv"