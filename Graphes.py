from idlelib.configdialog import is_int


class Graphes:
    def __init__(self):
        # Liste des attributs du graphe
        self.tache = [0]
        self.duree = [0]
        self.contraintes = [[]]

        # Matrice d'adjacence

        # COMMENTAIRES A SUPPRIMER :
        # self.matrice a la même forme que dans l'exemple donné : si des tâches sont
        # des contraintes, alors elle est ajoutée dans le tableau, sinon une étoile est rajoutée.
        #
        # Cela veut dire que si une tâche est une contrainte, alors la case contient une valeur numérique
        # plutôt qu'une chaine de caractère. On peut donc facilement filtrer en faisant des is_int(x).

        self.matrice = []


    def ajout_omega(self):
        """Ajoute un état oméga à l'automate"""
        self.tache.append(len(self.tache))
        self.duree.append(0)
        self.contraintes.append(list())
        # Rajouter les tâches qui ne sont les contraintes d'aucune autre tâche
        for t in self.tache[1:-1]:
            for c in self.contraintes:
                if t in c:
                    break
            else:
                self.contraintes[-1].append(t)


    def lecture_fichier(self, file:str):
        """Lis un fichier contenant un graphe pour en récupérer les tâches"""
        with open(file, 'r') as f:
            text = f.readlines()
            for i, ligne in enumerate(text):

                if i != len(text) - 1: ligne = ligne[:-1].split(" ")
                else: ligne = ligne.split(" ")

                self.tache.append(int(ligne[0]))
                self.duree.append(int(ligne[1]))

                if len(ligne) == 2:
                    self.contraintes.append([0])
                else:
                    self.contraintes.append([int(x) for x in ligne[2:]])

    def afficher_contraintes(self):
        """Affiche le tableau avec les tâches, les durées et les prédécessseurs"""
        print("-" * 44)
        print(f"|{'Tâche':^10}|{'Durée':^10}|{'Prédécesseurs':^20}|")
        for i in range(1, len(self.tache)):
            print(f"|{self.tache[i]:^10}|{self.duree[i]:^10}|{', '.join(map(str, self.contraintes[i])):^20}|")
        print("-" * 44 + "\n")

    def creer_matrice(self):
        """Crée une matrice des valeurs à partir des contraintes"""

        # Création de la matrice de taille (n+1) x (n+1) avec des étoiles
        self.matrice = [["*" for _ in range(len(self.tache))] for _ in range(len(self.tache))]

        # Remplissage de la matrice avec les durées des contraintes
        for i in range(1, len(self.tache)):
            for j in self.contraintes[i]:
                self.matrice[j][i] = self.duree[j]

    def afficher_matrice(self):
        """Affiche la matrice des valeurs"""
        print("Matrice des valeurs :")

        # Ligne supérieure du tableau
        print("-" * 9 + "-" * 6 * len(self.tache))

        # Ligne des tâches et des labels
        print(f"|{'Tâche':^7}|", end="")
        for i in range(len(self.tache)):
            print(f"{i:^5}|", end="")

        # Ligne de séparation entre les tâches et les valeurs
        print("\n|-------" + "".join(["-" * 6] * len(self.tache)) + "|")

        # Affichage des lignes des valeurs
        for i in range(len(self.tache)):
            # Colonne des tâches
            print(f"|{self.tache[i]:^7}", end="|")

            # Cellules des valeurs de la ligne
            for j in range(len(self.tache)):
                print(f"{self.matrice[i][j]:^5}", end="|")
            print()

        # Ligne inférieure du tableau
        print("-" * 9 + "-" * 6 * len(self.tache) + "\n")

# Programme principal pour tester les fonctions
# A SUPPRIMER POUR LA VERSION FINALE
if __name__ == "__main__":
    g = Graphes()
    g.lecture_fichier("tc_test.txt")

    print("Avant l'ajout de l'oméga :")
    print(g.tache)
    print(g.duree)
    print(g.contraintes, end="\n\n")
    g.afficher_contraintes()

    print("\nAprès l'ajout de l'oméga :")
    g.ajout_omega()
    print(g.tache)
    print(g.duree)
    print(g.contraintes, end="\n\n")
    g.afficher_contraintes()

    g.creer_matrice()
    g.afficher_matrice()