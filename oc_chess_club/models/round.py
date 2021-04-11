from oc_chess_club.models.match import Match


class Round:
    """Model for round. All rounds have matches associated with them and are associated with a tournament.

    Attributes:
        round_number (int): Ordered round number within the tournament.
        tournament_id (int): Unique id of the parent tournament.
        id_num (int): Unique id of this round.
        matches (dict): All matches associated with this round.
    """

    def __init__(self, round_number: int, tournament_id: int, id_num: int):
        """Constructor for Round.

        Args:
            round_number (int): Ordered round number within the tournament.
            tournament_id (int): Unique id of the parent tournament.
            id_num (int): Unique id of this round.
        """

        self.round_number = round_number
        self.tournament_id = tournament_id
        self.id_num = id_num

        self.matches = {}

    def __str__(self):
        stdout_content = "   - Round Number: {num}\n".format(num=self.round_number)

        stdout_content += "   - Matches -\n"

        for started_match in self.matches:
            stdout_content += started_match.__str__()

        return stdout_content