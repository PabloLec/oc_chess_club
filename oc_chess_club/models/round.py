from oc_chess_club.models.match import Match


class Round:
    def __init__(self, round_number: int, tournament_id: int, id_num: int):
        self.matches = {}
        self.id_num = id_num
        self.tournament_id = tournament_id

        self.round_number = round_number

    def __str__(self):
        stdout_content = "   - Round Number: {num}\n".format(num=self.round_number)

        stdout_content += "   - Matches -\n"

        for started_match in self.matches:
            stdout_content += started_match.__str__()

        return stdout_content

    def add_match(self, match: Match):
        self.matches.append(match)