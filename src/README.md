# helltaker_ia02

## Présentation

Le projet **helltaker_ia02** contient différents utilitaires pour gérer les grilles *Helltaker*, ainsi que des exemples. Il sera mis à jour au fur et à mesure. Si vous aves des propositions de cartes, n'hésitez pas à nous les soumettre <mailto:sylvain.lagrue@hds.utc.fr>.

## Structure des niveaux

Un simple `.txt` avec un titre en première ligne, un nombre maximum de coups en deuxième ligne, la description du niveau ensuite. Les lignes ne sont pas forcément finies.

- `H`: hero
- `D`: demoness
- `#`: wall
- ` ` : empty
- `B`: block
- `K`: key
- `L`: lock
- `M`: mob (skeleton)
- `S`: spikes
- `T`: trap (safe)
- `U`: trap (unsafe)
- `O`: block on spike
- `P`: block on trap (safe)
- `Q`: block on trap (unsafe)

### Exemple

```
Level 1
23
     ###
  ### H#
 #  M  #
 # M M#
#  ####
# B  B #
# B B  D#
#########
```


## Les utilitaires

Le package python3 `helltaker_utils` permet de lire les fichiers et de vérifier les plans. 

### `grid_from_file(filename: str, voc: dict = {})`

Cette fonction lit un fichier et le convertit en une grille de Helltaker

Arguments:

- filename: fichier contenant la description de la grille
- voc: argument facultatif permettant de convertir chaque case de la grille en votre propre vocabulaire

Retour:

- un dictionnaire contenant:
   - la grille de jeu sous une forme d'une liste de liste de (chaînes de) caractères
   - le nombre de ligne `m`
   - le nombre de colonnes `n`
   - le titre de la grille
   - le nombre maximal de coups `max_steps`

### `check_plan(plan: str)`

Cette fonction vérifie que votre plan est valide.

- Argument: un plan sous forme de chaîne de caractères
- Retour  : `True` si le plan est valide, `False` sinon


