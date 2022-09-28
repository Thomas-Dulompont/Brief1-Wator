
from multiprocessing.sharedctypes import Value
from random import randint, choice
from copy import deepcopy
from time import sleep
import os

class Monde:
    def __init__(self, largeur: int, hauteur: int):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[ "  " for _ in range(largeur)] for _ in range(hauteur)]
        self.poissons = []
    
    def afficher_monde(self):
        """
        Fonction qui affiche le monde dans la console.
        """
        affichee_grille = deepcopy(self.grille)

        for ligne_grille in affichee_grille:
            for case_grille in ligne_grille:
                if type(case_grille) == Poisson:
                    ligne_grille[ligne_grille.index(case_grille)] = "🐠"
            print(str(ligne_grille))


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
        while nb_poisson > max_poisson:
            random_y = randint(0, self.hauteur-1)
            random_x = randint(0, self.largeur-1)
            if self.grille[random_y][random_x] == "  ":
                self.grille[random_y][random_x] = Poisson(random_y, random_x)
                max_poisson += 1
        while nb_requin > max_requin:
            random_y = randint(0, self.hauteur-1)
            random_x = randint(0, self.largeur-1)
            if self.grille[random_y][random_x] == "  ":
                self.grille[random_y][random_x] = "🦈"
                max_requin += 1

    
    def jouer_un_tour(self):
        for ligne in self.grille:
            for case in ligne:
                if isinstance(case, Poisson):
                    self.poissons.append(case)
        
        for poisson in self.poissons:
            print(poisson)
            poisson.vivre_une_journee(self)

        self.afficher_monde()

class Poisson:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x
        self.reproduction = 0
    
    def deplacement_possible(self, monde):
        deplacements = []
        if monde.grille[(self.y+1) % monde.hauteur][self.x] == "  ":
            deplacements.append(((self.y+1) % monde.hauteur, self.x))
        
        if monde.grille[(self.y-1) % monde.hauteur][self.x] == "  ":
            deplacements.append(((self.y-1) % monde.hauteur, self.x))
        
        if monde.grille[self.y][(self.x+1) % monde.largeur] == "  ":
            deplacements.append((self.y, (self.x+1) % monde.largeur))
        
        if monde.grille[self.y][(self.x-1) % monde.largeur] == "  ":
            deplacements.append((self.y, (self.x-1) % monde.largeur))

        return deplacements


    def se_deplacer(self, monde, deplacements):
        preced_y = self.y
        preced_x = self.x

        if deplacements != []:
            choix = choice(deplacements)
            if self.reproduction > 4:
                monde.grille[preced_y][preced_x] = Poisson(choix[0],choix[1])
                monde.grille[choix[0]][choix[1]] = self
                self.reproduction = 0
                return True
            else: 
                monde.grille[choix[0]][choix[1]] = self
                monde.grille[preced_y][preced_x] = "  "       
                return True
        
    def vivre_une_journee(self, monde):
        if self.se_deplacer(monde, self.deplacement_possible(monde)):
            self.reproduction += 1

monde = Monde(5, 5)
monde.peupler(3, 5)
monde.afficher_monde()
for _ in range(2):
    print("------------------")
    monde.jouer_un_tour()