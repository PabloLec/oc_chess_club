import typer

from oc_chess_club.controller.tournament_handler import TournamentHandler
from oc_chess_club.models.match import Match


class GameMenu:
    def __init__(self, tournament_id: int):
        self.tournament_handler = TournamentHandler(tournament_id=tournament_id)
        self.play()

    def play(self):
        while self.tournament_handler.match_generator() is not None:
            self.display_next_match(self.tournament_handler.match_generator())

    def display_next_match(self, match: Match):
        self.display_tournament_progression()
        self.introduce_match(match=match)
        winner = self.ask_for_winner()
        self.tournament_handler.save_winner(match=match, winner=winner)

    def display_tournament_progression(self):
        self.tournament_handler.update_tournament_progression()
        decorator = typer.style(
            " - - ",
            bold=True,
        )
        separator = typer.style(
            " - ",
            bold=True,
        )

        tournament_num = typer.style(
            f"Tournoi {self.tournament_handler.tournament.id_num}",
            fg=typer.colors.BLUE,
        )
        round_num = typer.style(
            f"Round {self.tournament_handler.current_round_num}",
            fg=typer.colors.BLUE,
        )
        match_num = typer.style(
            f"Match {self.tournament_handler.current_match_num}",
            fg=typer.colors.BLUE,
        )

        typer.echo("\n" + decorator + tournament_num + separator + round_num + separator + match_num + decorator)

    def introduce_match(self, match: Match):
        player_1_title = typer.style(
            "Joueur 1: ",
            bold=True,
        )
        player_1_name = typer.style(
            "{f_name_1} {l_name_1} ".format(
                f_name_1=match.player_1.first_name,
                l_name_1=match.player_1.last_name,
            ),
            fg=typer.colors.GREEN,
        )
        player_1_elo = typer.style(
            f"({match.player_1.elo})",
            fg=typer.colors.BLUE,
        )

        player_1_full_presentation = player_1_title + player_1_name + player_1_elo

        versus = typer.style(
            " vs ",
            bold=True,
        )
        player_2_title = typer.style(
            "Joueur 2: ",
            bold=True,
        )
        player_2_name = typer.style(
            "{f_name_2} {l_name_2} ".format(
                f_name_2=match.player_2.first_name,
                l_name_2=match.player_2.last_name,
            ),
            fg=typer.colors.GREEN,
        )
        player_2_elo = typer.style(
            f"({match.player_2.elo})",
            fg=typer.colors.BLUE,
        )

        player_2_full_presentation = player_2_title + player_2_name + player_2_elo

        typer.echo(player_1_full_presentation + versus + player_2_full_presentation)

    def ask_for_winner(self):
        winner = ""
        while winner.lower() not in ["1", "2", "nul"]:
            winner = typer.prompt("Entrez le gagnant (1, 2, ou nul)")
        return winner.lower()