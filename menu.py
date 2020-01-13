from tkinter import *
import SpaceInvaderMain
fenetre_root = Tk()
fenetre_root.title('Space Invaders')
fenetre_root.geometry ("600x600")
fenetre_root.resizable(width=False, height=False)
canvas = Canvas(fenetre_root, bg = 'white', height = 600, width = 600)
canvas.pack(anchor='nw')
logo = canvas.create_image(50,50,image='logo.png')




fenetre_root.mainloop()