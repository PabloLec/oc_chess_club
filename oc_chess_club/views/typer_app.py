import typer

from oc_chess_club.views.main_menu import MainMenu
from oc_chess_club.views.tournament_menu import TournamentMenu
from oc_chess_club.views.new_tournament import NewTournamentMenu

_MAIN_TYPER_APP = typer.Typer()
_TOURNAMENT_APP = typer.Typer()

_MAIN_TYPER_APP.add_typer(_TOURNAMENT_APP, name="tournament")


@_MAIN_TYPER_APP.callback(invoke_without_command=True)
def load_main_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        MainMenu()


@_TOURNAMENT_APP.callback(invoke_without_command=True)
def load_tournament_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        TournamentMenu()


@_TOURNAMENT_APP.command("new")
def load_new_tournament_menu():
    NewTournamentMenu()