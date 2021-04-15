Pour commencer ou reprendre un tournoi, vous pouvez naviguer via le menu principal ou taper directement `python3 -m oc_chess_club tournament load`.

!!! astuce
    Pour charger directement un tournoi avec son id vous pouvez utiliser `python3 -m oc_chess_club tournament load [id]`.

<div class="termy">

``` console
$ python3 -m oc_chess_club tournament load 1

 - - Tournoi 1 - Round 1 - Match 1 - - 
Joueur 1: Bill Gates (410) vs Joueur 2: Robert Martin (620)
Entrez le gagnant (1, 2, ou nul):

$ 1

 - - Tournoi 1 - Round 1 - Match 2 - - 
Joueur 1: Tim Berners-Lee (470) vs Joueur 2: Ken Thompson (650)
Entrez le gagnant (1, 2, ou nul):

$ 2

 - - Tournoi 1 - Round 1 - Match 3 - - 
Joueur 1: Steve Jobs (520) vs Joueur 2: Linus Torvalds (680)
Entrez le gagnant (1, 2, ou nul):

$ nul

 - - Tournoi 1 - Round 1 - Match 4 - - 
Joueur 1: Dennis Ritchie (530) vs Joueur 2: Guido van Rossum (710)
Entrez le gagnant (1, 2, ou nul):

$ 1

 - - Tournoi 1 - Round 2 - Match 1 - - 
Joueur 1: Bill Gates (410) vs Joueur 2: Ken Thompson (650)
Entrez le gagnant (1, 2, ou nul):

$ 1

 - - Tournoi 1 - Round 2 - Match 2 - - 
Joueur 1: Dennis Ritchie (530) vs Joueur 2: Linus Torvalds (680)
Entrez le gagnant (1, 2, ou nul):

$ nul

 - - Tournoi 1 - Round 2 - Match 3 - - 
Joueur 1: Steve Jobs (520) vs Joueur 2: Guido van Rossum (710)
Entrez le gagnant (1, 2, ou nul):

$ 2

 - - Tournoi 1 - Round 2 - Match 4 - - 
Joueur 1: Robert Martin (620) vs Joueur 2: Tim Berners-Lee (470)
Entrez le gagnant (1, 2, ou nul):

$ 2

 - - Tournoi 1 - Round 3 - Match 1 - - 
Joueur 1: Bill Gates (410) vs Joueur 2: Dennis Ritchie (530)
Entrez le gagnant (1, 2, ou nul):

$ nul

 - - Tournoi 1 - Round 3 - Match 2 - - 
Joueur 1: Linus Torvalds (680) vs Joueur 2: Ken Thompson (650)
Entrez le gagnant (1, 2, ou nul):

$ 1

 - - Tournoi 1 - Round 3 - Match 3 - - 
Joueur 1: Guido van Rossum (710) vs Joueur 2: Tim Berners-Lee (470)
Entrez le gagnant (1, 2, ou nul):

$ 1

 - - Tournoi 1 - Round 3 - Match 4 - - 
Joueur 1: Steve Jobs (520) vs Joueur 2: Robert Martin (620)
Entrez le gagnant (1, 2, ou nul):

$ 2

 - - Tournoi 1 - Round 4 - Match 1 - - 
Joueur 1: Bill Gates (410) vs Joueur 2: Linus Torvalds (680)
Entrez le gagnant (1, 2, ou nul):

$ nul

 - - Tournoi 1 - Round 4 - Match 2 - - 
Joueur 1: Dennis Ritchie (530) vs Joueur 2: Guido van Rossum (710)
Entrez le gagnant (1, 2, ou nul):

$ 1

 - - Tournoi 1 - Round 4 - Match 3 - - 
Joueur 1: Ken Thompson (650) vs Joueur 2: Robert Martin (620)
Entrez le gagnant (1, 2, ou nul):

$ 1

 - - Tournoi 1 - Round 4 - Match 4 - - 
Joueur 1: Tim Berners-Lee (470) vs Joueur 2: Steve Jobs (520)
Entrez le gagnant (1, 2, ou nul):

$ 2


> Tournoi terminé
- Classement final:
1 - Bill Gates (3 points)
2 - Dennis Ritchie (3 points)
3 - Linus Torvalds (2.5 points)
4 - Ken Thompson (2 points)
5 - Guido van Rossum (2 points)
6 - Steve Jobs (1.5 points)
7 - Robert Martin (1 points)
8 - Tim Berners-Lee (1 points)
```

</div>
