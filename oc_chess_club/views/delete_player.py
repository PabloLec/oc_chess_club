import typer

from oc_chess_club.controller.database_handler import _DATABASE_HANDLER
import oc_chess_club.views.helper as _HELPER


class DeletePlayerMenu:
    """View for player deletion

    Attributes:
        selected_player (Player): Player selected by user for deletion.
    """

    def __init__(self):
        """Constructor DeletePlayerMenu."""

        self.selected_player = None

        self.selected_player = _HELPER.select_player()
        self.confirm_selection()

    def confirm_selection(self):
        """Prompts the user to confrim user deletion."""

        typer.secho(
            "\nVous allez supprimer définitivement {first_name} {last_name}".format(
                first_name=self.selected_player.first_name, last_name=self.selected_player.last_name
            ),
            fg=typer.colors.RED,
        )

        confirm = typer.confirm("Confirmer la suppression ?")

        if confirm:
            self.delete_player()
        else:
            typer.secho("\n L'utilisateur n'a pas été supprimé", fg=typer.colors.GREEN)

    def delete_player(self):
        """Uses database handler to delete player."""

        pass