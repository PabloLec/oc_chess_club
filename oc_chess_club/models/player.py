class Player:
    """Model for player.

    Attributes:
        first_name (str): Players's first name.
        last_name (str): Player's last name.
        dob (str): Player's date of birth.
        gender (str): Player's gender.
        elo (str): Player's ELO ranking.
        id_num (int): Player's unique id number.
    """

    def __init__(self, first_name: str, last_name: str, dob: str, gender: str, elo: str, id_num: int):
        """[summary]

        Args:
            first_name (str): Players's first name.
            last_name (str): Player's last name.
            dob (str): Player's date of birth.
            gender (str): Player's gender.
            elo (str): Player's ELO ranking.
            id_num (int): Player's unique id number.
        """

        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.elo = elo
        self.id_num = id_num

    def __str__(self):
        stdout_content = " - Player ID: {id}\n".format(id=self.id_num)
        stdout_content += "   - First Name: {first_name}\n".format(first_name=self.first_name)
        stdout_content += "   - Last Name: {last_name}\n".format(last_name=self.last_name)
        stdout_content += "   - DOB: {dob}\n".format(dob=self.dob)
        stdout_content += "   - Gender: {gender}\n".format(gender=self.gender)
        stdout_content += "   - ELO: {elo}\n".format(elo=self.elo)

        return stdout_content