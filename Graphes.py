from collections import OrderedDict


class Graphes:
    def __init__(self):
        # Liste des attributs du graphe
        self.tache = [0]
        self.duree = [0]
        self.contraintes = [[]]  # Liste des prédécesseurs pour chaque tâche
        self.matrice = []
        # Attributs pour les résultats du tri et de l'ordonnancement
        self.rangs = []  # Rang de chaque tâche (indice = numéro de tâche)
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
        print("─" * 44)
        print(f"│{'Tâche':^10}│{'Durée':^10}│{'Prédécesseurs':^20}│")
        for i in range(1, len(self.tache)):
            print(f"│{self.tache[i]:^10}│{self.duree[i]:^10}│{', '.join(map(str, self.contraintes[i])):^20}│")
        print("─" * 44 + "\n")

    def creer_matrice(self):
        """Crée une matrice des valeurs à partir des contraintes"""
        self.matrice = [["*" for _ in range(len(self.tache))] for _ in range(len(self.tache))]
        for i in range(1, len(self.tache)):
            for j in self.contraintes[i]:
                self.matrice[j][i] = self.duree[j]

    def afficher_matrice(self):
        """Affiche la matrice des valeurs"""
        print("* Matrice des valeurs :")
        print("─" * 9 + "─" * 6 * len(self.tache))
        print(f"│{'Tâche':^7}│", end="")
        for i in range(len(self.tache)):
            print(f"{i:^5}│", end="")
        print("\n│───────" + "".join(["─" * 6] * len(self.tache)) + "│")
        for i in range(len(self.tache)):
            print(f"│{self.tache[i]:^7}", end="│")
            for j in range(len(self.tache)):
                print(f"{self.matrice[i][j]:^5}", end="│")
            print()
        print("─" * 9 + "─" * 6 * len(self.tache) + "\n")

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
        ordre = self.ordre_topo  # Ordre des tâches en tri topologique
        n = len(ordre)
        labels = ["Rang", "Sommet", "Date au + tôt", "Date au + tard", "Marge totale", "Marge libre"]
        left_width = max(len(label) for label in labels) + 2
        cell_width = 10
        total_width = 1 + left_width + 1 + n * (cell_width + 1)
        sep_line = "─" * total_width

        def pred_assoc(t):
            preds = self.contraintes[t]
            if preds:
                finish_times = [self.temps_tot[p] + self.duree[p] for p in preds]
                max_finish = max(finish_times)
                best_preds = [str(p) for p, finish in zip(preds, finish_times) if finish == max_finish]
                return "(" + ", ".join(best_preds) + ")"
            return ""

        def succ_assoc(t):
            succs = [s for s in range(len(self.tache)) if t in self.contraintes[s]]
            if succs:
                time_tar = [self.temps_tar[s] - self.duree[t] for s in succs]
                min_time_tar = min(time_tar)
                best_succs = [str(s) for s, time in zip(succs, time_tar) if time == min_time_tar]
                return "(" + ", ".join(best_succs) + ")"
            return ""

        rang_row = f"│{'Rang'.center(left_width)}│"
        for t in ordre:
            rang_row += f"{str(self.rangs[t]).center(cell_width)}│"

        sommet_row = f"│{'Sommet'.center(left_width)}│"
        for t in ordre:
            sommet_row += f"{str(t).center(cell_width)}│"

        tot_row = f"│{'Date au + tôt'.center(left_width)}│"
        for t in ordre:
            tot_str = f"{self.temps_tot[t]}{pred_assoc(t)}"
            tot_row += f"{tot_str.center(cell_width)}│"

        tar_row = f"│{'Date au + tard'.center(left_width)}│"
        for t in ordre:
            tar_str = f"{self.temps_tar[t]}{succ_assoc(t)}"
            tar_row += f"{tar_str.center(cell_width)}│"

        mt_row = f"│{'Marge totale'.center(left_width)}│"
        for t in ordre:
            mt_row += f"{str(self.marge_totale[t]).center(cell_width)}│"

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

    def chemin_critique(self):
        """
        Retourne tous les chemins critiques (sous forme de chaînes) en respectant :
          - Seuls les successeurs de α ayant une marge totale de 0 sont considérés.
          - Un arc (i → j) est critique si self.temps_tot[i] + self.duree[i] == self.temps_tot[j].
          - On explore en profondeur (DFS) en mémorisant les résultats pour éviter les redondances.
          - Les successeurs sont traités dans l’ordre croissant (ordre alphabétique si les nœuds sont des nombres).
          - Seuls les chemins dont la durée totale (la somme des durées) est égale à la durée du projet
            (self.temps_tot[-1]) sont retenus.
        """
        final_node = len(self.tache) - 1
        project_duration = self.temps_tot[final_node]
        memo = {}

        def dfs(node):
            # Si on atteint le nœud final, retourner un chemin contenant uniquement ce nœud.
            if node == final_node:
                return [[final_node]]
            if node in memo:
                return memo[node]
            paths = []
            # Récupérer les successeurs de 'node' en se basant sur les contraintes
            # On ne considère que les successeurs qui :
            # • Ont une marge totale de 0,
            # • Respectent la condition critique : temps_tot[node] + duree[node] == temps_tot[succ]
            successeurs = []
            for succ in range(len(self.tache)):
                if node in self.contraintes[succ]:
                    if self.marge_totale[succ] == 0 and (
                            self.temps_tot[node] + self.duree[node] == self.temps_tot[succ]):
                        successeurs.append(succ)
            # Traiter les successeurs dans l'ordre croissant (ordre alphabétique)
            successeurs.sort()
            for s in successeurs:
                for sub_path in dfs(s):
                    paths.append([node] + sub_path)
            memo[node] = paths
            return paths

        # Lancer la recherche depuis le nœud de départ (α = 0)
        all_paths = dfs(0)
        # Filtrer pour ne garder que les chemins dont la durée totale est exactement celle du projet.
        critical_paths = []
        for path in all_paths:
            # Calcul de la somme des durées sur le chemin
            path_duration = sum(self.duree[node] for node in path)
            if path_duration == project_duration:
                critical_paths.append(path)
        # Formatage de l'affichage : un chemin par ligne avec les nœuds séparés par " -> "
        formatted_paths = ["• " + " -> ".join(map(str, path)) for path in critical_paths]
        return "\n".join(formatted_paths)

