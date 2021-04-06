from oc_chess_club.models.match import Match


class Round:
    def __init__(self, round_number: int):
        self.matches = []
        self.round_number = round_number

    def add_match(self, match: Match):
        self.matches.append(match)