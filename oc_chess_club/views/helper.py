import typer

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