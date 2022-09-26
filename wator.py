
from random import randint, choice
from time import sleep
import os

class Monde:
    def __init__(self, largeur: int, hauteur: int):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[ " " for _ in range(largeur)] for _ in range(hauteur)]
    
    def afficher_monde(self):
        """
        Fonction qui affiche le monde dans la console.
        """
        collumn_head = "  "
        row_head = 0

        # Affiche en tête des collumns des chiffres
        for collumn in range(self.largeur):
            collumn_head += "  " + str(collumn) + "  "
        print(collumn_head)

        # Affiche en début de ligne des chiffres et print la ligne
        for ligne in self.grille:
            print(str(row_head) + " " + str(ligne))
            row_head += 1

    def peupler(self, nb_poisson: int, nb_requin: int):
        """
        Fonction qui fait apparaître les poissons sur le monde
        : param nb_poisson (int) : Nombre de poissons à faire apparaître
        : param nb_requi (int) : Nombre de requin à faire apparaître
        """
        nb_total = nb_poisson + nb_requin
        case_total = self.hauteur * self.largeur
        if nb_total > case_total:
            print(ValueError(" \nLe nombre d'entités entrées est supérieur aux nombres de places disponnibles !\n".upper()))
            return
        max_poisson = 0
        max_requin = 0
        while True:
            random_y = randint(0, self.hauteur-1)
            random_x = randint(0, self.largeur-1)
            if nb_poisson > max_poisson:
                if self.grille[random_y][random_x] == " ":
                    self.grille[random_y][random_x] = "X"
                    max_poisson += 1
            else:
                break
        while True:
            random_y = randint(0, self.hauteur-1)
            random_x = randint(0, self.largeur-1)
            if nb_requin > max_requin:
                if self.grille[random_y][random_x] == " ":
                    self.grille[random_y][random_x] = "O"
                    max_requin += 1
            else:
                break

    
    def jouer_un_tour(self):
        pass

class Poisson:
    def __init__(self, x, y):
        pass
    
    def deplacement_possible(self, monde):
        pass
    
    def se_deplacer(self, monde):
        pass
        
    def vivre_une_journee(self, monde):
        pass

monde = Monde(10, 8)
monde.peupler(20, 20)
monde.afficher_monde()