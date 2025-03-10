from idlelib.configdialog import is_int

class Graphes:
    def __init__(self):
        # Liste des attributs du graphe
        self.tache = [0]
        self.duree = [0]
        self.contraintes = [[]] #Liste des prédécesseurs pour chaque tâche

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

    def lecture_fichier(self, file: str):
        """Lit un fichier contenant un graphe pour en récupérer les tâches"""
        with open(file, 'r') as f:
            text = f.readlines()
            for ligne in text:
                # Élimine les espaces en début/fin et découpe la ligne par défaut (en se basant sur tout espace blanc)
                tokens = ligne.strip().split()

                self.tache.append(int(tokens[0]))
                self.duree.append(int(tokens[1]))

                if len(tokens) == 2:
                    self.contraintes.append([0])
                else:
                    self.contraintes.append([int(x) for x in tokens[2:]])

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

    def verification_graphe(self):
        """Vérifie que le graphe peut servir pour l'ordonnancement. """

        # Vérification des arcs négatifs
        print("* Vérification des arcs négatifs")
        for i in range(len(self.contraintes)):
            for pred in self.contraintes[i]:
                if self.duree[pred] < 0:
                    print("-> Le graphe contient au moins un arc à valeur négative")
                    return False

        print("-> Le graphe ne contient pas d'arc à valeur négative\n")

        # Détection de circuit par élimination des points d'entrée
        print("* Détection de circuit")
        print("* Méthode d’élimination des points d’entrée\n")

        # Copie des contraintes pour ne pas modifier l'original
        contraintes_copie = {}
        for i in range(len(self.tache)):
            contraintes_copie[i] = list(self.contraintes[i])

        # Création de l'ensemble des sommets présents dans le graphe
        sommets = set()
        for i in range(len(self.tache)):
            sommets.add(i)

        while sommets:
            # Identifier les points d'entrée : les sommets sans prédécesseurs
            points_entree = []
            for s in sommets:
                if len(contraintes_copie[s]) == 0:
                    points_entree.append(s)

            if not points_entree:
                print("\n-> Il y a un circuit")
                return False

            # Affichage et suppression des points d'entrée
            print("Points d'entrée :", " ".join(map(str, points_entree)))
            print("Suppression des points d'entrée")
            for s in points_entree:
                sommets.remove(s)
                del contraintes_copie[s]

            # Mise à jour des listes de prédécesseurs pour retirer les sommets supprimés
            for s in contraintes_copie:
                nouveaux_predecesseurs = []
                for p in contraintes_copie[s]:
                    if p not in points_entree:
                        nouveaux_predecesseurs.append(p)
                contraintes_copie[s] = nouveaux_predecesseurs

            # Affichage des sommets restants
            if sommets:
                print("Sommets restant :", " ".join(map(str, sorted(sommets))))
                print("")
            else:
                print("Sommets restant : Aucun")

        print("\n-> Il n’y a pas de circuit")
        return True

    def calculer_rangs(self):
        """
        Calcule les rangs de tous les sommets du graphe en utilisant un parcours en largeur.
        Retourne la liste des sommets ordonnés par rang croissant.
        """

        # Copie des contraintes
        contraintes_copie = {}
        for i in range(len(self.tache)):
            contraintes_copie[i] = list(self.contraintes[i])

        # Ensemble des sommets présents dans le graphe
        sommets = set()
        for i in range(len(self.tache)):
            sommets.add(i)

        # Dictionnaire pour stocker le rang de chaque sommet
        rang = {}
        rang_courant = 0  # Rang courant

        # Parcours en largeur
        while sommets:
            # Identifier les points d'entrée
            points_entree = []
            for s in sommets:
                if len(contraintes_copie[s]) == 0:
                    points_entree.append(s)

            # Assigner le rang courant à tous les points d'entrée
            for s in points_entree:
                rang[s] = rang_courant

            # Retirer les points d'entrée de l'ensemble des sommets et de la copie des contraintes
            for s in points_entree:
                sommets.remove(s)
                del contraintes_copie[s]

            # Mise à jour des listes de prédécesseurs pour les sommets restants
            for s in contraintes_copie:
                nouveaux_predecesseurs = []
                for p in contraintes_copie[s]:
                    if p not in points_entree:
                        nouveaux_predecesseurs.append(p)
                contraintes_copie[s] = nouveaux_predecesseurs

            # Passage au niveau suivant
            rang_courant += 1

        # Tri des sommets par rang croissant
        sommets_tries = sorted(rang.items(), key=lambda item: item[1])

        # Construction des listes pour les rangs et les sommets
        rangs_list = [str(r_val) for (_, r_val) in sommets_tries]
        sommets_list = [str(som) for (som, _) in sommets_tries]

        # Paramètres de formatage
        left_width = 8  # largeur de la colonne de gauche (pour " Rang " et " Sommet ")
        cell_width = 5  # largeur de chaque cellule de donnée

        # Calcul de la largeur totale du tableau :
        # 1 pour le premier "|" + left_width + 1 pour la barre verticale après la colonne de gauche
        # + pour chaque cellule : (cell_width + 1)
        total_width = 1 + left_width + 1 + len(sommets_list) * (cell_width + 1)
        sep_line = "-" * total_width

        # Affichage du tableau avec un "|" initial et un espacement autour de "Rang" et "Sommet"
        print(sep_line)
        print(f"|{' Rang ':^{left_width}}|", end="")
        for r in rangs_list:
            print(f"{r:^{cell_width}}|", end="")
        print()
        print(sep_line)
        print(f"|{' Sommet ':^{left_width}}|", end="")
        for s in sommets_list:
            print(f"{s:^{cell_width}}|", end="")
        print()
        print(sep_line)

        # Retourne la liste des sommets dans l'ordre des rangs croissants
        return [sommet for sommet, rang_val in sommets_tries]

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