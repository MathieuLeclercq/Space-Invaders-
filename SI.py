# -*- coding: utf-8 -*-
import tkinter as tk
import random as rd

class Ennemi:
    def __init__(self, fcanvas, jeu, Horde, positionx=6, positiony=1, direction = 1, vitesse = 50, frequence = 500, kind=1):
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
        # Deplacement pour les solitaires persistant qui n'avancent pas (boss ?)
        if self.fcanvas.coords(self.sprite)[0] + self.direction*self.vitesse > 0 and self.fcanvas.coords(self.sprite)[0] + self.direction*self.vitesse + 50 < 600:
            self.fcanvas.move(self.sprite, self.direction*self.vitesse, 0)
        else:
            self.direction = (self.direction == -1) - (self.direction == 1)
            self.fcanvas.move(self.sprite, self.direction*self.vitesse, 0)
        self.fcanvas.after(self.frequence,self.deplacement)

class Horde:
    def __init__(self,fcanvas, jeu, length, heigth, vitesse = 50, direction = 1, frequence = 500):
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
                if self.fcanvas.coords(Ennemi.sprite)[1] + 50 + 50 > 550:
                    self.jeu.GameOver = True
            if self.jeu.GameOver:
                self.jeu.endGame()
                return

            for Ennemi in self.listeEnnemis:
                self.fcanvas.move(Ennemi.sprite, 0, 50)
                Ennemi.direction = (Ennemi.direction == -1) - (Ennemi.direction == 1) # Pas utilisé dans horde mais fait par rigueur
            self.direction = (self.direction == -1) - (self.direction == 1)
        self.fcanvas.after(self.frequence,self.deplacements)
    
    def NouveauTir(self):
        if self.jeu.GameOver:
            return
        for Ennemi in self.listeEnnemis:
            probatir = rd.randint(0,100)
            if probatir <= 20:
                self.jeu.Tirsactuels.append(Tir(self.fcanvas, self.jeu, self.fcanvas.coords(Ennemi.sprite)[0], self.fcanvas.coords(Ennemi.sprite)[1], 1))
        self.fcanvas.after(5000, self.NouveauTir)
                
                
            
class Tir:
    def __init__(self, fcanvas, jeu, positionx, positiony, direction):
        self.image = tk.PhotoImage(file='laser.png')
        self.fcanvas= fcanvas
        self.jeu = jeu
        self.direction = direction
        self.sprite = fcanvas.create_image(positionx,positiony+direction*30,image=self.image, anchor='nw')



class Player:
    def __init__(self, fcanvas, jeu, positionx=275, positiony=550, direction = 0):
        # fcanvas = canvas peut etre problematique
        self.fcanvas = fcanvas
        self.image = tk.PhotoImage(file='player.png').subsample(10,10) #50px*50px
        self.sprite= fcanvas.create_image(positionx,positiony,image=self.image, anchor='nw')
        self.direction = direction
        self.jeu = jeu

    def moveleft(self, event):
        self.direction=-1

    def moveright(self, event):
        self.direction=1

    def stopmove(self, event):
        if (event.keysym == "q" and self.direction == -1) or (event.keysym == "d" and self.direction == 1):
            self.direction = 0
    def deplacementplayer(self):
        if self.jeu.GameOver:
            return
        if (self.fcanvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.fcanvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0
        else:
            self.fcanvas.move(self.sprite, self.direction*5,0)
        self.fcanvas.after(16,self.deplacementplayer)

    def NouveauTirP(self, event):
        self.jeu.Tirsactuels.append(Tir(self.fcanvas, self.jeu, self.fcanvas.coords(self.sprite)[0], self.fcanvas.coords(self.sprite)[1], -1))

class Jeu:
    def __init__(self, fenetre):
        # A ameliorer pour configurer depuis la declaration d'un objet jeu
        self.fenetre = fenetre
        self.canvas = tk.Canvas(fenetre, bg = 'black', bd= 0, highlightthickness=0, height = 600, width = 600)
        self.player = Player(self.canvas, self)
        self.horde = Horde(self.canvas, self, 6, 3)
        self.GameOver = False
        self.Tirsactuels = []
    
    def Debut(self):
        self.canvas.pack(anchor='nw')
        self.canvas.after(16, self.horde.deplacements)
        self.canvas.after(16, self.player.deplacementplayer)
        self.canvas.after(16, self.GestionTirs)
        self.canvas.after(16, self.horde.NouveauTir)
        self.fenetre.bind('<q>', self.player.moveleft)
        self.fenetre.bind('<Q>', self.player.moveleft)
        self.fenetre.bind('<d>', self.player.moveright)
        self.fenetre.bind('<D>', self.player.moveright)
        self.fenetre.bind('<KeyRelease>', self.player.stopmove)
        self.fenetre.bind('<space>', self.player.NouveauTirP)

    def endGame(self):
        # A refaire en supprimant totalement le canvas et ses binds pour le recréer avec une fonction
        self.canvas.delete('all')
        widget = tk.Label(self.canvas, text='Game Over', fg='white', bg='black')
        widget.pack()
        self.canvas.create_window(300, 300, window=widget)
    
    def GestionTirs(self):
        if self.GameOver:
            return
        for tir in self.Tirsactuels:
            self.canvas.move(tir.sprite, 0,tir.direction*5)
            if self.canvas.coords(tir.sprite)[1] > 600 or self.canvas.coords(tir.sprite)[1] < -50:
                self.canvas.delete(tir.sprite)
                self.Tirsactuels.remove(tir)
        self.canvas.after(64, self.GestionTirs)


# Gestion mort player ou monstre + replay + obstacle
    
if __name__ == '__main__':
    fenetre_root = tk.Tk()
    fenetre_root.title('Space Invaders')
    fenetre_root.geometry ("600x600")
    fenetre_root.resizable(width=False, height=False)

    jeu = Jeu(fenetre_root)
    jeu.Debut()


    fenetre_root.mainloop()
