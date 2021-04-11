from oc_chess_club.models.round import Round
from oc_chess_club.models.player import Player


class Tournament:
    """Model for tournament. All tournaments have rounds associated with them, these rounds have matches associated with them.

    Attributes:
        name (str): Tournament's name.
        location (str): Tournament's physical location.
        date (str): Tournament's date.
        number_of_rounds (int): Number of rounds to be played.
        time_control (str): Type of time control chosen.
        description (str): Tournament's description.
        id_num (int): Tournament's unique id.
        is_finished (bool): Is the tournament finished ?
        players (list[Player]): List of participating players.
        leaderboard (dict): Tournament's leaderboard.
        rounds (dict): All rounds associated with this tournament.
    """

    def __init__(
        self,
        name: str,
        location: str,
        date: str,
        number_of_rounds: int,
        time_control: str,
        description: str,
        id_num: int,
        is_finished: bool,
        players: list,
        leaderboard: dict,
    ):
        """Constructor for Tournament.

        Args:
            name (str): Tournament's name.
            location (str): Tournament's physical location.
            date (str): Tournament's date.
            number_of_rounds (int): Number of rounds to be played.
            time_control (str): Type of time control chosen.
            description (str): Tournament's description.
            id_num (int): Tournament's unique id.
            is_finished (bool): Is the tournament finished ?
            players (list[Player]): List of participating players.
            leaderboard (dict): Tournament's leaderboard.
        """

        self.name = name
        self.location = location
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.time_control = time_control
        self.description = description
        self.id_num = id_num
        self.is_finished = is_finished
        self.players = players
        self.leaderboard = leaderboard

        self.rounds = {}

    def __str__(self):
        stdout_content = " - Tournament name: {name}\n".format(name=self.name)
        stdout_content += "   - Is finished ?: {is_finished}\n".format(is_finished=self.is_finished)
        stdout_content += "   - Location: {location}\n".format(location=self.location)
        stdout_content += "   - Date: {date}\n".format(date=self.date)
        stdout_content += "   - Number of rounds: {num}\n".format(num=self.number_of_rounds)
        stdout_content += "   - Time Control: {time}\n".format(time=self.time_control)
        stdout_content += "   - Description: {description}\n".format(description=self.description)
        stdout_content += "   - Players: {players}\n".format(players=self.players)
        stdout_content += "   - Leaderboard: {leaderboard}\n".format(leaderboard=self.leaderboard)

        stdout_content += " - - Started rounds - -\n"

        for started_round in self.rounds:
            stdout_content += started_round.__str__()

        return stdout_content