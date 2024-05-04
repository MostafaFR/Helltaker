import sys
from helltaker_utils import grid_from_file, check_plan


def monsuperplanificateur(infos):
    return "hbgd"


def main():
    # récupération du nom du fichier depuis la ligne de commande
    filename = sys.argv[1]

    # récupération de al grille et de toutes les infos
    infos = grid_from_file(filename)

    # calcul du plan
    plan = monsuperplanificateur(infos)

    # affichage du résultat
    if check_plan(plan):
        print("[OK]", plan)
    else:
        print("[Err]", plan, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()