import os
import re
from Graphes import Graphes


def main():
    print("Bienvenue dans le programme d'ordonnancement")
    print("Sélectionnez le fichier de contraintes à utiliser (dossier 'tables_contraintes') :\n")

    folder = "tables_contraintes"
    if not os.path.isdir(folder):
        print("Le dossier 'tables_contraintes' n'existe pas. Fin du programme.")
        return

    # Constitution de la liste des fichiers avec leur numéro extrait
    files = []
    for f in os.listdir(folder):
        if f.endswith(".txt"):
            # Extraction du premier nombre présent dans le nom du fichier
            m = re.search(r'\d+', f)
            num = int(m.group()) if m else float('inf')
            full_path = os.path.join(folder, f)
            files.append((num, full_path, f))

    # Tri des fichiers par le numéro extrait (ordre croissant)
    files.sort(key=lambda x: x[0])

    if not files:
        print("Aucun fichier de contraintes trouvé dans le dossier. Fin du programme.")
        return

    # Affichage de la liste avec uniquement le nom du fichier
    for i, (_, _, filename) in enumerate(files, start=1):
        print(f"{i}. {filename}")

    choix = input("\nEntrez le numéro du fichier à utiliser : ")
    try:
        choix = int(choix)
        if 1 <= choix <= len(files):
            file_selected = files[choix - 1][1]
        else:
            print("Choix invalide. Fin du programme.")
            return
    except ValueError:
        print("Entrée non valide. Fin du programme.")
        return

    print(f"\nFichier sélectionné : {file_selected}\n")

    # Exécution de l'algorithme complet
    g = Graphes()
    g.lecture_fichier(file_selected)
    print("Affichage du tableau de contraintes initial :")
    g.afficher_contraintes()

    g.ajout_omega()
    print("Affichage du tableau de contraintes après ajout de l'oméga :")
    g.afficher_contraintes()

    g.creer_matrice()
    g.afficher_matrice()

    if g.verification_graphe():
        print("-> C’est un graphe d’ordonnancement\n")
        g.calculer_rangs()
    else:
        print("-> Ce n’est pas un graphe d’ordonnancement")


if __name__ == "__main__":
    main()
