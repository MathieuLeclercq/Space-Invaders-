# -*- coding: utf-8 -*-
from tkinter import *

class Ennemi:
    def __init__(self, setimage, fcanvas, Horde, positionx=3, positiony=3, direction = True, kind=1):
        self.kind = kind # Pas encore implementé
        self.fcanvas = fcanvas
        self.positionx = positionx
        self.positiony= positiony # Utile pour la position dans la horde lorsque deplacement par groupe
        self.sprite= fcanvas.create_image(50*positionx,1+51*positiony,image=setimage[kind-1], anchor='nw')
        self.direction = direction
        self.Horde = Horde

    def deplacement(self):
        if self.fcanvas.coords(self.sprite)[0] > 539 and self.direction:
            return 1
        elif self.fcanvas.coords(self.sprite)[0] < 11 and not(self.direction):
            return 1
        elif self.direction:
            self.fcanvas.move(self.sprite, 50,0)
            return 0
        elif not(self.direction):
            self.fcanvas.move(self.sprite, -50,0)
            return 0

class Horde:
    def __init__(self,imgmechants,fcanvas, length, heigth):
        self.direction = True
        self.listeEnnemis = []
        self.length = length
        self.heigth = heigth
        self.fcanvas = fcanvas
        for i in range(length):
            for j in range(heigth):
                self.listeEnnemis.append(Ennemi(imgmechants, fcanvas, self, i+(12-length)//2, j, self.direction))

    def deplacements(self):
        Condition = 0
        if not(self.direction):
            self.listeEnnemis.reverse()
        for mechant in self.listeEnnemis:
            if Condition == 0:
                Condition += mechant.deplacement()
        if Condition != 0:
            self.direction = not(self.direction)
            for mechant in self.listeEnnemis:
                mechant.direction = self.direction
                mechant.fcanvas.move(mechant.sprite, 0, 51)
        if self.direction or Condition ==0:
            self.listeEnnemis.reverse()
        canvas.after(500,self.deplacements)



class Player:
    def __init__(self, image, fcanvas, positionx=0, positiony=550, direction = 0):
        # fcanvas = canvas peut etre problematique
        self.fcanvas = fcanvas
        self.sprite= fcanvas.create_image(positionx,positiony,image=image, anchor='nw')
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

    


if __name__ == '__main__':
    fenetre_root = Tk()
    fenetre_root.title('Space Invaders')
    fenetre_root.geometry ("600x600")
    fenetre_root.resizable(width=False, height=False)
    canvas = Canvas(fenetre_root, bg = 'white', height = 600, width = 600)
    canvas.pack(anchor='nw')
    
    imgplayer = PhotoImage(file='player.png').subsample(10,10) #50px*50px
    imgmechants = [PhotoImage(file='mechant.png')] #50px*50px

    player = Player(imgplayer,canvas)
    horde = Horde(imgmechants,canvas, 6, 3)
    
    canvas.after(500,horde.deplacements)
    canvas.after(16,player.deplacementplayer)
    fenetre_root.bind('<Left>', player.moveleft)
    fenetre_root.bind('<Right>', player.moveright)
    fenetre_root.bind('<KeyRelease>', player.stopmove)
    fenetre_root.mainloop()

