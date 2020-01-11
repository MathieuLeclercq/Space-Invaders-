# -*- coding: utf-8 -*-
from tkinter import *
from V4 import *
class Ennemi:
    def __init__(self, setimage, directionLeft = True, positionx=52, positiony=28, kind=1, fcanvas):
        self.kind = kind # Pas encore implementé
        self.fcanvas = fcanvas
        self.sprite= fcanvas.create_image(50*positionx,28+51*positiony,image=setimage[kind], anchor='nw')
        self.directionLeft = directionLeft
        self.position = fcanvas.coords(self.sprite) #Peut etre problematique

    def deplacement(self):
        if self.position[0] > 539 and self.directionLeft:
            self.fcanvas.move(self.sprite, 0,51)
            self.directionLeft = False
            return
        elif self.position[0] < 11 and not(self.directionLeft):
            self.fcanvas.move(self.sprite, 0,51)
            self.directionLeft = True
            return
        elif self.directionLeft:
            self.fcanvas.move(self.sprite, 50,0)
            return
        elif not(self.directionLeft):
            self.fcanvas.move(self.sprite, -50,0)
        return

class Player:
    def __init__(self, image, positionx=52, positiony=28, fcanvas, direction = 0):
        # fcanvas = canvas peut etre problematique
        self.fcanvas = fcanvas
        self.sprite= fcanvas.create_image(50*positionx,28+51*positiony,image=image, anchor='nw')
        self.position = fcanvas.coords(self.sprite) # Peut être problematique
        self.direction = direction

    def moveleft(self, event):
        self.direction=-1

    def moveright(self, event):
        self.direction=1

    def stopmove(self, event):
        if (event.keysym == "Left" and self.direction == -1) or (event.keysym == "Right" and self.direction == 1):
            self.direction = 0
    def deplacementplayer(self):
        if (self.fcanvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.fcanvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0
        else:
            self.fcanvas.move(self.sprite, self.direction*5,0)
        self.fcanvas.after(16,self.deplacementplayer)