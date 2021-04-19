## :material-console: Démarrer le programme

<div class="termy">

``` console
$ python3 -m oc_chess_club

- MENU PRINCIPAL -
1. Tournois
2. Gérer les joueurs
3. Générer un rapport

0. Quitter

Entrez votre sélection: :

// Vous pouvez également simplement utiliser 'oc_chess_club' si vous avez installé via pip.

// Maintenant utilisez l'argument --help

$ oc_chess_club --help

  Gestion des tournois et joueurs pour club d'échecs.

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  config      Modifier la configuration
  player      Affiche le menu des joueurs
  report      Affiche le menu des rapports
  tournament  Affiche le menu des tournois

// Vous pouvez utiliser l'argument --help pour chaque commande.

// Vous pouvez par exemple essayer oc_chess_club player --help
```

</div>

## :material-tools: Vérifier la configuration

Le programme a besoin de deux paramètres:

* Un fichier `.json` qui sera la base de données.
* Un chemin où sauvegarder les rapports générés.

Pour configurer le programme, tapez:

<div class="termy">

``` console
$ python3 -m oc_chess_club config

Souhaitez vous modifier la configuration actuelle ? [y/N]:

$ y

Base de données actuelle: /home/pablo/oc_chess_club/bdd.json
Modifier ? [y/N]:

$ n

Emplacement de sauvegarde des rapports actuel: /tmp/
Modifier ? [y/N]:

$ y

Entrez un nouvel emplacement:

$ /home/pablo/mes_rapports/

> La configuration ne comporte aucune erreur.
```

</div>

## :material-contain: Installer l'autocomplétion

L'utilisation de `typer` permet l'autocomplétion des commandes.

Pour l'installer tapez `python3 -m oc_chess_club --install-completion`

Si vous avez installé le programme via `pip` , la dépendance `shellingham` a été installée et la commande ci-dessus fonctionnera.

Dans le cas contraire vous devez préciser votre shell. Les choix possibles sont bash, zsh, fish, powershell et pwsh.  
Tapez donc par exemple `python3 -m oc_chess_club --install-completion bash` .

## :material-gamepad: [Jouer](game.md)

## :material-chess-king: [Gérer les tournois](tournaments.md)

## :material-human-edit: [Gérer les joueurs](players.md)

## :material-file: [Générer un rapport](reports.md)
