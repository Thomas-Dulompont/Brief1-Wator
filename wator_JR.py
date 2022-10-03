from random import randint, choice
from time import sleep
import os

class Monde:
    def __init__(self, hauteur, largeur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[ "  " for _ in range(largeur)] for _ in range(hauteur)]
    
    
    def afficher_monde(self):
        for ligne in self.grille:
            for case in ligne:
                if isinstance(case,Poisson):
                    print("🐠", end = " | " )
                elif isinstance (case,Requin):
                    print ( "🦈", end =" | ")
                else:
                    print("  ",end=" | ")
            print ("\n")




    def peupler (self, nb_poisson, nb_requin):
        max_poisson = 0
        max_requin = 0

        if nb_poisson + nb_requin > self.hauteur * self.largeur:
            return ValueError("Merci de rentrer un nombre plus petit")

        while max_poisson < nb_poisson:
            x_rand = randint(0,self.largeur-1)
            y_rand = randint(0,self.hauteur-1)

            if self.grille [y_rand][x_rand]== "  ":
                self.grille[y_rand][x_rand] = Poisson (y_rand, x_rand)
                max_poisson += 1
        
        
        
        while max_requin < nb_requin:
            x_rand = randint(0,self.largeur-1)
            y_rand = randint(0,self.hauteur-1)

            if self.grille [y_rand][x_rand]== "  ":
                self.grille[y_rand][x_rand] = Requin (y_rand, x_rand)
                max_requin += 1
    
   
    def jouer_un_tour(self):
        
        self.poissons = []
        self.requins = []

        for ligne in self.grille:
            for case in ligne:
                if isinstance (case,Poisson):
                    self.poissons.append (case)

        for poisson in self.poissons:
            poisson.vivre_une_journee (self)

        for ligne in self.grille:
            for case in ligne:
                if isinstance (case, Requin):
                    self.requins.append (case)

        for requin in self.requins:
            requin.vivre_une_journee(self)

        self.afficher_monde()
        



class Poisson:
   
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.compteur_repro = 0


    def deplacement_possible(self, monde):
        
        coup_possibles = []
        
        if monde.grille[(self.y-1)% monde.hauteur][self.x]== "  " :
            coup_possibles.append(((self.y-1)% monde.hauteur , self.x))
        
        if monde.grille[(self.y+1)% monde.hauteur][self.x]== "  ":
            coup_possibles.append(((self.y+1)% monde.hauteur , self.x))

        if monde.grille [self.y][(self.x+1) % monde.largeur]== "  ":
            coup_possibles.append((self.y , (self.x + 1) % monde.largeur))

        if monde.grille [self.y][(self.x-1) % monde.largeur]=="  ":
            coup_possibles.append((self.y , (self.x-1) % monde.largeur))

        return coup_possibles



    
    def se_deplacer(self, monde):
        
        coups_possibles=self.deplacement_possible(monde)
        if len (coups_possibles)!=0:
            if coups_possibles!=[]:
                coup_a_jouer = choice (coups_possibles)
                x_coup=coup_a_jouer[ 1 ]
                y_coup=coup_a_jouer[ 0 ]

                x_preced=self.x
                y_preced=self.y

                self.x = x_coup
                self.y = y_coup
                monde.grille[y_coup][x_coup]=self
        
                if self.compteur_repro >= 5:
                    monde.grille[y_preced][x_preced]= Poisson (y_preced, x_preced)
                    self.compteur_repro=0
                else: 
                    monde.grille [y_preced][x_preced]= "  "

        
        
    def vivre_une_journee(self, monde):
        self.compteur_repro +=1
        self.se_deplacer (monde)
        
    
        
class Requin:
    
    def __init__(self,y,x):
        self.x = x
        self.y = y
        self.compteur_repro = 0
        self.energie= 5

        
     
    
   
    def deplacement_possible (self,monde): 
        deplacements=[]

        if isinstance (monde.grille[(self.y+1) % monde.hauteur-1][self.x],Poisson):
            deplacements.append(((self.y+1) % monde.hauteur, self.x))
            return deplacements
        elif isinstance (monde.grille[(self.y-1) % monde.hauteur-1][self.x], Poisson):
            deplacements.append(((self.y-1) % monde.hauteur, self.x))
            return deplacements
        elif isinstance (monde.grille[self.y][(self.x+1) % monde.largeur],Poisson):
            deplacements.append((self.y, (self.x+1) % monde.largeur))
            return deplacements
        elif isinstance (monde.grille[self.y][(self.x-1)% monde.largeur],Poisson):
            deplacements.append((self.y, (self.x-1) % monde.largeur))
            return deplacements
            
        else:
            if monde.grille [(self.y+1) % monde.hauteur][self.x] == "  ":
                deplacements.append (((self.y+1) % monde.hauteur, self.x))

            if monde.grille [(self.y-1 ) % monde.hauteur][self.x] == "  ":
                deplacements.append(((self.y-1) % monde.hauteur, self.x ))

            if monde.grille [self.y][(self.x+1) % monde.largeur] == "  ":
                deplacements.append((self.y,(self.x+1)% monde.largeur ))
        
            if monde.grille [self.y][(self.x-1) % monde.largeur] == "  ":
                deplacements.append (( self.y , (self.x-1) % monde.largeur))
            
            return deplacements


    def se_deplacer (self, monde ,deplacements):
        preced_y = self.y
        preced_x = self.x
        if self.energie ==0:
            monde.grille [self.y][self.x] = "  "
        elif deplacements !=[]:
            choix = choice(deplacements)
            if isinstance(monde.grille[choix[0]][choix[1]], Poisson):
                if self.compteur_repro >=4:
                    self.y = choix [0]
                    self.x = choix [1]

                    monde.grille[preced_y][preced_x] = Requin (preced_y , preced_x)

                    monde.grille [choix[0]][choix[1]] = self
                    self.compteur_repro = 0
                
                else:
                
                    self.y = choix [0]
                    self.x = choix [1]

                    monde.grille [choix[0]] [choix[1]] = self
                    monde.grille [preced_y] [preced_x] = "  "

                self.energie +=1

            elif self.compteur_repro >=10:
                self.y = choix [0]
                self.y = choix [1]

                monde.grille [preced_y][preced_x] = Requin (preced_y, preced_x)

                monde.grille [choix[0]][choix[1]] = self
                self.compteur_repro=0
            else:
                self.y = choix [0]
                self.x = choix [1]

                monde.grille[choix[0]][choix[1]] = self
                monde.grille[preced_y][preced_x] = "  "

        
    
    def vivre_une_journee (self,monde):
        self.se_deplacer(monde ,self.deplacement_possible(monde))
        self.energie -= 1
        
        if self.energie==0:
            monde.grille[self.y][self.x] = "  "
        elif self.energie > 10:
            self.energie =10
        self.compteur_repro +=1

monde=Monde(10, 8)
monde.peupler(10,10)
monde.afficher_monde()

for _ in range (50):
     print("----------------------------------------------------------")
     monde.jouer_un_tour()