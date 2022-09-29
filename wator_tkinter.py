from tkinter import * 
from random import randint, choice
import time
import os

color_water = "#003dd6"
tile_size = 1
location_canvas = 1

def lancer_simulation():
        monde.jouer_un_tour()
        canvas.update_idletasks()
        print("Mise à jour du canvas")
        canvas.after(200, lancer_simulation())

class Monde:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[ "  " for _ in range(largeur)] for _ in range(hauteur)]
        self.poissons = []
        self.requins = []
    
    def afficher_monde(self):
        """
        Fonction qui affiche le monde dans la console.
        """
        canvas.delete("poisson")
        canvas.delete("requin")
        for ligne in self.grille:
            for case in ligne:
                x_current = self.grille.index(ligne)
                y_current = self.grille[self.grille.index(ligne)].index(case)
                if isinstance(case,Poisson):
                    canvas.create_rectangle(x_current + location_canvas, y_current + location_canvas, x_current + tile_size, y_current + tile_size, outline="", fill="#fb0", tags="poisson")
                elif isinstance(case,Requin):
                    canvas.create_rectangle(x_current + location_canvas, y_current + location_canvas, x_current + tile_size, y_current + tile_size, outline="", fill="#00d600", tags="requin")

    def peupler(self, nb_poisson, nb_requin):
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
                self.grille[random_y][random_x] = Requin(random_y, random_x)
                max_requin += 1

    
    def jouer_un_tour(self):
        """
        Fonction qui fait jouer toutes les entitées
        """
        # Reintialiser les Listes d'entités
        self.poissons = []
        self.requins = []

        # Ajout des Poissons dans la Liste d'entités
        for ligne in self.grille:
            for case in ligne:
                if isinstance(case, Poisson):
                    self.poissons.append(case)

        # Faire vivre une journée aux Poissons
        for poisson in self.poissons:
            poisson.vivre_une_journee(self)

        # Ajout des Requins dans la Liste d'entités
        for ligne in self.grille:
            for case in ligne:
                if isinstance(case, Requin):
                    self.requins.append(case)

        # Faire vivre une journée aux Poissons
        for requin in self.requins:
            requin.vivre_une_journee(self)

        # Afficher le monde
        self.afficher_monde()

class Poisson:
    def __init__(self, y, x):
        """
        Fonction qui est appeler à chaque requin
        : param y (int) :  Coordonnées en Y
        : param x (int) :  Coordonnées en X
        """
        self.y = y
        self.x = x
        self.reproduction = 0
    
    def deplacement_possible(self, monde):
        """
        Fonction qui analyse les déplacements disponnibles
        : param monde (list) :  Emplacement des entitées
        """
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
        """
        Fonction qui deplace les poissons et en ajoute si il peut
        : param monde (list) :  Emplacement des entitées
        : param deplacements (list) : Liste des déplacements disponnibles
        """
        preced_y = self.y
        preced_x = self.x

        if deplacements != []:
            choix = choice(deplacements)
            if self.reproduction >= 4:
                self.y = choix[0]
                self.x = choix[1]

                monde.grille[preced_y][preced_x] = Poisson(preced_y,preced_x)

                monde.grille[choix[0]][choix[1]] = self
                self.reproduction = 0
            else: 
                self.y = choix[0]
                self.x = choix[1]

                monde.grille[choix[0]][choix[1]] = self
                monde.grille[preced_y][preced_x] = "  "

    def vivre_une_journee(self, monde):
        """
        Fonction qui fait se deplacer
        : param monde (list) :  Emplacement des entitées
        """
        self.se_deplacer(monde, self.deplacement_possible(monde))
        self.reproduction += 1

class Requin:
    def __init__(self, y, x):
        """
        Fonction qui est appeler à chaque requin
        : param y (int) :  Coordonnées en Y
        : param x (int) :  Coordonnées en X
        """
        self.y = y
        self.x = x
        self.reproduction = 0
        self.energie = 6
    
    def deplacement_possible(self, monde):
        """
        Fonction qui analyse les déplacements disponnibles
        : param monde (list) :  Emplacement des entitées
        """
        deplacements = []
        # Chercher les Poissons
        if isinstance(monde.grille[(self.y+1) % monde.hauteur][self.x], Poisson):
            deplacements.append(((self.y+1) % monde.hauteur, self.x))
            return deplacements
        elif isinstance(monde.grille[(self.y-1) % monde.hauteur][self.x], Poisson):
            deplacements.append(((self.y-1) % monde.hauteur, self.x))
            return deplacements
        elif isinstance(monde.grille[self.y][(self.x+1) % monde.largeur], Poisson):
            deplacements.append((self.y, (self.x+1) % monde.largeur))
            return deplacements
        elif isinstance(monde.grille[self.y][(self.x-1) % monde.largeur], Poisson):
            deplacements.append((self.y, (self.x-1) % monde.largeur))
            return deplacements
        else:
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
        """
        Fonction qui deplace les requins et en ajoute si il peut
        : param monde (list) :  Emplacement des entitées
        : param deplacements (list) : Liste des déplacements disponnibles
        """
        preced_y = self.y
        preced_x = self.x
        if self.energie == 0:
            monde.grille[self.y][self.x] = "  "
        elif deplacements != []:
            choix = choice(deplacements)
            # Vérifie si le choix est un poisson
            if isinstance(monde.grille[choix[0]][choix[1]], Poisson):
                if self.reproduction >= 4:
                    self.y = choix[0]
                    self.x = choix[1]

                    monde.grille[preced_y][preced_x] = Requin(preced_y,preced_x)

                    monde.grille[choix[0]][choix[1]] = self
                    self.reproduction = 0
                else:
                    self.y = choix[0]
                    self.x = choix[1]

                    monde.grille[choix[0]][choix[1]] = self
                    monde.grille[preced_y][preced_x] = "  "
                # Ajout d'energie si le requin mange un poisson
                self.energie += 6
            elif self.reproduction >= 10:
                self.y = choix[0]
                self.x = choix[1]

                monde.grille[preced_y][preced_x] = Requin(preced_y,preced_x)

                monde.grille[choix[0]][choix[1]] = self
                self.reproduction = 0
            else: 
                self.y = choix[0]
                self.x = choix[1]

                monde.grille[choix[0]][choix[1]] = self
                monde.grille[preced_y][preced_x] = "  "
        
    def vivre_une_journee(self, monde):
        """
        Fonction qui fait se deplacer et actualise l'energie du Requin
        : param monde (list) :  Emplacement des entitées
        """
        self.se_deplacer(monde, self.deplacement_possible(monde))
        self.energie -= 1
        if self.energie == 0:
            monde.grille[self.y][self.x] = "  "
        elif self.energie > 10:
            self.energie = 10
        self.reproduction += 1

monde = Monde(300, 300)

monde.peupler(700, 500)

# Fenetre Tkinter
fenetre = Tk()

# Afficher canva
canvas = Canvas(fenetre, width=monde.largeur, height=monde.hauteur, background=color_water)
canvas.pack()

# Passe un tour et actualise le canva
while True:
    monde.jouer_un_tour()
    #time.sleep(1)
    canvas.update_idletasks()
    fenetre.update()
    print("Mise à jour du canvas")