from tkinter import *
#from SpaceInvaderMain import *


fenetre_root = Tk()
fenetre_root.title('Space Invaders')
fenetre_root.geometry ("600x600")
fenetre_root.resizable(width=False, height=False)
canvas = Canvas(fenetre_root, bg = 'white', height = 600, width = 600, bd= 0, highlightthickness=0)
canvas.pack(anchor='nw')
imgLogo = PhotoImage(file = 'logo.png')
imgBackground = PhotoImage(file = 'backgroundMenu.png')
logo = canvas.create_image(300,300,image=imgBackground)
logo = canvas.create_image(300,133,image=imgLogo)
boutonPLay = Button(fenetre_root, text = 'PLAY !',height = 4, width = 20)
canvas.create_window(300,350,window = boutonPLay)
boutonExit = Button(fenetre_root, text = 'EXIT',height = 2, width = 10,command = fenetre_root.destroy)
canvas.create_window(300,450,window = boutonExit)

fenetre_root.mainloop()