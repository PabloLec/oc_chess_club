from typing import Optional

import typer

from oc_chess_club.controller.config_loader import _CONFIG
from oc_chess_club.views.main_menu import MainMenu
import oc_chess_club.views.tournament_views as _TOURNAMENT_VIEWS
import oc_chess_club.views.player_views as _PLAYER_VIEWS
import oc_chess_club.views.report_views as _REPORT_VIEWS

_MAIN_TYPER_APP = typer.Typer()
_TOURNAMENT_APP = typer.Typer()
_PLAYER_APP = typer.Typer()
_REPORT_APP = typer.Typer()

_MAIN_TYPER_APP.add_typer(_TOURNAMENT_APP, name="tournament")
_MAIN_TYPER_APP.add_typer(_PLAYER_APP, name="player")
_MAIN_TYPER_APP.add_typer(_REPORT_APP, name="report")


def verify_config():
    if not _CONFIG.database_exists():
        typer.secho("\nLe fichier pour la base de données n'existe pas.", fg=typer.colors.RED, blink=True)
        typer.secho(
            "Si vous utilisez le programme pour la première fois, le fichier sera créé.",
            fg=typer.colors.RED,
            blink=True,
        )
        typer.secho("Sinon, vérifiez votre fichier config.yaml.\n", fg=typer.colors.RED, blink=True)
    elif not _CONFIG.report_save_path_exists():
        typer.secho(
            "\nLe chemin de sauvegarde des rapports n'existe pas, vous ne pourrez donc pas en générer.",
            fg=typer.colors.RED,
            blink=True,
        )
        typer.secho("Vérifiez votre fichier config.yaml.\n", fg=typer.colors.RED, blink=True)


@_MAIN_TYPER_APP.callback(invoke_without_command=True)
def load_main_menu(ctx: typer.Context):
    verify_config()

    if ctx.invoked_subcommand is None:
        MainMenu()


@_TOURNAMENT_APP.callback(invoke_without_command=True)
def tournament_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        _TOURNAMENT_VIEWS.TournamentMenu()


@_TOURNAMENT_APP.command("new")
def new_tournament_menu():
    _TOURNAMENT_VIEWS.NewTournamentMenu()


@_TOURNAMENT_APP.command("load")
def load_existing_tournament_menu(tournament_id: Optional[str] = typer.Argument(None)):
    if tournament_id.isnumeric() and tournament_id is not None:
        _TOURNAMENT_VIEWS.LoadTournamentMenu(tournament_id=int(tournament_id))
    else:
        _TOURNAMENT_VIEWS.LoadTournamentMenu()


@_TOURNAMENT_APP.command("edit")
def edit_tournament_menu(tournament_id: Optional[str] = typer.Argument(None)):
    if tournament_id.isnumeric() and tournament_id is not None:
        _TOURNAMENT_VIEWS.EditTournamentMenu(tournament_id=int(tournament_id))
    else:
        _TOURNAMENT_VIEWS.EditTournamentMenu()


@_TOURNAMENT_APP.command("delete")
def delete_tournament_menu(tournament_id: Optional[str] = typer.Argument(None)):
    if tournament_id.isnumeric() and tournament_id is not None:
        _TOURNAMENT_VIEWS.DeleteTournamentMenu(tournament_id=int(tournament_id))
    else:
        _TOURNAMENT_VIEWS.DeleteTournamentMenu()


@_PLAYER_APP.callback(invoke_without_command=True)
def load_player_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        _PLAYER_VIEWS.PlayerMenu()


@_PLAYER_APP.command("new")
def new_player_menu():
    _PLAYER_VIEWS.NewPlayerMenu()


@_PLAYER_APP.command("edit")
def edit_player_menu():
    _PLAYER_VIEWS.EditPlayerMenu()


@_PLAYER_APP.command("delete")
def delete_player_menu():
    _PLAYER_VIEWSDeletePlayerMenu()


@_REPORT_APP.callback(invoke_without_command=True)
def load_report_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        _REPORT_VIEWS.ReportMenu()