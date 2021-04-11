class Match:
    """Model for match. All matches are associated with a round which is also associated with a tournament.

    Attributes:
        tournament_id (int): Unique id of the parent tournament.
        round_id (int): Unique id of the parent round.
        winner (int): Winner of the match. 1 for Player 1, 2 for Player 2, 0 for a draw and None if TBD.
        id_num (int):  Unique id of this match.
        player_1 (Player): Arbitrary first player.
        player_2 (Player): Arbitrary second player.
    """

    def __init__(self, players: tuple, tournament_id: int, round_id: int, winner: int, id_num: int):
        """Constructor for Match.

        Args:
            players (tuple[Player]): The two participating players.
            tournament_id (int):  Unique id of the parent tournament.
            round_id (int): Unique id of the parent round.
            winner (int): Winner of the match. 1 for Player 1, 2 for Player 2, 0 for a draw and None if TBD.
            id_num (int): Unique id of this match.
        """

        self.tournament_id = tournament_id
        self.round_id = round_id
        self.winner = winner
        self.id_num = id_num

        self.player_1 = players[0]
        self.player_2 = players[1]

    def __str__(self):
        stdout_content = "    - {f_name_1} {l_name_1} ({elo_1}) vs {f_name_2} {l_name_2} ({elo_2})\n".format(
            f_name_1=self.player_1.first_name,
            l_name_1=self.player_1.last_name,
            elo_1=self.player_1.elo,
            f_name_2=self.player_2.first_name,
            l_name_2=self.player_2.last_name,
            elo_2=self.player_2.elo,
        )
        stdout_content += "    Winner : {winner}\n".format(winner=self.winner)
        stdout_content += "    id : {id}\n".format(id=self.id_num)

        return stdout_content