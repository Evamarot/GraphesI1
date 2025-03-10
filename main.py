import os
import re
from Graphes import Graphes

def main():
    print("Projet d'ordonnancement de tâches\n")
    folder = "tables_contraintes"
    if not os.path.isdir(folder):
        print("Le dossier 'tables_contraintes' n'existe pas. Fin du programme.")
        return

    while True:
        # Constitution de la liste des fichiers avec leur numéro extrait
        files = []
        for f in os.listdir(folder):
            if f.endswith(".txt"):
                # Extraction du premier nombre présent dans le nom du fichier
                m = re.search(r'\d+', f)
                num = int(m.group()) if m else float('inf')
                full_path = os.path.join(folder, f)
                files.append((num, full_path, f))
        files.sort(key=lambda x: x[0])

        if not files:
            print("Aucun fichier de contraintes trouvé dans le dossier. Fin du programme.")
            return

        # Affichage de la liste avec le nom des fichiers et option pour quitter
        print("\nSélectionnez le fichier de contraintes à utiliser (ou tapez Q pour quitter) :\n")
        for i, (_, _, filename) in enumerate(files, start=1):
            print(f"{i}. {filename}")

        choix = input("\nEntrez le numéro du fichier à utiliser (ou Q pour quitter) : ")
        if choix.lower() == "q":
            print("Fin du programme.")
            break
        try:
            choix = int(choix)
            if 1 <= choix <= len(files):
                file_selected = files[choix - 1][1]
            else:
                print("Choix invalide.")
                continue
        except ValueError:
            print("Entrée non valide.")
            continue

        print(f"\nFichier sélectionné : {file_selected}\n")

        # Exécution de l'algorithme complet
        g = Graphes()
        g.lecture_fichier(file_selected)
        print("* Affichage du tableau de contraintes initial :")
        g.afficher_contraintes()

        g.ajout_omega()
        print("* Affichage du tableau de contraintes après ajout de l'oméga :")
        g.afficher_contraintes()

        g.creer_matrice()
        g.afficher_matrice()

        if g.verification_graphe():
            print("-> C’est un graphe d’ordonnancement\n")
            # Calcul du tri topologique et stockage des rangs
            g.calculer_rangs()
            # Calcul des calendriers (dates au plus tôt et au plus tard)
            g.calcul_calendriers()
            # Calcul des marges totales et libres
            g.calcul_marges()
            print("* Résultats des calculs du calendrier et des marges :")
            g.afficher_resultats()
        else:
            print("-> Ce n’est pas un graphe d’ordonnancement")

        # Demander si l'utilisateur souhaite traiter un autre fichier
        rep = input("\nVoulez-vous traiter un autre fichier ? (O/N) : ")
        if rep.lower() not in ["o", "oui"]:
            print("Fin du programme.")
            break


if __name__ == "__main__":
    main()
