
from cmath import isinf
from pyexpat.model import XML_CQUANT_OPT
from random import randint, choice
from re import X
from time import sleep
import os

class Monde:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
<<<<<<< HEAD
        self.grille = [[ " " for _ in range(largeur)] for _ in range(hauteur)]
    
    
    def afficher_monde(self):
        
        for ligne in self.grille:
            for case in ligne:
                if isinstance(case,Poisson):
                    print(" 🐠 ", end = " | " )
                elif isinstance (case,Requin):
                    print ( "🦈 ", end =" | ")
                else:
                    print(" ",end=" | ")
            print ("\n")




    def peupler (self, nb_poisson, nb_requin):
        
        for i in range (nb_poisson):
            x_rand = randint(0,self.largeur-1)
            y_rand = randint(0,self.hauteur-1)
         
            while self.grille [y_rand][x_rand]== " ":
                x_rand =randint(0, self.largeur - 1)
                y_rand =randint(0, self.hauteur - 1)
        self.grille[y_rand][x_rand] = Poisson (x_rand, y_rand)
        
        
        
        for i in range (nb_requin):
            x_rand = randint(0,self.largeur-1)
            y_rand = randint(0,self.hauteur-1)
             
            while self.grille [y_rand][x_rand]== " ":
                x_rand =randint(0, self.largeur - 1)
                y_rand =randint(0, self.hauteur - 1)
        self.grille [y_rand][x_rand]= Requin (x_rand, y_rand)
=======
        self.grille = [[ "  " for _ in range(largeur)] for _ in range(hauteur)]
        self.poissons = []
        self.requins = []
    
    def afficher_monde(self):
        """
        Fonction qui affiche le monde dans la console.
        """
        for ligne in self.grille:
            for case in ligne:
                if isinstance(case,Poisson):
                    print("🐠", end=" | ")
                elif isinstance(case,Requin):
                    print("🦈", end=" | ")
                else:
                    print("  ", end=" | ")
            print("\n")


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

>>>>>>> 0f068797cd47dc2ac177ab9a9c90049e4427ff5a
    
   
    def jouer_un_tour(self):
<<<<<<< HEAD
        
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
            requin. vivre_une_journee (self)

        self.afficher_monde
        





class Poisson:
   
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.compteur_repro = 0


    def deplacement_possible(self, monde):
        
        coup_possibles = []
        
        if monde.grille[(self.y-1)% monde.hauteur][self.x]== " " :
            coup_possibles.append((self.x,(self.y-1))% monde.hauteur)
        
        if monde.grille[(self.y+1)% monde.hauteur][self.x]== " ":
            coup_possibles.append((self.x,(self.y+1))% monde.hauteur)

        if monde.grille [self.y][(self.x+1) % monde.largeur]== " ":
            coup_possibles.append(((self.x + 1) % monde.largeur, self.y))

        if monde.grille [self.y][(self.x-1) % monde.largeur]==" ":
            coup_possibles.append(((self.x-1) % monde.largeur, self.y))

        return coup_possibles



    
    def se_deplacer(self, monde):
        
        coups_possibles=self.deplacement_possible(monde)
        if len (coups_possibles)!=0:
            if coups_possibles!=[]:
                coup_a_jouer = choice (coups_possibles)
                x_coup=coup_a_jouer[ 0 ]
                y_coup=coup_a_jouer[ 1 ]

                x_preced=self.x
                y_preced=self.y

                self.x = x_coup
                self.y = y_coup
                monde.grille[y_coup][x_coup]=self
        
                if self.compteur_repro >= 5:
                    monde.grille[y_preced][x_preced]= Poisson (x_preced, y_preced)
                    self.compteur_repro=0
                else: 
                    monde.grille [y_preced][x_preced]= " "

        
        
    def vivre_une_journee(self, monde):
        self.compteur_repro +=1
        self.se_deplacer (monde)
        
    
        
class Requin:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.compteur_repro = 0
        self.energie= 5

        
     
    
    
    
    def deplacement_possible (self,monde): 
        
     deplacements=[]
        
     if isinstance (monde.grille[(self.y+1)% monde.hauteur][self.x],Poisson):
        deplacements.append (((self.y+1)% monde.hauteur, self.x))
        return deplacements
   
     elif isinstance (monde.grille[(self.y-1) % monde.hauteur][self.x], Poisson):
        deplacements.append (((self.y-1) % monde.hauteur, self.x))
        return deplacements
     elif isinstance (monde.grille [self.y],[(self.y+1) % monde.largeur],Poisson):
         deplacements.append[(self.y (self.x+1) % monde.largeur)]
         return deplacements
     elif isinstance (monde.grille[self.y][(self.x-1)% monde.largeur],Poisson):
        deplacements.append [(self.y,(self.x-1)% monde.largeur)]
        return deplacements
        
     else:
           
      if monde.grille [(self.y+1)% monde.hauteur][self.x] == " ":
            deplacements.append (((self.y+1) % monde.hauteur, self.x))

     if monde.grille [(self.y-1 ) % monde.hauteur][self.x] == " ":
            deplacements.append (((self-1) % monde.hauteur, self.x ))

     if monde.grille [self.y][(self.x+1) % monde.largeur] == " ":
            deplacements.append((self.y,(self.x+1)% monde.largeur ))
 
     if monde.grille [self.y][(self.x-1) % monde.largeur] == " ":
            deplacements.append (( self.y , (self.x-1) % monde.largeur))
        
            return deplacements
        


        



    def se_deplacer (self, monde ,deplacements):
        preced_y = self.y
        preced_x = self.x
        if self.energie ==0:
            monde.grille [self.y][self.x] = " "
        elif deplacements !=[]:
            choix = choice (deplacements)

        if isinstance (monde.grille[choix[0]][choix[1]], Poisson):
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
                monde.grille [preced_y] [preced_x] = " "

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
            monde.grille[preced_y][preced_x] = " "

        
    
    def vivre_une_journee (self,monde):
        
        self.se_deplacer (monde ,self.deplacement_possible (monde))
        self.compteur_repro +=1
        self.energie > 0
        if self.energie==0:
            monde.grille[self.y][self.x] = " "
        elif self.energie > 10:
            self.energie =10
        self.compteur_repro +=1

monde=Monde(10,8)
monde.peupler(10,10)
monde.afficher_monde()

for _ in range (50):
    print("----------------------------------------------------------")
    monde.jouer_un_tour()
=======
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

monde = Monde(10, 8)
monde.peupler(10, 10)
monde.afficher_monde()
for _ in range(50):
    print("-------------------------------------------------")
    monde.jouer_un_tour()
>>>>>>> 0f068797cd47dc2ac177ab9a9c90049e4427ff5a
