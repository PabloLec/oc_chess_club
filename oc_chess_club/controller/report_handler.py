import csv

from datetime import datetime
from pathlib import Path

from oc_chess_club.controller.config_loader import _CONFIG
from oc_chess_club.controller.database_handler import DatabaseHandler
from oc_chess_club.models.tournament import Tournament


class ReportHandler:
    """Handles report's data generation and local saving.

    Attributes:
        data (list): List of serialized data for the report.
        export_location (str): Local path for report saving.
    """

    def __init__(self):
        """Constructor for ReportHandler."""

        self.data = []
        self.export_location = _CONFIG.config["report_save_path"]

    def all_players_by_name(self):
        """Extracts data for all players ordered by name."""

        players_list = DatabaseHandler().helper.get_players_by_name()

        for player in players_list:
            self.data.append(
                {
                    "Nom": player.last_name,
                    "Prénom": player.first_name,
                    "Date de naissance": player.dob,
                    "Genre": player.gender,
                    "ELO": player.elo,
                    "id": player.id_num,
                }
            )

    def all_players_by_elo(self):
        """Extracts data for all players ordered by ELO ranking."""

        players_list = DatabaseHandler().helper.get_players_by_elo()

        for player in players_list:
            self.data.append(
                {
                    "ELO": player.elo,
                    "Nom": player.last_name,
                    "Prénom": player.first_name,
                    "Date de naissance": player.dob,
                    "Genre": player.gender,
                    "id": player.id_num,
                }
            )

    def tournament_players_by_name(self, tournament: Tournament):
        """Extracts data for all players of a tournament ordered by name.

        Args:
            tournament (Tournament): Tournament to be considered.
        """

        players_dict = {}
        for player in tournament.players:
            players_dict[player.id_num] = player

        players_list = DatabaseHandler().helper.get_players_by_name(players_sample=players_dict)

        for player in players_list:
            self.data.append(
                {
                    "Nom": player.last_name,
                    "Prénom": player.first_name,
                    "Date de naissance": player.dob,
                    "Genre": player.gender,
                    "ELO": player.elo,
                    "id": player.id_num,
                }
            )

    def tournament_players_by_elo(self, tournament: Tournament):
        """Extracts data for all players of a tournament ordered by ELO ranking.

        Args:
            tournament (Tournament): Tournament to be considered.
        """

        players_dict = {}
        for player in tournament.players:
            players_dict[player.id_num] = player

        players_list = DatabaseHandler().helper.get_players_by_elo(players_sample=players_dict)

        for player in players_list:
            self.data.append(
                {
                    "ELO": player.elo,
                    "Nom": player.last_name,
                    "Prénom": player.first_name,
                    "Date de naissance": player.dob,
                    "Genre": player.gender,
                    "id": player.id_num,
                }
            )

    def all_tournaments(self):
        """Extracts data for all tournaments."""

        tournaments_list = DatabaseHandler().helper.get_tournaments_by_id()

        for tournament in tournaments_list:
            players_ids = [x.id_num for x in tournament.players]
            list_of_players_name = DatabaseHandler().helper.get_players_names(players_sample=players_ids)

            if tournament.is_finished:
                is_finished = "Terminé"
            else:
                is_finished = "En cours"

            self.data.append(
                {
                    "id": tournament.id_num,
                    "Nom": tournament.name,
                    "Lieu": tournament.location,
                    "Date": tournament.date,
                    "Nombre de rounds": tournament.number_of_rounds,
                    "Contrôle de temps": tournament.time_control,
                    "Description": tournament.description,
                    "Progression": is_finished,
                    "Joueurs": list_of_players_name,
                    "Classement": DatabaseHandler().helper.get_formated_leaderboard(
                        leaderboard=tournament.leaderboard
                    ),
                }
            )

    def tournament_rounds(self, tournament: Tournament):
        """Extracts data for all rounds of a tournament.

        Args:
            tournament (Tournament): Tournament to be considered.
        """

        self.load_tournament_data(tournament_id=tournament.id_num)

        for round_ in tournament.rounds:
            matches = []

            for match in tournament.rounds[round_].matches:
                match = tournament.rounds[round_].matches[match]
                player_1 = DatabaseHandler().helper.get_player_name_from_id(match.player_1.id_num)
                player_2 = DatabaseHandler().helper.get_player_name_from_id(match.player_2.id_num)
                matches.append(f"{player_1} vs {player_2}")

            self.data.append(
                {
                    "Round n°": tournament.rounds[round_].round_number,
                    "Matchs": matches,
                    "id": tournament.rounds[round_].id_num,
                }
            )

    def tournament_matches(self, tournament: Tournament):
        """Extracts data for all matches of a tournament.

        Args:
            tournament (Tournament): Tournament to be considered.
        """

        self.load_tournament_data(tournament_id=tournament.id_num)

        for round_ in tournament.rounds:
            matches = tournament.rounds[round_].matches
            for match in matches:
                match = matches[match]
                player_1 = f"{match.player_1.first_name} {match.player_1.last_name}"
                player_2 = f"{match.player_2.first_name} {match.player_2.last_name}"

                if match.winner is None:
                    winner = "Pas encore joué"
                elif match.winner == 0:
                    winner = "Match nul"
                elif match.winner == 1:
                    winner = player_1
                elif match.winner == 2:
                    winner = player_2

                self.data.append({"id": match.id_num, "Joueur 1": player_1, "Joueur 2": player_2, "Vainqueur": winner})

    def load_tournament_data(self, tournament_id: int):
        """Uses database handler to load a tournament rounds and matches.

        Args:
            tournament_id (int): Unique id of tournament to be loaded.
        """

        DatabaseHandler().load_rounds(tournament_id=tournament_id)
        DatabaseHandler().load_matches(tournament_id=tournament_id)

    def init_export(self, file_format: str):
        """Initiates export process and set full local path.

        Args:
            file_format (str): Desired export file format.

        Returns:
            str: Local path of saved file.
        """

        time = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        file_name = f"oc_chess_club-rapport-{time}.{file_format}"

        save_path = Path(self.export_location).joinpath(file_name)

        if file_format == "txt":
            self.export_txt(save_path=save_path)
        elif file_format == "csv":
            self.export_csv(save_path=save_path)

        return str(save_path)

    def export_txt(self, save_path: Path):
        """Exports data to text format.

        Args:
            save_path (Path): Local path for file.
        """

        with open(save_path, "w") as output_file:
            for element in self.data:
                for key in element:
                    output_file.write(f"{key}: {element[key]}\n")
                output_file.write("\n")

    def export_csv(self, save_path: Path):
        """Exports data to csv format.

        Args:
            save_path (Path): Local path for file.
        """

        with open(save_path, "w") as output_file:
            field_names = list(self.data[0].keys())
            writer = csv.DictWriter(output_file, fieldnames=field_names)
            writer.writeheader()

            for element in self.data:
                writer.writerow(element)