import numpy as np
import copy
import time,sys
import Eval
import random
from tkinter import *
from tkinter import ttk
import random as easy

class Game:
    ## Class Game, of which an instance is created everytime the "Play" button is clicked  
    def __init__(self,root,a,btn,level):
        #Initializing all the variables and game screen to be required during the game
        self.title="Welcome to TicTacToe!"      # title
        self.btn=btn                            # 4 by 4 array of buttons
        self.a=a                                # Game board array
        self.Nodes=0                            # Counter for number of nodes at every AI move
        self.MaxDepth=0                         # Keeps a track of maximum depth reached
        self.CutOff=0                           # Keeps a track whether cutoff occured or no
        self.MaxPruning=0                       # Keeps a track of number of prunings in MAX function
        self.MinPruning=0                       # Keeps a track of number of prunings in MIN function
        self.level=level                        # difficulty level
        self.val=0                              # keeps a track of value returned by AlphaBetaSearch, 1000: AI wins, -1000: player wins, 0: draw
        self.master=root                        # Current tkinter game window instance

        #Setting the title of instance game window with repect to the difficulty level
        if self.level==1:
            self.master.title("Welcome to TicTacToe! Easy level")

        elif self.level==2:
            self.master.title("Welcome to TicTacToe! Medium level")
            self.max_time=1
            self.CutOffDepth=7

        elif self.level==3:
            self.master.title("Welcome to TicTacToe! Difficult level")
            self.max_time=10
            self.CutOffDepth=6 


        self.RFrame=Frame(root)                 #A frame in the window to display statistics of each AI move
        self.RFrame.pack(side=RIGHT)            #Packing the frame in the window
        self.BFrame=Frame(root)                 #A frame in the window to display the game board
        self.BFrame.pack(side=LEFT,padx=50,pady=40)
        self.Label1=Label(self.RFrame,text="Your Move Next")        # Label which will be updated throughout the duration of instance to display statistics of AI's moves
        self.Label1.grid(row=0,padx=100)
        for x in range(4):
            for y in range(4):
                ## Binding OnClick event with each of the button to update the matrix a
                self.btn[x][y] = Button(self.BFrame,command=lambda x1=x,y1=y: self.trigger(a,x1,y1))
                self.btn[x][y].config(width=5)
                self.btn[x][y].grid(column=x, row=y)
        self.updateBoard()


    # trigger method, called everytime a button is clicked on the game board   
    def trigger(self,a,i,j):

        if self.CheckGameStatus(self.a)==False:
            #Checks the status of the game, if false, the game has ended
            self.Labelappend("\nGame Over")

        elif self.InsertO(i,j):
            if self.CheckGameStatus(self.a)==False:
                #Checks the status of the game, if false, the game has ended
                self.Labelappend("\nGame Over")
            self.updateBoard()
            if self.level==1:
                #Easy level, random numbers approach

                self.Label1.config(text="Easy level")                          
                m,n=self.Actions(self.a)
                i=easy.choice(m)
                j=easy.choice(n)
                while(self.InsertX(i,j)==False):
                    i=easy.choice(m)
                    j=easy.choice(n)
                if self.CheckGameStatus(self.a)==False:
                    self.Labelappend("\nGame Over")
            else:
                #Medium/difficult level, Minimax Approach(with alpha-beta pruning)
                if self.CheckGameStatus(self.a)==False:
                    #Checks the status of the game, if false, the game has ended
                    self.Labelappend("\nGame Over")
                else:
                    t0=time.time()
                    depth=self.Checkdepth()
                    v,position=self.AlphaBetaSearch(self.a,t0,depth)
                    self.val=v
                    i,j=position.split(',')
                    i=int(i[1])
                    j=int(j[1])
                    if self.InsertX(i,j):
                        if self.CheckGameStatus(self.a)==False:
                            self.Labelappend("\nGame Over")  
                    else:
                        print ("Position already filled")     
          
          
    

    def updateBoard(self):
        # Updates the game board as per the matrix which is internally updated and stores all the X's and O's positions
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                self.btn[i][j].config(text=self.a[i][j])

    def Print_Board(self):
        #Function to Print_Board
        #print (np.array(self.a))
        self.updateBoard()

    def Checkdepth(self):
        # Checks the depth level currently with respect to initial state
        temp=0
        for i in self.a:
                if i=="X" or i=="O":
                    temp+=1
        return temp

    def InsertX(self,i,j):
        #Function to insert X at a postion i,j
        if self.a[i][j]==' ':
            self.a[i][j]='X'
            self.Print_Board()
            return True
        return False

    def InsertO(self,i,j):
        #Function to insert X at a postion i,j
        if self.a[i][j]==' ':
            self.a[i][j]='O'
            self.Print_Board()
            return True
        return False

    def CheckWin(self,board):
        #Function that checks if a terminating condition is reached beacuse of a player winning

        board=np.array(board)
        if np.all(np.diag(board)=='O') or np.all(np.diag(board)=='X'):
            return board[0][0]
        elif np.all(np.diag(np.fliplr(board))=='O') or np.all(np.diag(np.fliplr(board))=='X'):
            return board[0][3]
        else:
            for i in range(4):
                if np.all(board[i]=='O') or np.all(board[i]=='X'):
                    return board[i][0]
                elif np.all(board[:,i]=='O') or np.all(board[:,i]=='X'):
                    return board[0][i]
        return False
    
    def CheckGameStatus(self,board):
        #Function that checks the various terminating conditions for the game board like player wins, 
        # computer wins or if the board is filled then declare a draw
        
        board=np.array(board)
        result=self.CheckWin(board)
        if result!=False:
            if result=="O":
                temp=str("You Win")
            elif result=="X":
                temp=str("AI Wins")
            self.Label1.config(text=temp)
            return False
        if np.any(board==' '):
            return True
        else:
            temp=str("It's a Draw")
            self.Label1.config(text=temp)
            return False

    def Utility(self,board):
        # Function to calculate the utility value of the given board state
        board=np.array(board)
        if self.CheckWin(board)!=False:
            x=self.CheckWin(board)
            return (1000 if x=='X' else -1000)
        elif np.any(board!=' '):
            return 0


    def Actions(self,board):
        # return all possible remaining actions for the current board state
        indexi=[]
        indexj=[]
        for i in range(4):
            for j in range(4):
                if(board[i][j]==' '):
                    indexi.append(i)
                    indexj.append(j)
        return indexi,indexj

    def ResultX(self,board,i,j):
        # Returns board on performing action (inserting X) at location i,j
        boardtemp=copy.deepcopy(board)
        boardtemp[i][j]='X'
        return boardtemp

    def ResultO(self,board,i,j):
        # Returns board on performing action (inserting O) at location i,j
        boardtemp=copy.deepcopy(board)
        boardtemp[i][j]='O'
        #Print_Board(boardtemp)
        return boardtemp

    
    def CutOffSearch(self,board):
        #Cut off Search function, called when either max-depth is reached or max-time has passed
        if self.CheckGameStatus(board)==False:
            self.CutOff=0
            return self.Utility(board[:])
        else:
            self.CutOff=1                                                   #Checking flag as cutoff occured
            if self.level==2:
                return Eval.Medium_EvaluationFunction(board[:])             #current level is medium
            return Eval.Difficult_EvaluationFunction(board[:])              #current level is difficult

   
    def AlphaBetaSearch(self,board,t0,depth):
        # The main AlphaBeta Search algorithm

        self.Label1.config(text="")
        bestmove={}                     # dictionary to keep track of all possible moves as keys, and their values as values
        CurrentLevel=0                  # CurrentLevel, set to 0 for this particular tree of the AI's next move
        self.Nodes=0                    # resetting number of nodes to 0, for upcoming move of AI
        self.MaxDepth=0                 # resetting max-depth to 0, for upcoming move of AI
        self.MaxPruning=0               # resetting number of max-pruning to 0, for upcoming move of AI
        self.MinPruning=0               # resetting number of min-pruning to 0, for upcoming move of AI

        v=self.MaxAction(board,-1000,1000,CurrentLevel,depth,t0,bestmove) # CurrentLevel is variable depth which increments and depth is constant to compare against
        
        ## Displaying the statistics for each AI move
        self.Label1.config(text="\nTotal number of nodes generated: ")
        self.Labelappend(str(self.Nodes))
        if self.CutOff==1:
            self.Labelappend("\nCutoff occured")
        else:
            self.Labelappend("\nNo Cutoff ")
        self.Labelappend("\nMaximum Depth reached: ")
        self.Labelappend(str(self.MaxDepth))
        self.Labelappend("\nNumber of times Pruning occured in MAX Function: ")
        self.Labelappend(str(self.MaxPruning))
        self.Labelappend("\nNumber of times Pruning occured in MIN Function: ")
        self.Labelappend(str(self.MinPruning))
        
        print(self.Label1.cget("text"))     #printing in commandline
        print (bestmove)
        print (v)
        ## Returning the best AI move
        for position,value in bestmove.items():
            if value==v:
                print (position,value)
                return v,str(position)
  
    
    def Labelappend(self,text):
        # Function to append text to Label1 label, used to display statistics of each AI move
        temp=self.Label1.cget("text")+text
        self.Label1.config(text=temp)

    def MaxAction(self,board,alpha,beta,i,depth,t0,bestmove):
        #Max function

        self.Nodes+=1                               #incrementing number of nodes
        t=time.time()-t0                            #Calculating the time passed
        if self.MaxDepth<i:
            self.MaxDepth=i
        if self.CheckGameStatus(board)==False or t>self.max_time or i>=(depth+self.CutOffDepth):
            #Checking if cutoff/utility is required
            return self.CutOffSearch(board[:])      #cuts-off search or returns utility value if avaliable
        v=-10000                                    #setting max-value to -1000
        indexi,indexj=self.Actions(board)           #getting all possible actions
        for x in range(len(indexi)):                #iterating through all possible actions
            #recursive call to MinAction function
            v_min=self.MinAction(self.ResultX(board[:],indexi[x],indexj[x]),alpha,beta,i+1,depth,t0,bestmove)
            v=max(v,v_min)
            if(i==depth):
                temp=indexi[x],indexj[x]
                bestmove[temp]=v
            if v>=beta:                             #beta pruning
                self.MaxPruning+=1
                return v
            alpha=max(alpha,v)                      #updating the value of alpha, if lesser than v
        return v                                    #returning the value v for the particular move


    def MinAction(self,board,alpha,beta,i,depth,t0,bestmove):
        #Min function

        self.Nodes+=1                               #incrementing number of nodes
        t=time.time()-t0                            #Calculating the time passed
        if self.MaxDepth<i:
            self.MaxDepth=i
        if self.CheckGameStatus(board)==False or t>self.max_time or i>=(depth+self.CutOffDepth):
            #Checking if cutoff/utility is required
            return self.CutOffSearch(board[:])      #cuts-off search or returns utility value if avaliable
        v=10000                                     #setting min-value to +1000
        indexi,indexj=self.Actions(board)           #getting all possible actions
        for x in range(len(indexi)):                #iterating through all possible actions
            #recursive call to MaxAction function
            v_max=self.MaxAction(self.ResultO(board[:],indexi[x],indexj[x]),alpha,beta,i+1,depth,t0,bestmove)
            v=min(v,v_max)
            if(i==depth):
                temp=indexi[x],indexj[x]
                bestmove[temp]=v
            if v<=alpha:                            #alpha pruning
                self.MinPruning+=1
                return v
            beta=min(beta,v)                        #updating the value of beta, if greater than v
        return v                                    #returning the value v for the particular move