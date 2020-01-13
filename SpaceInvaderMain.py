# -*- coding: utf-8 -*-
from tkinter import *
from random import *

class Ennemi:
    def __init__(self, setimage, fcanvas, Horde, positionx=6, positiony=1, direction = 1, vitesse = 50, frequence = 500, kind=1):
        self.kind = kind # Pas encore implementé
        self.fcanvas = fcanvas
        self.positionx = positionx
        self.positiony= positiony # Pourrait être utile. Position dans la grille de la horde
        self.sprite= fcanvas.create_image(50*positionx,50*positiony,image=setimage[kind-1], anchor='nw')
        self.direction = direction # utile pour les solitaires hors hordes qui donnent des bonus
        self.image=setimage[kind-1]
        self.Horde = Horde
        self.vitesse = vitesse
        self.frequence = frequence

    def deplacement(self):
        # Deplacement pour les solitaires persistant qui n'avancent pas (boss ?)
        deplacementOK=True
        if self.fcanvas.coords(self.sprite)[0] + self.direction*self.vitesse > 0 and self.fcanvas.coords(self.sprite)[0] + self.direction*self.vitesse + 50 < 600:
            self.fcanvas.move(self.sprite, self.direction*self.vitesse, 0)
        else:
            self.direction = (self.direction == -1) - (self.direction == 1)
            self.fcanvas.move(self.sprite, self.direction*self.vitesse, 0)
        canvas.after(self.frequence,self.deplacement)

class Horde:
    def __init__(self,setimage,fcanvas, length, heigth, vitesse = 50, direction = 1, frequence = 500):
        self.listeEnnemis = []
        self.length = length
        self.heigth = heigth
        self.setimage=setimage
        self.fcanvas = fcanvas
        self.vitesse = vitesse
        self.direction = direction
        self.frequence = frequence
        
        
        for i in range(length):
            for j in range(heigth):
                self.listeEnnemis.append(Ennemi(setimage, fcanvas, self, i+(12-length)//2, j, self.direction, self.vitesse, self.frequence))

    def deplacements(self):
        deplacementOK=True
        GameOver=False
        for Ennemi in self.listeEnnemis:
            if self.fcanvas.coords(Ennemi.sprite)[0] + self.direction*self.vitesse < 0 or self.fcanvas.coords(Ennemi.sprite)[0] + self.direction*self.vitesse + 50 > 600:
                deplacementOK = False
        if deplacementOK:
            for Ennemi in self.listeEnnemis:
                self.fcanvas.move(Ennemi.sprite, self.direction*self.vitesse, 0)
        else:
            for Ennemi in self.listeEnnemis:
                if self.fcanvas.coords(Ennemi.sprite)[1] + 50 + 50 > 550:
                    GameOver = True
            if GameOver:
                self.endGame()
                return

            for Ennemi in self.listeEnnemis:
                self.fcanvas.move(Ennemi.sprite, 0, 50)
                Ennemi.direction = (Ennemi.direction == -1) - (Ennemi.direction == 1) # Pas utilisé dans horde mais fait par rigueur
            self.direction = (self.direction == -1) - (self.direction == 1)
        canvas.after(self.frequence,self.deplacements)
    
    def endGame(self):
        # A refaire en supprimant totalement le canvas et ses binds pour le recréer avec une fonction
        self.fcanvas.delete('all')
        widget = Label(self.fcanvas, text='Game Over', fg='white', bg='black')
        widget.pack()
        self.fcanvas.create_window(300, 300, window=widget)       
    
    def Tir(self):
        for Ennemi in self.listeEnnemis:
            Tir = randint(0,100)
            if Tir <= 20:
                x=4
                
            
class Piou:
    def __init__(self, image, fcanvas, positionx, positiony, direction):
        self.image = PhotoImage(file='laser.png')
        self.fcanvas= fcanvas
        self.direction = direction
        self.sprite = fcanvas.create_image(positionx+25,positiony+50,image=image, anchor='nw')



class Player:
    def __init__(self, image, fcanvas, positionx=275, positiony=550, direction = 0):
        # fcanvas = canvas peut etre problematique
        self.fcanvas = fcanvas
        self.image = image # Pour recuperer les dimensions
        self.sprite= fcanvas.create_image(positionx,positiony,image=image, anchor='nw')
        self.direction = direction

    def moveleft(self, event):
        self.direction=-1

    def moveright(self, event):
        self.direction=1

    def stopmove(self, event):
        if (event.keysym == "q" and self.direction == -1) or (event.keysym == "d" and self.direction == 1):
            self.direction = 0
    def deplacementplayer(self):
        if (self.fcanvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.fcanvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0
        else:
            self.fcanvas.move(self.sprite, self.direction*5,0)
        self.fcanvas.after(16,self.deplacementplayer)



    
if __name__ == '__main__':
    fenetre_root = Tk()
    fenetre_root.title('Space Invaders')
    fenetre_root.geometry ("600x600")
    fenetre_root.resizable(width=False, height=False)
    canvas = Canvas(fenetre_root, bg = 'black', bd= 0, highlightthickness=0, height = 600, width = 600)
    canvas.pack(anchor='nw')
    
    imgplayer = PhotoImage(file='player.png').subsample(10,10) #50px*50px
    imgmechants = [PhotoImage(file='mechant.png')] #50px*50px

    player = Player(imgplayer,canvas)
    horde = Horde(imgmechants,canvas, 8, 8)
    
    canvas.after(16,horde.deplacements)
    canvas.after(16,player.deplacementplayer)
    fenetre_root.bind('<q>', player.moveleft)
    fenetre_root.bind('<d>', player.moveright)
    fenetre_root.bind('<KeyRelease>', player.stopmove)
    fenetre_root.mainloop()