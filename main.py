def main():

    # Message d'accueil

    while True:

        # Menu principal, avec séléction de l'option
        res = 4
        match res:

            # Tentative de lecture d'un fichier
            case 1:
                pass

            # Affichage du tableau de contraintes
            case 2:
                pass

            # Affichage de la matrice des valeurs du graphe
            case 3:
                pass

            # Quitter le programme
            case 4:
                break

            # Si la valeur n'est pas valide
            case _:
                print("Option non valide, veuillez réessayer")


if __name__ == "__main__":
    main()