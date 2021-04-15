## :material-chess-knight: Principe

Ce programme a pour but de gérer les tournois et joueurs d'un club d'échecs.

* Le programme est utilisé en ligne de commande.
* Une base de données légère permet de stocker les informations des joueurs et des tournois.
* Les tournois peuvent être arrêtés et repris à n'importe quel moment.
* Divers rapports peuvent être générés et exportés.

## :material-order-bool-descending-variant: Prérequis

L'installation via pip installera pour vous les dépendances situées dans `requirements.txt` .

Les deux dépendances principales sont `tinydb` pour la gestion de la base de données au format JSON et `typer` pour la gestion de la partie CLI de l'application.  
Ce dernier, basé sur `click` va permettre un fonctionnement cross-OS. Votre système d'exploitation et votre terminal ne devraient pas poser de problème de compatibilité.

:warning: **Votre version de Python doit être >= 3.9**.  
Notamment du fait de l'utilisation native de type hints de génériques sans passer par la librairie `typing` . Fonctionnalité introduite dans le [PEP 585](https://www.python.org/dev/peps/pep-0585/).

## :material-folder-settings: Installation

<div class="termy">

``` console

$ python3 _m pip install oc_chess_club

```

</div>

## :material-rocket-launch: Utilisation

Rendez-vous dans le [tutoriel](start.md) pour apprendre à utiliser le programme.
