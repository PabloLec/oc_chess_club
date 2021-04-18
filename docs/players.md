!!! astuce

    Pour accèder directement au menu des joueurs entrez `oc_chess_club player` .

### Créer un joueur

<div class="termy">

``` console
$ python3 -m oc_chess_club player new

- CRÉATION D'UN JOUEUR -
- Entrez les informations du joueur

Prénom du joueur:

$ Jake

Nom de famille du joueur:

$ Mate

Date de naissance (JJ/MM/AAAA):

$ 16/07/1993

Genre (H/F):

$ H

ELO:

$ 750

- Informations du joueur:

Prénom: Jake
Nom de famille: Mate
Date de naissance: 16/07/1993
Genre: H
ELO: 750

Souhaitez vous confirmer la création de ce joueur ? [y/N]:

$ y

> Le joueur a été créé avec le numéro 9.
```

</div>

### Editer un joueur

<div class="termy">

``` console
$ python3 -m oc_chess_club player edit

- MODIFICATION D'UN JOUEUR -
- Liste des joueurs existants:
1. Bill Gates
2. Linus Torvalds
3. Steve Jobs
4. Ken Thompson
5. Dennis Ritchie
6. Guido van Rossum
7. Robert Martin
8. Tim Berners-Lee
9. Jake Mate

Sélectionnez un joueur:

$ 9

- Informations actuelles du joueur:

Prénom: Jake
Modifier cette information? [y/N]:

$ n

Nom de famille: Mate
Modifier cette information? [y/N]:

$ n

Date de naissance: 16/07/1993
Modifier cette information? [y/N]:

$ n

Genre: H
Modifier cette information? [y/N]:

$ n

ELO: 750
Modifier cette information? [y/N]:

$ y

Entrez une nouvelle valeur pour 'ELO':

$ 800

- Nouvelles informations du joueur:

Prénom: Jake
Nom de famille: Mate
Date de naissance: 16/07/1993
Genre: H
ELO: 800

Souhaitez vous confirmer la modification de ce joueur ? [y/N]:

$ y

> Le joueur n°9 a été modifié.

```

</div>

### Supprimer un joueur

<div class="termy">

``` console
$ python3 -m oc_chess_club player delete

- SUPPRESSION D'UN JOUEUR -
- Liste des joueurs existants:
1. Bill Gates
2. Linus Torvalds
3. Steve Jobs
4. Ken Thompson
5. Dennis Ritchie
6. Guido van Rossum
7. Robert Martin
8. Tim Berners-Lee
9. Jake Mate

Sélectionnez un joueur:

$ 9

VOUS ALLEZ SUPPRIMER DÉFINITIVEMENT 'JAKE MATE'

Confirmer la suppression ? [y/N]:

$ y

```

</div>
