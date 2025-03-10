from idlelib.configdialog import is_int

class Graphes:
    def __init__(self):
        # Liste des attributs du graphe
        self.tache = [0]
        self.duree = [0]
        self.contraintes = [[]]  # Liste des prédécesseurs pour chaque tâche
        self.matrice = []
        # Attributs pour les résultats du tri et de l'ordonnancement
        self.rangs = []       # Rang de chaque tâche (indice = numéro de tâche)
        self.ordre_topo = []  # Liste des tâches dans l'ordre topologique

    def ajout_omega(self):
        """Ajoute un état oméga à l'automate"""
        self.tache.append(len(self.tache))
        self.duree.append(0)
        self.contraintes.append(list())
        # Rajouter les tâches qui ne sont les contraintes d’aucune autre tâche
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
                tokens = ligne.strip().split()
                self.tache.append(int(tokens[0]))
                self.duree.append(int(tokens[1]))
                if len(tokens) == 2:
                    self.contraintes.append([0])
                else:
                    self.contraintes.append([int(x) for x in tokens[2:]])

    def afficher_contraintes(self):
        """Affiche le tableau avec les tâches, les durées et les prédécesseurs"""
        print("-" * 44)
        print(f"|{'Tâche':^10}|{'Durée':^10}|{'Prédécesseurs':^20}|")
        for i in range(1, len(self.tache)):
            print(f"|{self.tache[i]:^10}|{self.duree[i]:^10}|{', '.join(map(str, self.contraintes[i])):^20}|")
        print("-" * 44 + "\n")

    def creer_matrice(self):
        """Crée une matrice des valeurs à partir des contraintes"""
        self.matrice = [["*" for _ in range(len(self.tache))] for _ in range(len(self.tache))]
        for i in range(1, len(self.tache)):
            for j in self.contraintes[i]:
                self.matrice[j][i] = self.duree[j]

    def afficher_matrice(self):
        """Affiche la matrice des valeurs"""
        print("Matrice des valeurs :")
        print("-" * 9 + "-" * 6 * len(self.tache))
        print(f"|{'Tâche':^7}|", end="")
        for i in range(len(self.tache)):
            print(f"{i:^5}|", end="")
        print("\n|-------" + "".join(["-" * 6] * len(self.tache)) + "|")
        for i in range(len(self.tache)):
            print(f"|{self.tache[i]:^7}", end="|")
            for j in range(len(self.tache)):
                print(f"{self.matrice[i][j]:^5}", end="|")
            print()
        print("-" * 9 + "-" * 6 * len(self.tache) + "\n")

    def verification_graphe(self):
        """Vérifie que le graphe peut servir pour l'ordonnancement."""
        print("* Vérification des arcs négatifs")
        for i in range(len(self.contraintes)):
            for pred in self.contraintes[i]:
                if self.duree[pred] < 0:
                    print("-> Le graphe contient au moins un arc à valeur négative")
                    return False
        print("-> Le graphe ne contient pas d'arc à valeur négative\n")
        print("* Détection de circuit")
        print("* Méthode d’élimination des points d’entrée\n")
        contraintes_copie = {i: list(self.contraintes[i]) for i in range(len(self.tache))}
        sommets = set(range(len(self.tache)))
        while sommets:
            points_entree = [s for s in sommets if len(contraintes_copie[s]) == 0]
            if not points_entree:
                print("\n-> Il y a un circuit")
                return False
            print("Points d'entrée :", " ".join(map(str, points_entree)))
            print("Suppression des points d'entrée")
            for s in points_entree:
                sommets.remove(s)
                del contraintes_copie[s]
            for s in contraintes_copie:
                contraintes_copie[s] = [p for p in contraintes_copie[s] if p not in points_entree]
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
        Stocke le rang de chaque tâche dans self.rangs et l'ordre topologique dans self.ordre_topo.
        """
        contraintes_copie = {i: list(self.contraintes[i]) for i in range(len(self.tache))}
        sommets = set(range(len(self.tache)))
        rang = {}
        rang_courant = 0

        while sommets:
            points_entree = [s for s in sommets if len(contraintes_copie[s]) == 0]
            for s in points_entree:
                rang[s] = rang_courant
            for s in points_entree:
                sommets.remove(s)
                del contraintes_copie[s]
            for s in contraintes_copie:
                contraintes_copie[s] = [p for p in contraintes_copie[s] if p not in points_entree]
            rang_courant += 1

        # Tri des tâches par rang croissant
        sommets_tries = sorted(rang.items(), key=lambda item: item[1])
        self.rangs = [None] * len(self.tache)
        for s, r_val in rang.items():
            self.rangs[s] = r_val

        # Stocker l'ordre topologique
        self.ordre_topo = [sommet for sommet, _ in sommets_tries]

        # Affichage du tableau des rangs et des sommets
        left_width = 8
        cell_width = 5
        total_width = 1 + left_width + 1 + len(self.ordre_topo) * (cell_width + 1)
        sep_line = "-" * total_width

        rang_row = f"|{'Rang'.center(left_width)}|"
        for t in self.ordre_topo:
            rang_row += f"{str(self.rangs[t]).center(cell_width)}|"
        sommet_row = f"|{'Sommet'.center(left_width)}|"
        for t in self.ordre_topo:
            sommet_row += f"{str(t).center(cell_width)}|"

        print(sep_line)
        print(rang_row)
        print(sep_line)
        print(sommet_row)
        print(sep_line)

        return self.ordre_topo

    def calcul_calendriers(self):
        """Calcule les dates au plus tôt et au plus tard en se basant sur les rangs calculés."""
        nb_taches = len(self.tache)
        rangs = self.rangs
        max_r = max(rangs)

        self.temps_tot = [0] * nb_taches
        self.temps_tar = [float('inf')] * nb_taches

        # Calcul du calendrier au plus tôt
        for r in range(max_r + 1):
            for t in range(nb_taches):
                if rangs[t] == r:
                    for pred in self.contraintes[t]:
                        self.temps_tot[t] = max(self.temps_tot[t], self.temps_tot[pred] + self.duree[pred])

        # La date au plus tard de la tâche finale (oméga) est égale à sa date au plus tôt
        self.temps_tar[-1] = self.temps_tot[-1]

        # Calcul du calendrier au plus tard (en ordre inverse)
        for r in range(max_r, -1, -1):
            for t in range(nb_taches):
                if rangs[t] == r:
                    for succ in range(nb_taches):
                        if t in self.contraintes[succ]:
                            self.temps_tar[t] = min(self.temps_tar[t], self.temps_tar[succ] - self.duree[t])

    def calcul_marges(self):
        """Calcule les marges totales et libres"""
        nb_taches = len(self.tache)
        self.marge_totale = [0] * nb_taches

        for t in range(nb_taches):
            self.marge_totale[t] = self.temps_tar[t] - self.temps_tot[t]

    def afficher_resultats(self):
        """
        Affiche le tableau complet en respectant l'ordre du tri topologique.
        Le tableau comporte les lignes :
            - Rang
            - Sommet
            - Date au + tôt
            - Date au + tard
            - Marge totale
            - Marge libre
        """
        ordre = self.ordre_topo  # Ordre des tâches en tri topologique
        n = len(ordre)
        # Choisir une largeur suffisante pour afficher les étiquettes
        labels = ["Rang", "Sommet", "Date au + tôt", "Date au + tard", "Marge totale"]
        left_width = max(len(label) for label in labels) + 2
        cell_width = 5
        total_width = 1 + left_width + 1 + n * (cell_width + 1)
        sep_line = "-" * total_width

        # Construction des lignes du tableau
        rang_row = f"|{'Rang'.center(left_width)}|"
        for t in ordre:
            rang_row += f"{str(self.rangs[t]).center(cell_width)}|"

        sommet_row = f"|{'Sommet'.center(left_width)}|"
        for t in ordre:
            sommet_row += f"{str(t).center(cell_width)}|"

        tot_row = f"|{'Date au + tôt'.center(left_width)}|"
        for t in ordre:
            tot_row += f"{str(self.temps_tot[t]).center(cell_width)}|"

        tar_row = f"|{'Date au + tard'.center(left_width)}|"
        for t in ordre:
            tar_row += f"{str(self.temps_tar[t]).center(cell_width)}|"

        mt_row = f"|{'Marge totale'.center(left_width)}|"
        for t in ordre:
            mt_row += f"{str(self.marge_totale[t]).center(cell_width)}|"

        # Affichage du tableau complet
        print(sep_line)
        print(rang_row)
        print(sep_line)
        print(sommet_row)
        print(sep_line)
        print(tot_row)
        print(sep_line)
        print(tar_row)
        print(sep_line)
        print(mt_row)
        print(sep_line)
