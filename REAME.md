

# AI27 Projet Helltaker

Ce dossier contient tous les élements necessaires pour le rendu du projet AI27 Helltaker, encadré par :
- M Sylvain LAGRUE
- M Khaled BELAHCENE

Ce projet a été réalisé par :
-	Mostafa ABOU GHALIA
-	Tristan DEREIGNE
-	Edouard LE

## Structure du dossier

### 0.STRIPS
Ce dossier contient la modélisation du jeu helltaker en language STRIPS. Cette modélisation a pour but de simplifier le codage en ASPPLAN et en SATPLAN;

Deux fichiers ont été généré et contiennent le même contenu. 
Toutes les explications jugées necessaire sont en 'commentaire' dans les fichiers.
### 1.ASPPLAN
Nous n'avons pas terminé le génerateur d'ASP en Python, 
Pour lancer les fichiers ASP, la commande commande clingo est en début de chaque fichier :
clingo -c h=nb d'actions -n0 .\helltaker_lvl1.lp

Le generation d'ASP en python existe néanmoins

### 2. SATPLAN

Pour lancer le programme avec le solveur glophersat:
```
python helltaker_plan_glophersat chemin_du_fichier
```


Pour lancer le programme avec le solveur pycosat:
```
python helltaker_plan_pycosat chemin_du_fichier
```
Remplacer $chemin_du_fichier$ par le fichiers level$x$.txt