class Graphes:
    def __init__(self):
        # Liste des attributs de l'automate
        self.tache = [0]
        self.duree = [0]
        self.contraintes = [[]]

    def ajout_omega(self):
        """Ajoute un état oméga à l'automate"""
        self.tache.append(len(self.tache))
        self.duree.append(0)
        self.contraintes.append(list())
        # Rajouter la seule tâche qui n'est la contrainte d'aucune autre tâche
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

if __name__ == "__main__":
    g = Graphes()
    g.lecture_fichier("tc_test.txt")

    print("Avant l'ajout de l'oméga :")
    print(g.tache)
    print(g.duree)
    print(g.contraintes)

    print("\nAprès l'ajout de l'oméga :")
    g.ajout_omega()
    print(g.tache)
    print(g.duree)
    print(g.contraintes)