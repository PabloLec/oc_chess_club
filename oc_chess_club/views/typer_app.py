import typer

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


@_MAIN_TYPER_APP.callback(invoke_without_command=True)
def load_main_menu(ctx: typer.Context):
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
def load_existing_tournament_menu():
    _TOURNAMENT_VIEWS.LoadTournamentMenu()


@_TOURNAMENT_APP.command("edit")
def edit_tournament_menu():
    _TOURNAMENT_VIEWS.EditTournamentMenu()


@_TOURNAMENT_APP.command("delete")
def delete_tournament_menu():
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