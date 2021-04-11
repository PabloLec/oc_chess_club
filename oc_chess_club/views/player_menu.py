import typer

from oc_chess_club.views.new_player import NewPlayerMenu
from oc_chess_club.views.edit_player import EditPlayerMenu
from oc_chess_club.views.delete_player import DeletePlayerMenu


class PlayerMenu:
    """View for player related operations."""

    def __init__(self):
        """Constructor for PlayerMenu."""

        self.print_menu()
        self.user_selection()

    def print_menu(self):
        """Displays the different menu options."""

        number = typer.style("1. ", bold=True)
        typer.echo(number + "Créer un nouveau joueur")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Modifier un joueur")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Supprimer un joueur")

        number = typer.style("2. ", bold=True)
        typer.echo(number + "Afficher tous les joueurs")

    def user_selection(self):
        """Prompts the user to select an option."""

        selection = typer.prompt("Entrez votre sélection: ")

        if selection == "1":
            self.create_new_player()
        elif selection == "2":
            self.edit_player()
        elif selection == "3":
            self.delete_player()
        else:
            self.user_selection()

    def create_new_player(self):
        """Opens the player creation menu."""

        NewPlayerMenu()

    def edit_player(self):
        """Opens the player editing menu."""

        EditPlayerMenu()

    def delete_player(self):
        """Opens the player deletion menu."""

        DeletePlayerMenu()