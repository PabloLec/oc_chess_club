from typing import Optional

import typer

from oc_chess_club.controller.config_loader import _CONFIG
from oc_chess_club.views.main_menu import MainMenu
import oc_chess_club.views.tournament_views as _TOURNAMENT_VIEWS
import oc_chess_club.views.player_views as _PLAYER_VIEWS
import oc_chess_club.views.report_views as _REPORT_VIEWS
import oc_chess_club.views.helper as _HELPER

_MAIN_TYPER_APP = typer.Typer(help="Gestion des tournois et joueurs pour club d'échecs.")
_TOURNAMENT_APP = typer.Typer(help="Affiche le menu des tournois")
_PLAYER_APP = typer.Typer(help="Affiche le menu des joueurs")
_REPORT_APP = typer.Typer(help="Affiche le menu des rapports")

_MAIN_TYPER_APP.add_typer(_TOURNAMENT_APP, name="tournament")
_MAIN_TYPER_APP.add_typer(_PLAYER_APP, name="player")
_MAIN_TYPER_APP.add_typer(_REPORT_APP, name="report")


def verify_config():
    if not _CONFIG.database_path_exists():
        _HELPER.print_warning(
            message="Le chemin de sauvegarde pour la base de données n'est pas valide."
            " Vérifiez votre fichier config.yaml."
        )
        _HELPER.prompt_config_modification()
    elif not _CONFIG.database_exists():
        _HELPER.print_warning(
            message="Le fichier pour la base de données n'existe pas.\n"
            "Si vous utilisez le programme pour la première fois, le fichier sera créé.\n"
            "Sinon, vérifiez votre fichier config.yaml."
        )
        _HELPER.prompt_config_modification()
    elif not _CONFIG.report_save_path_exists():
        _HELPER.print_warning(
            message="Le chemin de sauvegarde des rapports n'existe pas, vous ne pourrez donc pas en générer."
            " Vérifiez votre fichier config.yaml."
        )
        _HELPER.prompt_config_modification()


@_MAIN_TYPER_APP.callback(invoke_without_command=True)
def load_main_menu(ctx: typer.Context):
    verify_config()

    if ctx.invoked_subcommand is None:
        _HELPER.print_welcome_splash()
        MainMenu()


@_MAIN_TYPER_APP.command("config", help="Modifier la configuration")
def load_config_menu():
    _HELPER.prompt_config_modification()


@_TOURNAMENT_APP.callback(invoke_without_command=True)
def tournament_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        _TOURNAMENT_VIEWS.TournamentMenu()


@_TOURNAMENT_APP.command("new", help="Créer un nouveau tournoi")
def new_tournament_menu():
    _TOURNAMENT_VIEWS.NewTournamentMenu()


@_TOURNAMENT_APP.command("load", help="Charger un tournoi existant")
def load_existing_tournament_menu(
    tournament_id: Optional[str] = typer.Argument(None, help="id du tournoi à charger", metavar="id")
):
    if tournament_id is not None and tournament_id.isnumeric():
        _TOURNAMENT_VIEWS.LoadTournamentMenu(tournament_id=int(tournament_id))
    else:
        _TOURNAMENT_VIEWS.LoadTournamentMenu()


@_TOURNAMENT_APP.command("edit", help="Modifier un tournoi existant")
def edit_tournament_menu(
    tournament_id: Optional[str] = typer.Argument(None, help="id du tournoi à charger", metavar="id")
):
    if tournament_id is not None and tournament_id.isnumeric():
        _TOURNAMENT_VIEWS.EditTournamentMenu(tournament_id=int(tournament_id))
    else:
        _TOURNAMENT_VIEWS.EditTournamentMenu()


@_TOURNAMENT_APP.command("delete", help="Supprimer un tournoi existant")
def delete_tournament_menu(
    tournament_id: Optional[str] = typer.Argument(None, help="id du tournoi à charger", metavar="id")
):
    if tournament_id is not None and tournament_id.isnumeric():
        _TOURNAMENT_VIEWS.DeleteTournamentMenu(tournament_id=int(tournament_id))
    else:
        _TOURNAMENT_VIEWS.DeleteTournamentMenu()


@_PLAYER_APP.callback(invoke_without_command=True)
def load_player_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        _PLAYER_VIEWS.PlayerMenu()


@_PLAYER_APP.command("new", help="Créer un nouveau joueur")
def new_player_menu():
    _PLAYER_VIEWS.NewPlayerMenu()


@_PLAYER_APP.command("edit", help="Modifier un joueur existant")
def edit_player_menu(player_id: Optional[str] = typer.Argument(None, help="id du joueur à charger", metavar="id")):
    if player_id is not None and player_id.isnumeric():
        _PLAYER_VIEWS.EditPlayerMenu(player_id=int(player_id))
    else:
        _PLAYER_VIEWS.EditPlayerMenu()


@_PLAYER_APP.command("delete", help="Modifier un joueur existant")
def delete_player_menu(player_id: Optional[str] = typer.Argument(None, help="id du joueur à charger", metavar="id")):
    if player_id is not None and player_id.isnumeric():
        _PLAYER_VIEWS.DeletePlayerMenu(player_id=int(player_id))
    else:
        _PLAYER_VIEWS.DeletePlayerMenu()


@_REPORT_APP.callback(invoke_without_command=True)
def load_report_menu(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        _REPORT_VIEWS.ReportMenu()