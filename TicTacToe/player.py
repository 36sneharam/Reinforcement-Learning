import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import time
import TicTacToeEnvironment
import os
import seaborn as sns

class player:
    def __init__(self, env, val = 1):
        self.env = env 
        self.val = val

    #Q table methods 
    def initqtable(self, file = "qtable.txt"):
        if os.path.getsize(file) == 0:
            self.qtable = self.genqtable(base = self.env.dim)
        else:
            self.qtable = self.readqtable(file)
    def genqtable(self, base = 2):
        board_size = self.env.board_size
        qtable = np.zeros((base**(board_size**2), (board_size**2)))
        self.qtable = (qtable)
    def saveqtable(self, file = "qtable.txt"):
        f =  open(file, 'w')
        np.savetxt(f, self.qtable)
        f.close()
    def readqtable(self, file = "qtable.txt"):
        return np.loadtxt(file)


    
    def train(self, mode = "Random", epsilon = 0.1, gamma = 1, games = 4000):
        game = self.env
        if mode == "Random": 
            for g in range(games):
                game.initgame(gamemod = "Random")
                game_status = False
                while game_status == False:
                    game_status = self.singletrain(gamma = gamma, epsilon = epsilon)
        if mode == "HumanGame":
            realdata = game.realdata 
            nboard = len(realdata[0]) #Number of boards 
            for g in range(nboard):
                for i in range(games): 
                    game.board = realdata[1][g]
                    game_status = False
                    while game_status == False:
                        game_status = self.singletrain(gamma = gamma, epsilon = epsilon)
        if mode == "MistakeLearn":
            realdata = game.realdata
            nboard = len(realdata[0])
            for g in range(nboard):
                game.board = realdata[1][g]
                pos = list(map(int, realdata[0][g]))

                val = int(realdata[2][g])
                
                self.singletrain(pos = pos, epsilon = epsilon, gamma = gamma, val = val)

        


    def singletrain(self, pos = "Default", epsilon = 0.1, gamma = 1, val = "Default"):
        r = []
        if val == "Default":
            val = self.val 
        #game_status = False
        game = self.env
        #Determine position
        if pos == "Default":
            ran = random.random()
            if ran > epsilon:
                        
                x = random.randint(0, game.board_size-1)
                y = random.randint(0, game.board_size-1)
                pos = [x,y]
            else:
                idx = np.argmax(self.qtable[int(game.getstateid())])
                pos = game.actidtopos(idx)

        total_reward = 0
        reward, game_status = game.fill(pos, val)
        total_reward += reward
        
        if np.sum(game.board) >= game.board_size**2:
            q_next = 0 
        else:
            q_next = (self.qtable[int(game.getstateid())].max())
        self.qtable[int(game.getstateid()), game.actpostoid(pos)] = reward+ gamma*q_next
        return game_status

    def check_accuracy(self, safety = False, showfail = False):
        dim = self.env.board_size
        correct = 0 
        wrong = 0
        for i in range(0, 2**(dim)**2):
            #Generate board
            flatarr = (np.array(list((bin(i)[2:])))).astype('int') 
            pad = np.zeros(int((dim**2)-len(flatarr)))
            flatarrpad = (np.concatenate((flatarr, pad)))
            arr = np.reshape(flatarrpad, (dim, dim))
        
            if np.all(arr) != 1:
                #Check accuracy of next move 
                [x,y] = self.predict_action(board = arr, safety = safety)
                if arr[x,y] == 0:
                    correct+=1
                else:
                    if showfail == True:
                        print(arr)
                        print([x,y])
                    wrong+= 1
            
        #Calculate Error Rate 
        err = correct/(correct+wrong)
        return(err)
    
    def predict_action(self, board = "Current", safety = True):
        if board == "Current":
            board = self.env.board
            #print(board)
        idx = self.env.getstateid(board)
        #print(self.qtable)
        actid = np.argmax((self.qtable[int(idx)]))
        pos = self.env.actidtopos(int(actid))
        #Check if predicted state is occupied 
        [x,y] = pos 
        if safety == True:
            qrow = self.qtable[int(idx)]
            arglist = np.argsort(qrow)
            i = 1
            while board[x,y] != 0:
                actid = arglist[-i]
                pos = self.env.actidtopos(int(actid))
                [x,y] = pos
                
                i = i+1

                if(i == len(qrow)):
                    break
        return (pos)
    
    def play1move(self, record = True):
        
        pos = self.predict_action()
        if record == True:
            self.last_move = pos
        print(pos)
        self.env.fill(pos, val = self.val)

        #self.env.dispboard()
    def baseplay(self, random = False):
        self.env.initgame(random)
        steps = 0
        while self.env.checkwin() == False:
            self.env.dispboard()
            #print(self.env.checkwin())
            self.play1move()
            steps += 1
            if steps > 20:
                break
        self.env.dispboard()
        return steps
    
    #Hyperparameter Optimization Methods 
    def gridop(self):
        epsilon = np.linspace(0, 1, 10)
        acc = []
        for i in range(len(epsilon)):
            self.train(epsilon = i)
            acc.append(self.check_accuracy())
        plt.plot(epsilon, acc, 'o')

class ticplayer:
    #Initialization 
    def __init__(self, env, playerclass, val, games = 2000, gamma = 0.2, epsilon =0.1):
        self.env = env #Importing environment 
        self.playerclass = playerclass #Importing player class
        self.val = val
        self.games = games 
        self.gamma = gamma 
        self.epsilon = epsilon
        self.player = self.initplayer()

    def initplayer(self, qtablefile = "qtable.txt"):
        p = self.playerclass(self.env, val = self.val)
        #p.genqtable(base = 3)
        p.initqtable(qtablefile)
        p.train(games = self.games, gamma = self.gamma, epsilon = self.epsilon)
        p.train(mode = "HumanGame", games = 200, gamma = self.gamma, epsilon = self.epsilon)
        p.train(mode = "MistakeLearn", gamma = self.gamma, epsilon = self.epsilon)
        p.saveqtable(qtablefile)
        return p