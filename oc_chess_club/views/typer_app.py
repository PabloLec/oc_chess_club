import typer

from oc_chess_club.views.main_menu import MainMenu
from oc_chess_club.views.tournament_menu import TournamentMenu
from oc_chess_club.views.new_tournament import NewTournamentMenu
from oc_chess_club.views.load_tournament import LoadTournamentMenu
from oc_chess_club.views.player_menu import PlayerMenu
from oc_chess_club.views.new_player import NewPlayerMenu
from oc_chess_club.views.edit_player import EditPlayerMenu

_MAIN_TYPER_APP = typer.Typer()
_TOURNAMENT_APP = typer.Typer()
_PLAYER_APP = typer.Typer()

_MAIN_TYPER_APP.add_typer(_TOURNAMENT_APP, name="tournament")
_MAIN_TYPER_APP.add_typer(_PLAYER_APP, name="player")


@_MAIN_TYPER_APP.callback(invoke_without_command=True)
def load_main_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        MainMenu()


@_TOURNAMENT_APP.callback(invoke_without_command=True)
def load_tournament_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        TournamentMenu()


@_TOURNAMENT_APP.command("new")
def new_tournament_menu():
    NewTournamentMenu()


@_TOURNAMENT_APP.command("load")
def load_existing_tournament_menu():
    LoadTournamentMenu()


@_PLAYER_APP.callback(invoke_without_command=True)
def load_player_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        PlayerMenu()


@_PLAYER_APP.command("new")
def new_player_menu():
    NewPlayerMenu()


@_PLAYER_APP.command("edit")
def edit_player_menu():
    EditPlayerMenu()