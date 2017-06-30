import copy
import numpy as np



#Function that checks if a terminating condition is reached beacuse of a player winning
def CheckWin(board):
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


def Difficult_EvaluationFunction(board):
    # Difficult level Evaluation function implementation. Calculates using 6*x[3]+3*x[2]+x[1]-6*o[3]-3*o[2]-o[1] , 
    # where, o[i] : “i” number of number of O’s vertically, horizontally and diagonally, without any X’s
    #        x[i] : “i” number of number of X’s vertically, horizontally and diagonally, without any O’s
    boardtemp=copy.deepcopy(board)
    boardtemp=np.array(board)
    if CheckWin(board)!=False:
        if CheckWin(board)=='X':
            return 1000
        elif CheckWin(board)=='O':
            return -1000
    x=[0,0,0,0]
    o=[0,0,0,0]

    #Count x1,x2,x3,o1,o2,o3 for 45 degree diagonal
    if list(np.diag(boardtemp)).count('X')>0 and list(np.diag(boardtemp)).count('O')==0:
        c=list(np.diag(boardtemp)).count('X')
        x[c-1]+=1
    if list(np.diag(boardtemp)).count('O')>0 and list(np.diag(boardtemp)).count('X')==0:
        c=list(np.diag(boardtemp)).count('O')
        o[c-1]+=1

    #Count x1,x2,x3,o1,o2,o3 for 135 degree diagonal
    if list(np.diag(np.fliplr(boardtemp))).count('X')>0 and list(np.diag(np.fliplr(boardtemp))).count('O')==0:
        c=list(np.diag(np.fliplr(boardtemp))).count('X')
        x[c-1]+=1
    elif list(np.diag(np.fliplr(boardtemp))).count('O')>0 and list(np.diag(np.fliplr(boardtemp))).count('X')==0:
        c=list(np.diag(np.fliplr(boardtemp))).count('O')
        o[c-1]+=1

    #Count x1,x2,x3,o1,o2,o3 for all rows
    for i in range(4):
        if list(boardtemp[i]).count('X')>0 and list(boardtemp[i]).count('O')==0:
            c=list(boardtemp[i]).count('X')
            x[c]+=1
        elif list(boardtemp[i]).count('O')>0 and list(boardtemp[i]).count('X')==0:
            c=list(boardtemp[i]).count('O')
            o[c]+=1

    #Count x1,x2,x3,o1,o2,o3 for all columns
    for i in range(4):
        if list(boardtemp[:,i]).count('X')>0 and list(boardtemp[:,i]).count('O')==0:
            c=list(boardtemp[:,i]).count('X')
            x[c]+=1
        elif list(boardtemp[:,i]).count('O')>0 and list(boardtemp[:,i]).count('X')==0:
            c=list(boardtemp[:,i]).count('O')
            o[c]+=1
   
    final= 6*x[2]+3*x[1]+x[0]-6*o[2]-3*o[1]-o[0]
   # print (final)
    return final

def Medium_EvaluationFunction(board):
    #Evaluation function used : o[2]-o[3] 
    #wherer, o[i] : “i” number of number of O’s vertically, horizontally and diagonally, without any X’s

    boardtemp=copy.deepcopy(board)
    boardtemp=np.array(board)
    if CheckWin(board)!=False:
        if CheckWin(board)=='X':
            return 1000
        elif CheckWin(board)=='O':
            return -1000
    x=[0,0,0,0]
    o=[0,0,0,0]

    #Count x1,x2,x3,o1,o2,o3 for 45 degree diagonal
    if list(np.diag(boardtemp)).count('X')>0 and list(np.diag(boardtemp)).count('O')==0:
        c=list(np.diag(boardtemp)).count('X')
    if list(np.diag(boardtemp)).count('O')>0 and list(np.diag(boardtemp)).count('X')==0:
        c=list(np.diag(boardtemp)).count('O')
        #print ("O diag",c)
        o[c-1]+=1

    #Count o1,o2,o3 for 135 degree diagonal
    if list(np.diag(np.fliplr(boardtemp))).count('X')>0 and list(np.diag(np.fliplr(boardtemp))).count('O')==0:
        c=list(np.diag(np.fliplr(boardtemp))).count('X')
    elif list(np.diag(np.fliplr(boardtemp))).count('O')>0 and list(np.diag(np.fliplr(boardtemp))).count('X')==0:
        c=list(np.diag(np.fliplr(boardtemp))).count('O')
        #print ("O rev diag",c)
        o[c-1]+=1

    #Count o1,o2,o3 for all rows
    for i in range(4):
        if list(boardtemp[i]).count('X')>0 and list(boardtemp[i]).count('O')==0:
            c=list(boardtemp[i]).count('X')
        elif list(boardtemp[i]).count('O')>0 and list(boardtemp[i]).count('X')==0:
            c=list(boardtemp[i]).count('O')
            o[c]+=1

    #Count o1,o2,o3 for all columns
    for i in range(4):
        if list(boardtemp[:,i]).count('X')>0 and list(boardtemp[:,i]).count('O')==0:
            c=list(boardtemp[:,i]).count('X')
        elif list(boardtemp[:,i]).count('O')>0 and list(boardtemp[:,i]).count('X')==0:
            c=list(boardtemp[:,i]).count('O')
            o[c]+=1
   
    final= o[1]-o[2]        #-1 indexs used, o[1]= count of number of 2's, o[2]= count of number of 3's
    return final