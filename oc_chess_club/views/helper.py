import typer

from typing import Any
from datetime import datetime

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER


def select_player():
    """Prompts the user to select a player in database."""

    list_all_players()

    selection = ""
    while not player_exists(selected_id=selection):
        selection = typer.prompt(f"Sélectionnez un joueur")

    return _DATABASE_HANDLER.helper.player_object_from_id_str(player_id=selection)


def list_all_players():
    typer.secho("Liste des joueurs existants:\n", fg=typer.colors.BLUE)

    all_players = _DATABASE_HANDLER.helper.get_players_by_id()

    for player in all_players:
        player_id = typer.style(str(player.id_num), bold=True)
        typer.echo(f"{player_id}. {player.first_name} {player.last_name}")


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

    if _DATABASE_HANDLER.helper.is_player_id_in_database(player_id=int(selected_id)):
        return True

    typer.secho(f"Pas de joueur avec le numéro {selected_id}", fg=typer.colors.RED)

    return False


def edit_prompt(field_title: str, value: Any):
    display_current_value(field_title=field_title, value=value)

    if ask_for_edit():
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
