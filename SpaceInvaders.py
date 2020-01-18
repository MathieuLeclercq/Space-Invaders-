# -*- coding: utf-8 -*-
import tkinter as tk
import random as rd

class Ennemi:
    def __init__(self, canvas, jeu, Horde, positionx=6, positiony=1, direction = 1, vitesse = 2, frequence = 16, kind=2):
        self.kind = kind
        self.canvas = canvas
        self.positionx = positionx
        self.setimage = [tk.PhotoImage(file='mechant.png'),tk.PhotoImage(file='mechant2.png'),tk.PhotoImage(file='mechant1.png'),tk.PhotoImage(file='mechant22.png')] #50px*50px
        self.positiony= positiony # Pourrait être utile. Position dans la grille de la horde
        self.sprite= canvas.create_image(50*positionx,50*positiony+50,image=self.setimage[kind-1], anchor='nw')
        self.direction = direction # utile pour les solitaires hors hordes qui donnent des bonus
        self.image=self.setimage[kind-1]
        self.Horde = Horde
        self.vitesse = vitesse
        self.frequence = frequence
        self.jeu = jeu
        self.score = 50*kind**2
        self.pv = kind
        if self.pv == 3:
            self.pv = 1
            # C'est le boss

    def deplacementboss(self):
        if self.jeu.GameOver:
            return
        # Deplacement pour les solitaires persistant sur une ligne et qui n'avancent pas (boss ?). Se manipule en dehors des hordes. Pas implémenté (suffit de créer l'objet de type Ennemi et lancer cette fonction apres un certain nombre de manche)
        if self.canvas.coords(self.sprite)[0] + self.direction*self.vitesse > 0 and self.canvas.coords(self.sprite)[0] + self.direction*self.vitesse + 50 < 600:
            self.canvas.move(self.sprite, self.direction*self.vitesse, 0)
        else:
            self.direction = (self.direction == -1) - (self.direction == 1)
            self.canvas.move(self.sprite, self.direction*self.vitesse, 0)
        self.canvas.after(self.frequence,self.deplacement)

    def deplacementsurprise(self):
        if self.jeu.GameOver:
            return
        # Deplacement pour les solitaires surprises qui apparaitrait à intervalle regulier mais pas toujours. Se manipule en dehors des hordes. Pas implémenté (suffit de créer l'objet de type Ennemi et lancer cette fonction apres un after)
        if self.canvas.coords(self.sprite)[0] + self.direction*self.vitesse > 0 and self.canvas.coords(self.sprite)[0] + self.direction*self.vitesse + 50 < 650:
            self.canvas.move(self.sprite, self.direction*self.vitesse, 0)
        else:
            self.canvas.destroy(self.sprite)
        self.canvas.after(self.frequence,self.deplacement)

class Horde:
    def __init__(self,canvas, jeu, length, heigth, vitesse = 1, direction = 1, frequence = 16):
        self.listeEnnemis = []
        self.length = length
        self.heigth = heigth
        self.setimage = [tk.PhotoImage(file='mechant.png')] #50px*50px
        self.canvas = canvas
        self.jeu = jeu
        self.vitesse = vitesse
        self.direction = direction
        self.frequence = frequence
        
        
        for i in range(length):
            for j in range(heigth-1):
                self.listeEnnemis.append(Ennemi(canvas, jeu, self, i+(12-length)//2, j, self.direction, self.vitesse, self.frequence, 2))
            self.listeEnnemis.append(Ennemi(canvas, jeu, self, i+(12-length)//2, heigth-1, self.direction, self.vitesse, self.frequence, 1))
    def deplacements(self):
        if self.jeu.GameOver or self.jeu.transition:
            return
        deplacementOK=True
        for Ennemi in self.listeEnnemis:
            if self.canvas.coords(Ennemi.sprite)[0] + self.direction*self.vitesse < 0 or self.canvas.coords(Ennemi.sprite)[0] + self.direction*self.vitesse + 50 > 600:
                deplacementOK = False
        if deplacementOK:
            for Ennemi in self.listeEnnemis:
                self.canvas.move(Ennemi.sprite, self.direction*self.vitesse, 0)
        else:
            for Ennemi in self.listeEnnemis:
                if self.canvas.coords(Ennemi.sprite)[1] + 50 + 25 > 490:
                    self.jeu.GameOver = True
            if self.jeu.GameOver:
                self.canvas.after(16, self.jeu.endGame)
                return

            for Ennemi in self.listeEnnemis:
                self.canvas.move(Ennemi.sprite, 0, 25)
                Ennemi.direction = (Ennemi.direction == -1) - (Ennemi.direction == 1) # Pas utilisé dans horde mais fait par rigueur
            self.direction = (self.direction == -1) - (self.direction == 1)
        self.canvas.after(self.frequence,self.deplacements)
    
    def NouveauTir(self):
        if self.jeu.GameOver or self.jeu.transition:
            return
        for Ennemi in self.listeEnnemis:
            probatir = rd.randint(0,5000)
            if probatir <= 1:
                self.jeu.Tirsactuels.append(Tir(self.canvas, self.jeu, self.canvas.coords(Ennemi.sprite)[0], self.canvas.coords(Ennemi.sprite)[1], 1))
        self.canvas.after(16, self.NouveauTir)
                
                
            
class Tir:
    def __init__(self, canvas, jeu, positionx, positiony, direction):
        self.image = [tk.PhotoImage(file='laser.png'), tk.PhotoImage(file='laser2.png')]
        self.canvas= canvas
        self.jeu = jeu
        self.direction = direction
        self.sprite = canvas.create_image(positionx,positiony+direction*30,image=self.image[(self.direction == -1)], anchor='nw')



class Player:
    def __init__(self, canvas, jeu, positionx=275, positiony=550):
        # canvas = canvas peut etre problematique
        self.canvas = canvas
        self.image = tk.PhotoImage(file='player.png').subsample(10,10) #50px*50px
        self.sprite= canvas.create_image(positionx,positiony,image=self.image, anchor='nw')
        self.direction = 0
        self.jeu = jeu
        self.TimerTir = 1000
        self.tir = False

    def moveleft(self, event):
        if self.jeu.GameOver:
            return
        self.direction=-1

    def moveright(self, event):
        if self.jeu.GameOver:
            return
        self.direction=1

    def stopmove(self, event):
        if self.jeu.GameOver:
            return
        if (event.keysym == "q" and self.direction == -1) or (event.keysym == "d" and self.direction == 1):
            self.direction = 0
        if (event.keysym == "space" and self.tir == 1):
            self.tir = False
    def deplacementplayer(self):
        if self.jeu.GameOver:
            return
        if (self.canvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.canvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0
        else:
            self.canvas.move(self.sprite, self.direction*5,0)
        self.canvas.after(16,self.deplacementplayer)
        
        if self.tir == True and self.TimerTir >= 25 and not(self.jeu.transition):
            self.jeu.Tirsactuels.append(Tir(self.canvas, self.jeu, self.canvas.coords(self.sprite)[0], self.canvas.coords(self.sprite)[1], -1))
            self.TimerTir = 0

    def NouveauTirP(self, event):
        if self.jeu.GameOver:
            return
        if self.TimerTir >= 25:
            self.tir = True  
    
    def PasdeTir(self):
        if self.jeu.GameOver:
            return
        self.TimerTir += 1

        self.canvas.after(16, self.PasdeTir)


class Menu:
    def __init__(self):
        self.background = tk.PhotoImage(file = 'backgroundMenu.png')
        self.logo =  tk.PhotoImage(file = 'logo.png')



class Jeu:
    def __init__(self, fenetre, length, heigth, vitesse = 1):
        # A ameliorer pour configurer depuis la declaration d'un objet jeu
        self.fenetre = fenetre
        self.fenetre.title('Space Invaders')
        self.fenetre.geometry("600x600")
        self.fenetre.resizable(width=False, height=False)

        self.canvas = tk.Canvas(self.fenetre, bg = 'black', bd= 0, highlightthickness=0, height = 600, width = 600)

        self.player = Player(self.canvas, self)

        self.length = length
        self.heigth = heigth
        self.vitesse = vitesse # Ces 3 pour manches suivantes, incrémentés

        self.horde = Horde(self.canvas, self, self.length, self.heigth, self.vitesse)
        self.murs = Murs(self.canvas,self)
        self.GameOver = False
        self.Tirsactuels = []

        self.menu = Menu()
        self.boutonPlay = tk.Button(self.fenetre, text = 'PLAY !',height = 4, width = 20,command=self.Debut,activebackground='#ffbd33',background='#FFE213')
        self.boutonExit = tk.Button(self.fenetre, text = 'EXIT',height = 2, width = 10,command=self.fenetre.destroy,activebackground='#ffbd33',background='#FFE213')

        self.transition = False

        self.score = 0

        temp = open("highscore.txt", "rt")
        self.highscore = int(temp.readline())
        temp.close()


    def lancerMenu(self):
        self.canvas.pack(anchor='nw')
        self.affBackground = self.canvas.create_image(300,300,image=self.menu.background)
        self.affLogo = self.canvas.create_image(300,133,image=self.menu.logo)        
        self.affBoutonPLay =self.canvas.create_window(300,350,window = self.boutonPlay)        
        self.affBoutonExit = self.canvas.create_window(300,450,window = self.boutonExit)
    
    def Debut(self):
        self.canvas.delete(self.affBoutonPLay,self.affBoutonExit,self.affBackground,self.affLogo)
        self.canvas.pack(anchor='nw')
        self.canvas.after(16, self.horde.deplacements)
        self.canvas.after(16, self.player.deplacementplayer)
        self.canvas.after(16, self.GestionTirs)
        self.canvas.after(16, self.horde.NouveauTir)       
        self.canvas.after(16, self.player.PasdeTir)
        self.fenetre.bind('<q>', self.player.moveleft)
        self.fenetre.bind('<Q>', self.player.moveleft)
        self.fenetre.bind('<d>', self.player.moveright)
        self.fenetre.bind('<D>', self.player.moveright)
        self.fenetre.bind('<KeyRelease>', self.player.stopmove)
        self.fenetre.bind('<space>', self.player.NouveauTirP)
        
    def newmanche(self):
        self.vitesse += 1

        self.horde = Horde(self.canvas, self, self.length, self.heigth, self.vitesse)
        self.transition = False
        self.canvas.after(16, self.horde.deplacements)
        self.canvas.after(16, self.horde.NouveauTir)
        self.canvas.after(16, self.GestionTirs)
    def endGame(self):
        self.canvas.delete('all')
        label = tk.Label(self.canvas, text='GAME OVER', fg='white', bg='black')
        label.config(font=("Liberation", 30))
        labelc = self.canvas.create_window(300, 300, window=label)
        self.affBackground = self.canvas.create_image(300,300,image=self.menu.background)
        
        if self.score > self.highscore:
            temp = open("highscore.txt", "wt")
            temp.write(str(self.score))
            temp.close()
        
        self.canvas.after(500, self.relaunch)
        
    def relaunch(self):
        self.canvas.delete('all')
        self.vitesse = 1
        self.player = Player(self.canvas, self)
        self.horde = Horde(self.canvas, self, self.length, self.heigth, self.vitesse)
        self.murs = Murs(self.canvas,self)
        self.GameOver = False
        self.Tirsactuels = []

        self.menu = Menu()
        self.boutonPlay = tk.Button(self.fenetre, text = 'PLAY !',height = 4, width = 20,command=self.Debut,activebackground='#ffbd33',background='#FFE213')
        self.boutonExit = tk.Button(self.fenetre, text = 'EXIT',height = 2, width = 10,command=self.fenetre.destroy,activebackground='#ffbd33',background='#FFE213')
        jeu.lancerMenu()

    def GestionTirs(self):
        if self.GameOver:
            return
        for tir in self.Tirsactuels:
            touche = False
            indexEnnemiasuppr = None 
            indexblocasuppr = None
            indexEnnemiatoucher = None

            self.canvas.move(tir.sprite, 0,tir.direction*4)
            if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(self.player.sprite)[0]) < 20 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(self.player.sprite)[1]) < 33 and tir.direction == 1:
                
                touche = True
                self.GameOver = True
                
            for Ennemi in self.horde.listeEnnemis:
                if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(Ennemi.sprite)[0]) < 23 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(Ennemi.sprite)[1]) < 33 and tir.direction == -1:
                    
                    touche = True                    
                    if Ennemi.pv == 1:
                        indexEnnemiasuppr = self.horde.listeEnnemis.index(Ennemi)                  
                        self.score += Ennemi.score
                    else:
                        Ennemi.pv -= 1
                        indexEnnemiatoucher = self.horde.listeEnnemis.index(Ennemi)
               

            for bloc in self.murs.listeBlocs:
                if self.canvas.coords(bloc.sprite)[0] - self.canvas.coords(tir.sprite)[0] < 29 and self.canvas.coords(bloc.sprite)[0] - self.canvas.coords(tir.sprite)[0] > 0 and self.canvas.coords(tir.sprite)[1] - self.canvas.coords(bloc.sprite)[1] < 9 and self.canvas.coords(bloc.sprite)[1] - self.canvas.coords(tir.sprite)[1] < 29:
                    touche = True
                    indexblocasuppr = self.murs.listeBlocs.index(bloc)
            
            if indexEnnemiatoucher != None:
                self.canvas.itemconfig(self.horde.listeEnnemis[indexEnnemiatoucher].sprite, image=self.horde.listeEnnemis[indexEnnemiatoucher].setimage[self.horde.listeEnnemis[indexEnnemiatoucher].kind-1+2])
            if indexEnnemiasuppr != None:
                self.canvas.delete(self.horde.listeEnnemis[indexEnnemiasuppr].sprite)
                self.horde.listeEnnemis.remove(self.horde.listeEnnemis[indexEnnemiasuppr])
            if indexblocasuppr != None:
                self.canvas.delete(self.murs.listeBlocs[indexblocasuppr].sprite)
                self.murs.listeBlocs.remove(self.murs.listeBlocs[indexblocasuppr])
            
            if self.canvas.coords(tir.sprite)[1] >= 560 or self.canvas.coords(tir.sprite)[1] < 0 or touche == True:
                self.canvas.delete(tir.sprite)
                self.Tirsactuels.remove(tir)
            
            if self.GameOver == True:
                self.canvas.delete(self.player.sprite)
                self.canvas.after(1000, self.endGame)
                return

            if len(self.horde.listeEnnemis) == 0:
                self.transition = True
            if len(self.horde.listeEnnemis) == 0 and len(self.Tirsactuels) == 0:
                self.canvas.after(1000, self.newmanche)
                return
                
        self.canvas.after(16, self.GestionTirs)

class Bloc:
    def __init__(self, canvas, jeu,positionx, positiony):
        self.image = tk.PhotoImage(file='bloc.png').subsample(25,25)
        self.jeu = jeu
        self.canvas = canvas
        self.sprite = self.canvas.create_image(positionx,positiony,image=self.image, anchor='nw')
        
class Murs:
    def __init__(self, canvas, jeu):
        self.jeu = jeu
        self.canvas = canvas
        self.listeBlocs=[]
        for i in range(5):
            for j in range(3):
                self.listeBlocs.append(Bloc(canvas, jeu, 60+20*i, j*20+485))
                self.listeBlocs.append(Bloc(canvas, jeu, 260+20*i, j*20+485))
                self.listeBlocs.append(Bloc(canvas, jeu, 460+20*i, j*20+485))
                
        

    
if __name__ == '__main__':
    fenetre = tk.Tk()
    jeu = Jeu(fenetre, 8, 3)
    jeu.lancerMenu()
    jeu.fenetre.mainloop()