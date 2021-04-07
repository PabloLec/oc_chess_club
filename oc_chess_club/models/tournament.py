from oc_chess_club.models.round import Round
from oc_chess_club.models.player import Player


class Tournament:
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
    ):

        self.name = name
        self.location = location
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.time_control = time_control
        self.description = description
        self.id_num = id_num
        self.is_finished = is_finished

        self.rounds = []
        self.players = []

    def __str__(self):
        stdout_content = " - Tournament name: {name}\n".format(name=self.name)
        stdout_content += "   - Is finished ?: {is_finished}\n".format(is_finished=self.is_finished)
        stdout_content += "   - Location: {location}\n".format(location=self.location)
        stdout_content += "   - Date: {date}\n".format(date=self.date)
        stdout_content += "   - Number of rounds: {num}\n".format(num=self.number_of_rounds)
        stdout_content += "   - Time Control: {time}\n".format(time=self.time_control)
        stdout_content += "   - Description: {description}\n".format(description=self.description)

        stdout_content += " - - Started rounds - -\n"

        for started_round in self.rounds:
            stdout_content += started_round.__str__()

        return stdout_content

    def add_player(self, player: Player):

        self.players.append(player)

    def is_tournament_full(self):

        if self.players >= 8:
            return True
        else:
            return False

    def add_round(self, round_object: Round):
        self.rounds.append(round_object)