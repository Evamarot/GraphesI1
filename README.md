# Projet d'ordonnancement de tâches

Ce projet permet d'ordonnancer des tâches à partir d'un graphe de contraintes. Le programme lit un fichier de contraintes, construit le graphe correspondant, vérifie sa validité (absence d'arcs négatifs et détection de circuits), puis effectue un tri topologique. À partir de ce tri, il calcule pour chaque tâche :

- La date au plus tôt (avec, en indice, le prédécesseur qui contribue le plus à cette date)
- La date au plus tard (avec, en indice, le successeur qui contraint le plus cette date)
- La marge totale
- La marge libre

Les résultats sont affichés dans un tableau détaillé et interactif.

---

## Fonctionnalités

- **Lecture de fichier de contraintes**  
  Le fichier texte doit contenir une ligne par tâche avec le format suivant :  
  ```
  numéro_de_tâche durée [prédécesseurs]
  ```  
  Par exemple :  
  ```
  1 7
  2 3 1
  3 1 2
  4 8 1
  5 2 3 4
  6 1 3 4
  7 1 3 4
  8 3 6
  9 2 8
  10 1 5 7 9
  ```

- **Ajout de l'état oméga**  
  Un état oméga est ajouté pour représenter la tâche finale, facilitant le calcul des calendriers.

- **Création d'une matrice d'adjacence**  
  La matrice représente les dépendances entre les tâches en indiquant, pour chaque arc, la durée associée.

- **Vérification du graphe**  
  Le programme vérifie que le graphe ne contient pas d'arcs négatifs et détecte d'éventuels circuits via la méthode d'élimination des points d'entrée.

- **Tri topologique et calcul des rangs**  
  Un parcours en largeur permet de calculer le rang de chaque tâche et de déterminer l'ordre topologique.

- **Calcul des calendriers**  
  Pour chaque tâche, la date au plus tôt est calculée en tenant compte de la durée et des prédécesseurs, et la date au plus tard est calculée en partant de la tâche finale (oméga).

- **Calcul des marges**  
  La marge totale (écart entre date au plus tard et date au plus tôt) et la marge libre (écart en fonction des successeurs) sont déterminées pour chaque tâche.

- **Affichage détaillé des résultats**  
  Un tableau final affiche :
  - **Rang** : niveau de la tâche dans le graphe
  - **Sommet** : identifiant de la tâche
  - **Date au + tôt** : date calculée, avec en indice le prédécesseur associé
  - **Date au + tard** : date calculée, avec en indice le successeur associé
  - **Marge totale**
  - **Marge libre**

- **Interface utilisateur interactive**  
  À la fin de chaque exécution, l'utilisateur peut choisir un autre fichier à traiter ou quitter le programme.

---

## Structure du projet

- **main.py**  
  Gère l'interface utilisateur, la sélection des fichiers et l'exécution de l'algorithme complet.

- **Graphes.py**  
  Contient la classe `Graphes` qui implémente toutes les fonctionnalités de lecture, de traitement et d'affichage du graphe.

- **tables_contraintes/**  
  Dossier contenant les fichiers de contraintes à traiter.

---

## Prérequis

- Python 3.x  
- Aucun module externe n'est requis.

---

## Utilisation

1. **Préparation des fichiers**  
   Placez vos fichiers de contraintes dans le dossier `tables_contraintes`. Chaque fichier doit être au format texte et respecter le format décrit ci-dessus.

2. **Exécution du programme**  
   Lancez le programme via la ligne de commande :
   ```bash
   python main.py
   ```
3. **Sélection du fichier**  
   Une liste des fichiers disponibles s'affiche. Entrez le numéro correspondant au fichier que vous souhaitez traiter ou tapez "Q" pour quitter.

4. **Affichage des résultats**  
   Après le traitement, le tableau des résultats s'affiche. Vous verrez pour chaque tâche son rang, ses dates (avec les indices des prédécesseurs ou successeurs associés), ainsi que les marges calculées.

5. **Traitement d'un autre fichier**  
   À la fin de l'exécution, vous avez la possibilité de choisir un autre fichier à traiter ou de sortir du programme.

---

## Auteurs

- Doryan DENIS
- Adria DJAFRI
- Eva MAROT
- Sacha PORTAL
