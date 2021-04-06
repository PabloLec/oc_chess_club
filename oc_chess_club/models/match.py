class Match:
    def __init__(self, players: tuple):
        self.winner = None
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

        return stdout_content