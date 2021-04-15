!!! astuce

    Pour accèder directement au menu des tournois entrez `oc_chess_club tournament` .

### Créer un tournoi

<div class="termy">

``` console
$ python3 -m oc_chess_club tournament new

- CRÉATION D'UN TOURNOI -
- Entrez les informations du tournoi.

Nom du tournoi:

$ Tournoi du siècle

Lieu:

$ Batcave

Date (JJ/MM/AAAA):

$ 01/01/1970

Nombre de round:

$ 4

Contrôle du temps:

$ blitz

Description:

$ Le grand tournoi des champions

Entrez le numéro d'un joueur à ajouter

- Liste des joueurs existants:
1. Bill Gates
2. Linus Torvalds
3. Steve Jobs
4. Ken Thompson
5. Dennis Ritchie
6. Guido van Rossum
7. Robert Martin
8. Tim Berners-Lee

Joueur (0/8):

$ 1

Joueur (1/8):

$ 2

Joueur (2/8):

$ 3

Joueur (3/8):

$ 4

Joueur (4/8):

$ 5

Joueur (5/8):

$ 6

Joueur (6/8):

$ 7

Joueur (7/8):

$ 8

- Paramètres du tournoi:

Nom: Tournoi du siècle
Lieu: Batcave
Date: 01/01/1970
Nombre de rounds: 4
Contrôle du temps: Blitz
Description: Le grand tournoi des champions

- Liste des joueurs:

 - Bill Gates
 - Linus Torvalds
 - Steve Jobs
 - Ken Thompson
 - Dennis Ritchie
 - Guido van Rossum
 - Robert Martin
 - Tim Berners-Lee

Souhaitez vous confirmer la création de ce tournoi ? [y/N]:

$ y

> Le tournoi a été créé.
```

</div>

### Editer un tournoi

<div class="termy">

``` console
$ python3 -m oc_chess_club tournament edit

- MODIFICATION D'UN TOURNOI -
- Liste des tournois existants:
1. Le tournoi du siècle - 01/01/1970

Sélectionnez un tournoi:

$ 1

- Informations actuelles du tournoi:

Nom: Le tournoi du siècle
Modifier cette information? [y/N]:

$ y

Entrez une nouvelle valeur pour 'Nom':

$ Tournoi du jour

Lieu: Batcave
Modifier cette information? [y/N]:

$ n

Date: 01/01/1970
Modifier cette information? [y/N]:

$ n

Description: Le grand tournoi des champion
Modifier cette information? [y/N]:

$ y

Entrez une nouvelle valeur pour 'Description':

$ Le petit tournoi des champions

- Nouvelles informations du tournoi:

Nom: Tournoi du jour
Lieu: Batcave
Date: 01/01/1970
Description: Le petit tournoi des champions

Souhaitez vous confirmer la modification de ce tournoi ? [y/N]:

$ y

> Le tournoi n°1 a été modifié.

```

</div>

### Supprimer un tournoi

<div class="termy">

``` console
$ python3 -m oc_chess_club tournament delete

- SUPPRESSION D'UN TOURNOI -
- Liste des tournois existants:
1. Tournoi du jour - 01/01/1970

Sélectionnez un tournoi:

$ 1

VOUS ALLEZ SUPPRIMER DÉFINITIVEMENT LE TOURNOI 'TOURNOI DU JOUR'

Confirmer la suppression ? [y/N]:

$ y

```

</div>
