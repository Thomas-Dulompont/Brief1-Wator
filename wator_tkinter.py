from tkinter import * 
from random import randint, choice
import time
import os

fenetre = Tk()

color_water = "#000643"

def lancer_simulation(duree):
    for _ in range(duree):
        #time.sleep(2)
        monde.jouer_un_tour()
        canvas.update_idletasks()

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
        for ligne in self.grille:
            for case in ligne:
                x_current = self.grille.index(ligne)
                y_current = self.grille[self.grille.index(ligne)].index(case)
                if isinstance(case,Poisson):
                    canvas.create_rectangle(x_current + 3, y_current + 3, x_current + 3, y_current + 3,outline="#fb0",fill="#fb0")
                elif isinstance(case,Requin):
                    canvas.create_rectangle(x_current + 3, y_current + 3, x_current + 3, y_current + 3,outline="#00d600",fill="#00d600")
                else:
                    canvas.create_rectangle(x_current + 3, y_current + 3, x_current + 3, y_current + 3,outline=color_water,fill=color_water)

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
        self.se_deplacer(monde, self.deplacement_possible(monde))
        self.reproduction += 1

class Requin:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.reproduction = 0
        self.energie = 6
    
    def deplacement_possible(self, monde):
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
                self.energie += 1
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
        self.se_deplacer(monde, self.deplacement_possible(monde))
        self.energie -= 1
        if self.energie == 0:
            monde.grille[self.y][self.x] = "  "
        elif self.energie > 10:
            self.energie = 10
        self.reproduction += 1

monde = Monde(500, 500)

canvas = Canvas(fenetre, width=monde.largeur, height=monde.hauteur, background=color_water)
canvas.pack()

monde.peupler(100, 100)

button= Button(fenetre, text="Lancer",command=lambda:lancer_simulation(10))
button.pack()

fenetre.mainloop()