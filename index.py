from tkinter import *                       #tkinter library for graphics
from tictactoeai import Game                # importing game class from tictactoeai.py
import random                               #random variable generation library

## INITIALIZING TKINTER WINDOW
root = Tk()
root.title("Welcome to TicTacToe by Ajay Thorve - aat414")      #setting the title
RFrame=Frame(root)                                              #adding a frame
RFrame.pack(side=RIGHT)                                         #packing the frame to root


def start():
    #start function, called when program is initialized
    window =Toplevel(root)                                      #new window created for game instance
    a=[[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' ']]     #initialize empty 4 by 4 array
    if(firstmove.get()==1):                                     #if no, get a random position and play on behalf of the AI
        i,j=random.sample(range(4),2)
        a[i][j]='X'
    btn= [[0 for x in range(4)] for x in range(4)]              
    start = Game(window,a,btn,level.get())                      #create an instance of class Game

level = IntVar()                                                #initialzing radio button variable for difficulty level
level.set(1)


## Creating Labels, radio buttons, play and quit buttons, and assigning them to the home page
Label(RFrame,text=" Welcome to TicTacToe ").pack(anchor=CENTER,pady=100)
Label(RFrame,text="Choose Difficulty").pack(padx=450)
Radiobutton(RFrame, text="Easy", variable=level, value=1).pack(anchor=W,padx=450)
Radiobutton(RFrame, text="Medium", variable=level, value=2).pack(anchor=W,padx=450)
Radiobutton(RFrame, text="Difficult", variable=level, value=3).pack(anchor=W,padx=450)

#check if user wants to play first move or no
firstmove = IntVar()                                            #initialzing radio button variable for first move flag

#Play first move label and radio buttons
Label(RFrame,text="Play first move?").pack(padx=450)            
Radiobutton(RFrame, text="Yes", variable=firstmove, value=0).pack(anchor=W,padx=450)
Radiobutton(RFrame, text="No", variable=firstmove, value=1).pack(anchor=W,padx=450)


Button(RFrame,text="Play",command=start).pack(pady=50)             #Play button
Button(RFrame,text="Quit the Game",command=quit).pack(pady=50)     #Quit the game button




#run the mainloop inorder for the graphics to keep running until manually quit
root.mainloop()
