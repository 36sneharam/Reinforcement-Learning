import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import time
import json



class tictactoe:
    convert = {0: ' ', 1: 'X', 2: 'O'} #0: empty space, 1: computer, 2: human 
    def __init__(self, dim):
        self.dim = dim
        self.board_size = self.dim
        self.initrealdata()
        self.initgame()
        return 
    
    #Dimension 
    def adddim(self, dim):
        self.dim = dim 
    def getdim(self):
        return self.dim
    
    #Board State 
    def initgame(self, gamemod = "Random"):
        if gamemod == "Zeros":
            self.board = np.zeros((self.dim, self.dim))
        elif gamemod == "Random": 
            self.board = np.random.randint(0, 3, size = (self.dim, self.dim))
        else:
        	print("Something went wrong")
        #self.board[0,0] = 1
    def getboardstate(self):
        return self.board
    def addboardstate(self, state):
        self.board = (state)
        #Make sure dimension of board is self consistent 
        self.adddim(self.getboardstate().shape[0])
        

    #Visualizing the board   
    def drawboard(self):
        #Checking for correct dimension
        dim = self.dim 
        #self.board = np.zeros((self.dim, self.dim))
        board_state = self.getboardstate()
        for i in range(dim):
            for j in range(dim -1):
                print("  | "+self.convert[board_state[i,j]], end = '')
            print(" | "+self.convert[board_state[i,dim-1]]+" | ")
            if i != dim-1:
                print('_'*dim*6)
    #Data
    #Init data 
    def initrealdata(self, filepos = 'realpos.txt', fileboard = 'realboard.txt', fileval = 'realval.txt'):
    	self.realdata = self.readrealdata(filepos, fileboard, fileval)

    #Saving real games in a data set 
    def saverealdata(self, pos, board, val, filepos = 'realpos.txt' ,fileboard = "realboard.txt", fileval = "realval.txt"):
    	self.realdata.append([pos, board])
    	#Saving it to file 
    	f =  open(fileboard, 'a')
    	np.savetxt(f, board)
    	f.close()

    	g = open(filepos, 'a')
    	np.savetxt(g, np.array(pos))
    	g.close()

    	h = open(fileval, 'a')
    	np.savetxt(h, np.array([val]))
    	h.close()

    def readrealdata(self, filepos = 'realpos.txt' ,fileboard = "realboard.txt", fileval = "realval.txt"):
    	pos = (list(np.loadtxt(filepos).reshape(-1,2)))
    	boards = (list(np.loadtxt(fileboard).reshape(-1, self.dim, self.dim)))
    	val = (list(np.loadtxt(fileval).reshape(-1, 1)))
    	return [pos, boards, val]

    def clearfile(self, file):
    	open(file, w).close()

    #Check
    def checkrow(self, board):     
        #Check if row has the same symbol
        for i in range(0, board.shape[0]):
            if (np.any(board[i,:] != 0)):
                if (np.all(board[i,:]==1)):
                    return "1win"
                elif (np.all(board[i,:]==2)):
                    return "2win"
        return "Nowin"
    def checkcolumn(self, board):
        return self.checkrow(np.transpose(board))
    def getdiagonal(self, board):
        l = board.shape[0]
        output = np.zeros((2,l))
        for i in range(0, (l)):
            output[0,i] = board[i,i]
            output[1,i] = board[i, l-1-i]
        return output
    def checkdiagonal(self, board):
        return self.checkrow(self.getdiagonal(board))
    def checkwin(self, board):
        if self.checkrow(board) != "Nowin":
            return self.checkrow(board)
        if self.checkcolumn(board) != "Nowin":
            return self.checkcolumn(board)
        if self.checkdiagonal(board) != "Nowin":
            return self.checkdiagonal(board)
        return "Nowin"
    def checkdraw(self, board):
        if (np.all(board != 0)) and self.checkwin(board) == "Nowin":
            return "Draw"
        else:
            return self.checkwin(board)
    def checkstatus(self, board = "Default"):
        if board == "Default":
            board = self.getboardstate()
        #Check if there is a draw 
        if self.checkdraw(board) == "Draw":
            return "Draw"
        else:
            return self.checkwin(board)
    def checkblock(self, pos, board = "Default"):
        if board == "Default":
            board = self.getboardstate()
        [x,y] = pos 

        if board[x,y] == 1:
        	og = 1
        	swap = 2 
        elif board[x,y] == 2:
        	og = 2
        	swap = 1 
        else: 
        	og = 0
        	swap = 0
        board[x,y] = swap
        if self.checkstatus(board) == "1win" or self.checkstatus(board) == "2win":
            out =  "Block"
        else:
            out = "NoBlock"
        board[x,y] = og
        return out
    
    #Update board
    def updateboard(self, pos, val):
        [i,j] = pos
        board = self.getboardstate()
        board[i,j] = val 
        self.addboardstate(board)
    
    def fill(self, pos, val):
        
        #Check if board is filled 
        [x,y] = pos 
        r = 0

        if self.board[x,y]==0:
            r+=1
            self.updateboard(pos, val)
            
			
            status = self.checkstatus(self.getboardstate())
            
            if val == 1:
	            #Check if A wins
	            if  status == "1win":
	                r +=2 
	            #Check if B wins
	            elif status == "2win":
	                r -=2  
	            #Check if there is a Draw
	            elif status == "Draw":
	                r +=1 
	            else:
            		r-= 4
	            #Check if there is a block 
	            if self.checkblock([x,y]) == "Block":
	                r+= 2
            if val == 2:
	            if  status == "2win":
	                r +=2 
	            #Check if B wins
	            elif status == "1win":
	                r -=2  
	            #Check if there is a Draw
	            elif status == "Draw":
	                r +=1 
	            else:
            		r-= 4
	            #Check if there is a block 
	            if self.checkblock([x,y]) == "Block":
	                r+= 2

        return (r, self.checkstatus(self.getboardstate()))
    
    #Identification
    def getstateid(self, board = "Defined"):
        if board == "Defined":
            board = self.getboardstate()
        id = 0
        for i in range(len(board.flatten())):
            id += (3**i)*board.flatten()[i]
        return id 
    
    def actidtopos(self, id):
        col = id%(self.dim)
        row = (int((id)/(self.dim)))
        return [row,col]
    
    def actpostoid(self, pos):
        [x,y] = pos 
        return (self.dim)*x + y
    

    