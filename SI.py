# -*- coding: utf-8 -*-
import tkinter as tk
import random as rd

class Ennemi:
    def __init__(self, fcanvas, jeu, Horde, positionx=6, positiony=1, direction = 1, vitesse = 2, frequence = 16, kind=1):
        self.kind = kind # Pas encore implementé
        self.fcanvas = fcanvas
        self.positionx = positionx
        self.setimage = [tk.PhotoImage(file='mechant.png')] #50px*50px
        self.positiony= positiony # Pourrait être utile. Position dans la grille de la horde
        self.sprite= fcanvas.create_image(50*positionx,50*positiony,image=self.setimage[kind-1], anchor='nw')
        self.direction = direction # utile pour les solitaires hors hordes qui donnent des bonus
        self.image=self.setimage[kind-1]
        self.Horde = Horde
        self.vitesse = vitesse
        self.frequence = frequence
        self.jeu = jeu

    def deplacement(self):
        if self.jeu.GameOver:
            return
        # Deplacement pour les solitaires persistant500 qui n'avancent pas (boss ?)
        if self.fcanvas.coords(self.sprite)[0] + self.direction*self.vitesse > 0 and self.fcanvas.coords(self.sprite)[0] + self.direction*self.vitesse + 50 < 600:
            self.fcanvas.move(self.sprite, self.direction*self.vitesse, 0)
        else:
            self.direction = (self.direction == -1) - (self.direction == 1)
            self.fcanvas.move(self.sprite, self.direction*self.vitesse, 0)
        self.fcanvas.after(self.frequence,self.deplacement)

class Horde:
    def __init__(self,fcanvas, jeu, length, heigth, vitesse = 1, direction = 1, frequence = 16):
        self.listeEnnemis = []
        self.length = length
        self.heigth = heigth
        self.setimage = [tk.PhotoImage(file='mechant.png')] #50px*50px
        self.fcanvas = fcanvas
        self.jeu = jeu
        self.vitesse = vitesse
        self.direction = direction
        self.frequence = frequence
        
        
        for i in range(length):
            for j in range(heigth):
                self.listeEnnemis.append(Ennemi(fcanvas, jeu, self, i+(12-length)//2, j, self.direction, self.vitesse, self.frequence))

    def deplacements(self):
        if self.jeu.GameOver:
            return
        deplacementOK=True
        for Ennemi in self.listeEnnemis:
            if self.fcanvas.coords(Ennemi.sprite)[0] + self.direction*self.vitesse < 0 or self.fcanvas.coords(Ennemi.sprite)[0] + self.direction*self.vitesse + 50 > 600:
                deplacementOK = False
        if deplacementOK:
            for Ennemi in self.listeEnnemis:
                self.fcanvas.move(Ennemi.sprite, self.direction*self.vitesse, 0)
        else:
            for Ennemi in self.listeEnnemis:
                if self.fcanvas.coords(Ennemi.sprite)[1] + 50 + 25 > 550:
                    self.jeu.GameOver = True
            if self.jeu.GameOver:
                self.jeu.endGame()
                return

            for Ennemi in self.listeEnnemis:
                self.fcanvas.move(Ennemi.sprite, 0, 25)
                Ennemi.direction = (Ennemi.direction == -1) - (Ennemi.direction == 1) # Pas utilisé dans horde mais fait par rigueur
            self.direction = (self.direction == -1) - (self.direction == 1)
        self.fcanvas.after(self.frequence,self.deplacements)
    
    def NouveauTir(self):
        if self.jeu.GameOver:
            return
        for Ennemi in self.listeEnnemis:
            probatir = rd.randint(0,5000)
            if probatir <= 1:
                self.jeu.Tirsactuels.append(Tir(self.fcanvas, self.jeu, self.fcanvas.coords(Ennemi.sprite)[0], self.fcanvas.coords(Ennemi.sprite)[1], 1))
        self.fcanvas.after(16, self.NouveauTir)
                
                
            
class Tir:
    def __init__(self, fcanvas, jeu, positionx, positiony, direction):
        self.image = [tk.PhotoImage(file='laser.png'), tk.PhotoImage(file='laser2.png')]
        self.fcanvas= fcanvas
        self.jeu = jeu
        self.direction = direction
        self.sprite = fcanvas.create_image(positionx,positiony+direction*30,image=self.image[(self.direction == -1)], anchor='nw')



class Player:
    def __init__(self, fcanvas, jeu, positionx=275, positiony=550, direction = 0):
        # fcanvas = canvas peut etre problematique
        self.fcanvas = fcanvas
        self.image = tk.PhotoImage(file='player.png').subsample(10,10) #50px*50px
        self.sprite= fcanvas.create_image(positionx,positiony,image=self.image, anchor='nw')
        self.direction = direction
        self.jeu = jeu
        self.TimerTir = 1000
        self.tir = 0

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
            self.tir = 0
            print("tu n'appuye plus sur espace")
    def deplacementplayer(self):
        if self.jeu.GameOver:
            return
        if (self.fcanvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.fcanvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0
        else:
            self.fcanvas.move(self.sprite, self.direction*5,0)
        self.fcanvas.after(16,self.deplacementplayer)
        
        if self.tir == 1 and self.TimerTir >= 25:
            self.jeu.Tirsactuels.append(Tir(self.fcanvas, self.jeu, self.fcanvas.coords(self.sprite)[0], self.fcanvas.coords(self.sprite)[1], -1))
            self.TimerTir = 0

    def NouveauTirP(self, event):
        if self.jeu.GameOver:
            return
        if self.TimerTir >= 25:
            self.tir = 1  
    
    def PasdeTir(self):
        if self.jeu.GameOver:
            return
        self.TimerTir += 1

        self.fcanvas.after(16, self.PasdeTir)


class Menu:
    def __init__(self):
        self.background = tk.PhotoImage(file = 'backgroundMenu.png')
        self.logo =  tk.PhotoImage(file = 'logo.png')



class Jeu:
    def __init__(self):
        # A ameliorer pour configurer depuis la declaration d'un objet jeu
        self.fenetre = tk.Tk()
        self.fenetre.title('Space Invaders')
        self.fenetre.geometry("600x600")
        self.fenetre.resizable(width=False, height=False)

        self.canvas = tk.Canvas(self.fenetre, bg = 'black', bd= 0, highlightthickness=0, height = 600, width = 600)

        self.player = Player(self.canvas, self)
        self.horde = Horde(self.canvas, self, 11, 11)
        self.murs = Murs(self.canvas,self)
        self.GameOver = False
        self.Tirsactuels = []

        self.menu = Menu()
        self.boutonPlay = tk.Button(self.fenetre, text = 'PLAY !',height = 4, width = 20,command=self.Debut,activebackground='#ffbd33',background='#FFE213')
        self.boutonExit = tk.Button(self.fenetre, text = 'EXIT',height = 2, width = 10,command=self.fenetre.destroy,activebackground='#ffbd33',background='#FFE213')

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
        

    def endGame(self):
        # A refaire en supprimant totalement le canvas et ses binds pour le recréer avec une fonction
        self.canvas.delete('all')
        widget = tk.Button(self.canvas, text='Game Over', fg='white', bg='black', command=self.relaunch)
        widgetc = self.canvas.create_window(300, 300, window=widget)
        
    def relaunch(self):
        self.canvas.delete('all')
        # Visiblement à revoir
        self.canvas = tk.Canvas(self.fenetre, bg = 'black', bd= 0, highlightthickness=0, height = 600, width = 600)
        self.player = Player(self.canvas, self)
        self.horde = Horde(self.canvas, self, 10, 10)
        self.murs = Murs(self.canvas,self)
        self.GameOver = False
        self.Tirsactuels = []
        
        
        
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

    def GestionTirs(self):
        if self.GameOver:
            return
        for tir in self.Tirsactuels:
            touche = False
            indexEnnemiasuppr = None 
            indexblocasuppr = None
            self.canvas.move(tir.sprite, 0,tir.direction*4)
            if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(self.player.sprite)[0]) < 20 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(self.player.sprite)[1]) < 33 and tir.direction == 1:
                
                touche = True
                # TUER PLAYER ET GAME OVER
                
            for Ennemi in self.horde.listeEnnemis:
                if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(Ennemi.sprite)[0]) < 23 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(Ennemi.sprite)[1]) < 33 and tir.direction == -1:
                    
                    touche = True                    
                    indexEnnemiasuppr = self.horde.listeEnnemis.index(Ennemi)                  
                    
            for bloc in self.murs.listeBlocs:
                if abs(self.canvas.coords(tir.sprite)[0] - self.canvas.coords(bloc.sprite)[0]) < 25 and abs(self.canvas.coords(tir.sprite)[1] - self.canvas.coords(bloc.sprite)[1]) < 39:
                    
                    touche = True
                    indexblocasuppr = self.murs.listeBlocs.index(bloc)
            
            
            if indexEnnemiasuppr != None:
                self.canvas.delete(self.horde.listeEnnemis[indexEnnemiasuppr].sprite)
                self.horde.listeEnnemis.remove(self.horde.listeEnnemis[indexEnnemiasuppr])
            if indexblocasuppr != None:
                self.canvas.delete(self.murs.listeBlocs[indexblocasuppr].sprite)
                self.murs.listeBlocs.remove(self.murs.listeBlocs[indexblocasuppr])
                
            
            if self.canvas.coords(tir.sprite)[1] >= 560 or self.canvas.coords(tir.sprite)[1] < 0 or touche == True:
                self.canvas.delete(tir.sprite)
                self.Tirsactuels.remove(tir)
            
            
            
        self.canvas.after(16, self.GestionTirs)

class Bloc:
    def __init__(self, canvas, jeu,positionx, positiony):
        self.image = tk.PhotoImage(file='bloc.png').subsample(25,25)
        self.jeu = jeu
        self.canvas = canvas
        self.sprite = self.canvas.create_image(positionx,positiony,image=self.image, anchor='nw')
        
class Murs:
    def __init__(self, fcanvas, jeu):
        self.jeu = jeu
        self.canvas = fcanvas
        self.listeBlocs=[]
        for i in range(5):
            for j in range(3):
                self.listeBlocs.append(Bloc(fcanvas, jeu, 60+20*i, j*20+525-40))
                self.listeBlocs.append(Bloc(fcanvas, jeu, 260+20*i, j*20+525-40))
                self.listeBlocs.append(Bloc(fcanvas, jeu, 460+20*i, j*20+525-40))
                
        
        
# Gestion mort player ou monstre + replay + obstacle
    
if __name__ == '__main__':
    jeu = Jeu()
    jeu.lancerMenu()
    jeu.fenetre.mainloop()


