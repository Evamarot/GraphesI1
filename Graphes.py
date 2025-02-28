class Graphes:
    def __init__(self):
        # Liste des attributs de l'automate
        self.tache = [0]
        self.duree = [0]
        self.contraintes = [[]] #Liste des prédécesseurs pour chaque tâche

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

    def afficher_contraintes(self):
        """Affiche le tableau avec les tâches, les durées et les prédécessseurs"""
        print(f"{'Tâche':<10}{'Durée':<10}{'Prédécesseurs':<20}")
        for i in range(1, len(self.tache)):
            print(f"{self.tache[i]:<10}{self.duree[i]:<10}{', '.join(map(str, self.contraintes[i])):<20}")

    
    # Ici tri topologique avec les rangs des sommets
    

    def calcul_calendriers(self):
        """Calcule les dates au plus tôt et au plus tard"""
        #ordre, rangs = self.tri_topologique_avec_rangs()
        ordre = [0, 1, 2, 3, 4, 5, 6]
        rangs = [0, 1, 1, 2, 2, 3, 4] #On compte oméga
        nb_taches = len(self.tache)

        # Initialisation des calendriers
        self.temps_tot = [0] * nb_taches  
        self.temps_tar = [float('inf')] * nb_taches  

        # Calcul du calendrier au plus tôt
        for r in range(max(rangs)+1):
            for t in range(nb_taches):
                if rangs[t] == r:
                    for pred in self.contraintes[t]:
                        self.temps_tot[t] = max(self.temps_tot[t], self.temps_tot[pred] + self.duree[pred])

        # La date au plus tard de la tâche finale ω est égale à sa date au plus tôt
        self.temps_tar[-1] = self.temps_tot[-1]

        # Calcul du calendrier au plus tard (ordre inverse)
        for r in range(max(rangs), -1, -1):
            for t in range(nb_taches):
                if rangs[t] == r:
                    for succ in range(nb_taches):
                        if t in self.contraintes[succ]:
                            self.temps_tar[t] = min(self.temps_tar[t], self.temps_tar[succ] - self.duree[t])


    def calcul_marges(self):
        """Calcule les marges totales et libres"""
        nb_taches = len(self.tache)
        self.marge_totale = [0] * nb_taches
        self.marge_libre = [0] * nb_taches

        # Calcul des marges totales
        for t in range(nb_taches):
            self.marge_totale[t] = self.temps_tar[t] - self.temps_tot[t]

        # Calcul des marges libres
        for t in range(nb_taches):
            successeurs = [s for s in range(nb_taches) if t in self.contraintes[s]]
            if successeurs: 
                self.marge_libre[t] = min(self.temps_tot[s] for s in successeurs) - (self.temps_tot[t] + self.duree[t])
            else:  # Si la tâche n'a pas de successeurs
                self.marge_libre[t] = self.marge_totale[t]

    def afficher_resultats(self):
        """Affiche les résultats : dates et marges"""
        print(f"{'Tâche':<10}{'Début au + tôt':<15}{'Fin au + tard':<15}{'Marge totale':<15}{'Marge libre':<15}")
        for t in range(len(self.tache)):
            print(f"{t:<10}{self.temps_tot[t]:<15}{self.temps_tar[t]:<15}{self.marge_totale[t]:<15}{self.marge_libre[t]:<15}")


if __name__ == "__main__":
    g = Graphes()
    g.lecture_fichier("tc_test.txt")

    print("Avant l'ajout de l'oméga :")
    print(g.tache)
    print(g.duree)
    print(g.contraintes)
    g.afficher_contraintes()

    print("\nAprès l'ajout de l'oméga :")
    g.ajout_omega()
    print(g.tache)
    print(g.duree)
    print(g.contraintes)

    print("\nCalendriers et marges :")
    g.calcul_calendriers()
    g.calcul_marges()
    g.afficher_resultats()
    #Pour l'instant ne marche pas car l'affichage des contraintes ne prend pas en compte 0 et 6