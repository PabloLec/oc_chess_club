import typer


print(typer.colors.__dir__())


def print_line(pawn: str, title: str):
    pawn_part = typer.style(pawn, fg=typer.colors.BRIGHT_WHITE, bold=True)
    title_part = typer.style(title, fg=typer.colors.BRIGHT_MAGENTA)

    typer.echo(pawn_part + title_part)


def print_welcome_splash():
    welcome_splash_lines = [
        ["    __", ""],
        ["   /  \\", "                      _                         _       _"],
        ["   \\__/", "                     | |                       | |     | |"],
        ["  /____\\", "     ___   ___   ___| |__   ___  ___ ___   ___| |_   _| |__"],
        ["   |  |", "     / _ \\ / __| / __| '_ \\ / _ \\/ __/ __| / __| | | | | '_ \\"],
        ["   |__|", "    | (_) | (__ | (__| | | |  __/\\__ \\__ \\| (__| | |_| | |_) |"],
        ["  (====)", "    \\___/ \\___| \\___|_| |_|\\___||___/___/ \\___|_|\\__,_|_.__/"],
        ["  }===={", "            ______                    ______ "],
        [" (______)", "          |______|                  |______|"],
    ]

    for line in welcome_splash_lines:
        pawn_part = typer.style(part[0], fg=typer.colors.BRIGHT_WHITE, bold=True)
        title_part = typer.style(part[1], fg=typer.colors.BRIGHT_MAGENTA)

        typer.echo(pawn_part + title_part)

    typer.echo("\n")


test_menu_title = typer.secho(
    "- MENU DE TOURNOIS -", fg=typer.colors.BRIGHT_CYAN, bg=typer.colors.BRIGHT_BLACK, bold=True
)
test_error = typer.secho("Pas de tournoi créé.", fg=typer.colors.BRIGHT_RED, bg=typer.colors.BRIGHT_BLACK, bold=True)
test_success = typer.secho(
    "Le rapport a été généré.", fg=typer.colors.BRIGHT_GREEN, bg=typer.colors.BRIGHT_BLACK, bold=True
)
test_info = typer.secho("Sélection d'un truc", fg=typer.colors.BRIGHT_MAGENTA, bg=typer.colors.BRIGHT_BLACK, bold=True)
