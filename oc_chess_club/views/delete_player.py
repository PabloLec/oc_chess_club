import typer

import oc_chess_club.views.helper as _HELPER


class DeletePlayerMenu:
    def __init__(self):
        self.selected_player = None

        self.selected_player = _HELPER.select_player()
