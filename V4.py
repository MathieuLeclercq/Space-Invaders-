# -*- coding: utf-8 -*-
from tkinter import *

fenetre_root = Tk()
fenetre_root.title('Space Invaders')
fenetre_root.geometry ("600x600")
#fenetre_root.configure(bg = "black")
fenetre_root.resizable(width=False, height=False)
global canvas
canvas = Canvas(fenetre_root, bg = 'white', height = 600, width = 600)
canvas.pack(anchor='nw')
boutonExit = Button(fenetre_root, text = 'EXIT', bg = 'white', relief="solid", command = fenetre_root.destroy, borderwidth=0)
canvas.create_window(0,0,window = boutonExit, anchor='nw')
canvas.create_line(0, 27, 600, 27, fill="grey")

global dire
dire=0
def moveleft(event):
    global dire
    dire=-1
    print(dire)
def moveright(event):
    global dire
    dire=1
    print(dire)
def stopmove(event):
    global dire
    if (event.keysym == "Left" and dire == -1) or (event.keysym == "Right" and dire == 1):
        dire = 0
        print(dire)
def bouge():
    global dire,player
    if (canvas.coords(player)[0] <= 4 and dire==-1) or (canvas.coords(player)[0] >= 550 and dire==1) :
        dire=0
        print(dire)
    else:
        canvas.move(player, dire*5,0)
    canvas.after(16,bouge)


class Ennemi:
    def __init__(self, image, directionLeft = True, kind=1, positionx=52, positiony=28):
        self.kind = kind
        self.positionx = positionx
        self.positiony = positiony
        self.image = image
        self.directionLeft = directionLeft
        
    def deplacement(self):
        if canvas.coords(self.image)[0] > 539 and self.directionLeft:
            canvas.move(self.image, 0,51)
            self.directionLeft = False
            return
        elif canvas.coords(self.image)[0] < 11 and not(self.directionLeft):
            canvas.move(self.image, 0,51)
            self.directionLeft = True
            return
        elif self.directionLeft:
            canvas.move(self.image, 50,0)
        elif not(self.directionLeft):
            canvas.move(self.image, -50,0)
            return


################################################
img = PhotoImage(file='player.png')
global playerimage
playerimage = img.subsample(10,10) #50px*50px
global player
player = canvas.create_image(0,600,image=playerimage, anchor='sw')

global mechantimage
mechantimage = PhotoImage(file='mechant.png') #50px*50px
#################################################

Ennemis = []
for j in range(3):
    for i in range(12):
        Ennemis.append(Ennemi(canvas.create_image(50*i,28+j*51,image=mechantimage, anchor='nw'), (j==1 or j==3)))

def deplacements():
    for x in Ennemis:
        x.deplacement()
    canvas.after(500,deplacements)
        
#class Horde:
#    def __init__(Ennemis):
#        self.Ennemis=Ennemis
#
#TTT = Horde(Ennemi())
#for i in range(3):
#    Horde
    
###################################


        
canvas.after(500,deplacements)

canvas.after(16,bouge)
fenetre_root.bind('<Left>', moveleft)
fenetre_root.bind('<Right>', moveright)
fenetre_root.bind('<KeyRelease>', stopmove)
fenetre_root.mainloop()
