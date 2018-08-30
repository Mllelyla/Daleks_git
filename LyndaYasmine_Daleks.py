## -*- coding:utf-8 -*-
#!/usr/bin/env python

##############################################
#### par Lynda Lavoie et Yasmine Kaddouri ####
##############################################

import random
import os

class Dalek():
    def __init__(self,x,y):
        self.x = x
        self.y = y


    def deplacement(self,posDocteur):
        self.doc = posDocteur    
        if self.x > self.doc[0]:
            self.x = self.x - 1
        if self.x < self.doc[0]:
            self.x = self.x + 1
        if self.y > self.doc[1]:
            self.y = self.y - 1
        if self.y < self.doc[1]:
            self.y = self.y + 1
            
    def crash(self,daleks):
        morts = []
        self.daleks=daleks

        for i in self.daleks:
            for j in self.daleks:
                if (i.x == j.x) and (i.y == j.y):
                    self.parent.morts.append(i)
            for i in self.parent.morts : 
                self.daleks.remove(i)
            return morts

class Ferraille():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Docteur():
    def __init__(self,parent,x,y,difficulte,dimx,dimy):
        self.parent = parent
        self.largeur = dimx
        self.hauteur = dimy
        self.x = x
        self.y = y
        self.posDocteur =[x,y]
        self.etatDocteur = True;
        self.actionDoc = None
        self.nbZap = 1
        self.optionDifficulte = difficulte
        
    def action(self, inputDoc):
        self.actionDoc = inputDoc
        
        if self.actionDoc == 'Z':
            self.zapper()
            
        elif self.actionDoc == 'T':
            self.teleport()
            
        elif self.actionDoc == 'E':
            self.attireDaleks()
            
        else:
            self.posDocteur =self.deplacementDocteur(inputDoc)
        return self.posDocteur

    def deplacementDocteur(self, inputDoc):
        nouvelX = self.posDocteur[0] + inputDoc[0] 
        nouvelY = self.posDocteur[1] + inputDoc[1]
        self.x = nouvelX
        self.y = nouvelY
        self.posDocteur[0]= nouvelX 
        self.posDocteur[1]= nouvelY 
        return self.posDocteur

    def teleport(self):
        if self.optionDifficulte == '1' or '2' or '3':
            self.x = random.randrange(self.largeur)
            self.y = random.randrange(self.hauteur)
            self.posDocteur[0]= self.x 
            self.posDocteur[1]= self.y
                    
    def zapper(self):
        if self.nbZap > 0:
            self.nbZap-=1
            print("ZAP!")
        else:
            print("Oups plus de ZAP")


    def attireDaleks(self):
        #pas le temps de coder
        print("Attire Daleks - ITS A TRAP")
        return True


class Jeu():
    def __init__(self,dimx,dimy):
        self.dimx = dimx
        self.dimy = dimy

        self.airedejeu = self.prepareJeu()
        
        self.inputDoc = []

    def prepareJeu(self):
        Aire = []
        for i in range(self.dimy):
            Ligne = []
            for j in range(self.dimx):
                Ligne.append(" . ")
            Aire.append(Ligne)
        return Aire


    def finirPartie(self,partieFinie):
        self.partieFinie = partieFinie
        if self.partieFinie == True:
            self.partie.partieFinie =True

    
    
    def commencerPartie(self, optionDifficulte):
        self.partie =  PartieCourante(self,optionDifficulte)
        self.partie.nouveauNiveau()
                   
    def quitter(self):
        exit(0)

    
class PartieCourante():
    def __init__(self,parent,optionDifficulte):
        self.parent=parent
        self.niveauFini = False
        self.partieFinie = False
        self.optionDifficulte =optionDifficulte

        self.listeDaleks=[]
        self.listeTas = []
        self.posDocteur =None
        self.disparus=None
        self.player=None

        self.nbDaleks = 5
        self.niveau = 1
        self.points = 0
        self.nbZap = 1
        self.nbPointsDalekMort = 5

        self.symboleDalek =" X "
        self.symboleDoc = " @ "
        self.symboleTas = " ! "

        self.inputDoc = self.parent.inputDoc

    def nouveauNiveau(self):
        self.genererDaleks()
        self.posDocteur = self.genererDocteur()
        
    def genererDaleks(self):
        nbDaleksNiveau = self.nbDaleks*self.niveau
        posDaleks = []

        for i in range(nbDaleksNiveau):
            x = random.randrange(self.parent.dimx)
            y = random.randrange(self.parent.dimy)
            DalekCourant = Dalek(x,y)
            self.listeDaleks.append(DalekCourant)
            self.parent.airedejeu[DalekCourant.y][DalekCourant.x] = self.symboleDalek

    def genererDocteur(self):
        dimx = self.parent.dimx
        dimy = self.parent.dimy
        
        x = random.randrange(dimx)
        y = random.randrange(dimy)
        
        self.player = Docteur(self,x,y,self.optionDifficulte,dimx,dimy)
        self.posDocteur = [x,y]
        self.parent.airedejeu[y][x] = self.symboleDoc
        return self.posDocteur

    def genererFerraille(self):
        for i in self.morts:
            self.listeTas.append(Ferraille(i[0],i[1]))
            
        
    def actionsDocteur(self,inputDoc):
        self.inputDoc = inputDoc
        self.player.etatDocteur = self.docteurMort(self.posDocteur,self.listeDaleks)
        self.parent.finirPartie( self.player.etatDocteur)
        
        self.posDocteur = self.player.action(inputDoc)
        
    def docteurMort(self,posDocteur,listeDaleks):
        doc = posDocteur
        for i in listeDaleks:
            if i.x == doc[0] and i.y == doc[1]:
                return True

            
    def actionsDaleks(self):
        self.player.etatDocteur = self.docteurMort(self.posDocteur,self.listeDaleks)
        self.parent.finirPartie( self.player.etatDocteur)
        
        doc = self.player.posDocteur
        for dalek in self.listeDaleks:
            
            dalek.deplacement(self.player.posDocteur)

                
                
    def collisionDaleks(self):
        self.disparus = []
        for i in self.listeDaleks:
            if i.crash() == True:
                self.points += self.nbPointsDalekMort
                d=disparus.append(i)
        if len(disparus) > 0:
            for tas in disparus:
                self.daleks.remove(tas)
           
    def rafraichirNiveau(self):
        
        self.parent.airedejeu=self.parent.prepareJeu()
        
        for i in self.listeDaleks:
            self.parent.airedejeu[i.y][i.x] = self.symboleDalek
        for i in self.listeTas:
            self.parent.airedejeu[i.y][i.x] = self.symboleTas
            
        self.parent.airedejeu[self.player.y][self.player.x] = self.symboleDoc
        
     
class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.inputDoc = None
        self.optionDifficulte = None
        self.commencerPartie = None

    def afficherMenu(self):
        self.commencerPartie = False
        os.system('cls')
        print("            JEU DE DALEKS !!")
        print("==========================================")
        print("=        1: Commencer une partie         =")             
        print("=                                        =")
        print("=        2: Tableau de Pointage          =")
        print("=                                        =")
        print("=        3: Quitter                      =")
        print("=                                        =")
        print("==========================================")

        optionMenu = input("Choisissez une option : ")
        if optionMenu == '1':
            self.parent.optionDifficulte = self.choisirDifficulte()
        elif optionMenu == '2':
            self.afficherPointage()
        elif optionMenu == '3':
            exit()
        else:
            print("option non disponible")
        
    
    def choisirDifficulte(self):
        os.system('cls')
        print("==========================================")
        print("=         Niveau de Difficult�           =")
        print("=                                        =")
        print("=         1: Facile                      =")
        print("=         2: Ordinaire                   =")
        print("=         3: Difficile                   =")
        print("=         4: Retour au menu precedent    =")
        print("=                                        =")
        print("==========================================")
        
        option = input("Choisissez une option : ")
        if option == '1' or option == '2' or option == '3':
            self.commencerPartie = True
            self.espace()
            return option
        elif option == '4':
            self.afficherMenu()
        else:
            print("option non disponible, recommencez")
            self.espace()
            self.choisirDifficulte()
            

    def printAire(self,aire):
        os.system('cls')
        print("==========================================")
        print("=  CONTROLES (NumPad):                   =")             
        print("=        1-8 : D�placement                           =")
        print("=         5  : Attendre un tour          =")
        print("=          / : T�l�portation             =")
        print("=          * : Zappeur                   =")
        print("=          0 : Attirer les Daleks        =")
        print("=                                        =")
        print("                                         =")
        print("=           Symbole Dalek = X            -")
        print("=           Symbole Doc = @              =")
        print("=           Symbole Feraille = !         =")
        print("==========================================")
        
        print("Niveau = ",self.parent.modele.partie.niveau)
        print("Nombre Daleks = ",self.parent.modele.partie.nbDaleks)
        print("Nombre de Zaps = ",self.parent.modele.partie.nbZap)
        print("Score = ",self.parent.modele.partie.points)
        print("======================================")
        for i in aire:
            print(*i)
        
        print("======================================")
            
    def inputDocteur(self):
        self.positionPresente = self.parent.modele.partie.posDocteur
        HAUT = [0,-1]
        BAS = [0,1]
        GAUCHE = [-1,0]
        DROITE = [1,0]
        HD = [1,-1]
        HG = [-1,-1]
        BD = [1,1]
        BG = [-1,1]
        WAIT = [0,0]
        TELEPORT = 'T'
        ZAP = 'Z'
        END = 'E'
        
        keys={'8':HAUT,'2':BAS,'4':GAUCHE,'6':DROITE,
                '9':HD,'7':HG,'1':BG,'3':BD,
                '5':WAIT,'/':TELEPORT,'*':ZAP,'0':END}    
        
        print("Position Pr�sente :",self.positionPresente)
        valide = False
        while not valide:
            touche = input("Action du Docteur  :")
            if touche in keys:
                self.inputDoc = keys[touche]
                valide = True
            else:
                print("Action non valide") 
        return self.inputDoc 
           
            
          
    def deplacementValide(self, action, positionPresente):
        self.positionPresente = positionPresente
        listeExceptions =['T','Z','E']
        if action not in listeExceptions:
            self.nouvelX =  self.positionPresente[0] + action[0]
            self.nouvelY = self.positionPresente[1] + action[1]
            
            if self.nouvelX >= 0 or self.nouvelX < self.parent.modele.dimx:
                return True
            if self.nouvelY >= 0 or self.nouvelY < self.parent.modele.dimy:
                return True
            for i in self.parent.modele.partie.listeTas:
                if i.x != self.nouvelX and i.y != self.nouvelY:
                    return True
            
    def afficherPointage(self):
        os.system('cls')
        self.espace()
        print("==========================================")
        print("=         Tableau de Pointage            =")             
        print("=                                        =")
        print("=                                        =")
        print("= pas de fichier pointage encore !       =")
        print("=                                        =")
        print("=                                        =")
        print("==========================================")        
        touche = input("Pressez un touche pour continuer")
        self.espace()
        self.afficherMenu()
        
    def afficherFinPartie(self):
        os.system('cls')
        self.espace()
        print("==========================================")
        print("=         Vous etes Morts!               =")             
        print("=                                        =")
        print("=                                        =")
        print("=                                        =")
        print("=                                        =")
        print("=                                        =")
        print("==========================================")        
        touche = input("Pressez un touche pour quitter")
        self.espace()  
        
    def espace(self):
        for i in range(5):
            print("")
             
class Controleur():
    def __init__(self):
        self.modele=Jeu(10,10) 
        self.vue=Vue(self)

    def menu(self):
        c.vue.afficherMenu()
        if c.vue.commencerPartie == True:
            c.modele.commencerPartie(c.vue.optionDifficulte)
            self.jeu()
        else:
            self.menu()

    def jeu(self):
        c.vue.printAire(c.modele.airedejeu)

        while c.modele.partie.partieFinie == False:       
            #tour du Docteur
            input=c.vue.inputDocteur()
            c.modele.partie.actionsDocteur(input)
            c.modele.partie.rafraichirNiveau()
            
            #tour des Daleks
            c.modele.partie.actionsDaleks()
            c.modele.partie.rafraichirNiveau()
            c.vue.printAire(c.modele.airedejeu)
            
            self.jeu()
        c.vue.afficherFinPartie()
        c.modele.quitter()
        
        


if __name__ == '__main__':
    c = Controleur()
    c.menu()








