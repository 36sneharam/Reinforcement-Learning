import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import time
from TicTacToeEnvironment import *
from player import *



def gethumanplay():
	s = input("Enter position to play")
	pos = list(map(int, s.split()))
	return (pos)



def HumanGame(game, tplayer):
	game.initgame(gamemod = "Zeros")
	game.drawboard()
	while game.checkstatus() == "Nowin":
		print("Move by computer")
		cbrd = game.board
		cpos = (tplayer.player.predict_action())
		print(cbrd)
		game.saverealdata(cpos, cbrd, tplayer.player.val)
		tplayer.player.play1move()
		game.drawboard()
		if game.checkstatus() != "Nowin":
			break 
		print("Move by user")
		upos = gethumanplay()
		uval = 1
		ubrd = game.board
		game.saverealdata(upos, ubrd, uval)
		game.updateboard(upos, uval)
		game.drawboard()

	print("Final Board")
	game.drawboard()
	print(game.checkstatus())

def TwoCompGame(game, tplayer1, tplayer2, disp = True):
	game.initgame(gamemod = "Zeros")
	game.drawboard()
	while game.checkstatus() == "Nowin":
		if disp == True:
			print("Move by computer A")
		Abrd = game.board
		Apos = (tplayer1.player.predict_action())
		game.saverealdata(Apos, Abrd, tplayer1.player.val)
		tplayer1.player.play1move()
		if disp == True:
			game.drawboard()
		if game.checkstatus() != "Nowin":
			break 
		if disp == True:
			print("Move by computer B")
		Bbrd = game.board
		Bpos = (tplayer2.player.predict_action())
		game.saverealdata(Bpos, Bbrd, tplayer2.player.val)
		tplayer2.player.play1move()
		if disp == True:
			game.drawboard()
		if game.checkstatus() != "Nowin":
			break
	return (game.checkstatus()) 

tgame = tictactoe(3)
tp = ticplayer(tgame, player, 2 , games = 500)
for _ in range(3):
	HumanGame(tgame, tp)
"""
result = []
for _ in range(10):
	tgame = tictactoe(3)
	tp1 = ticplayer(tgame, player, 2, games = 1000)
	tp2 = ticplayer(tgame, player, 1, games = 1000)
	#Have two tictactoe player play together 
	result.append(TwoCompGame(tgame, tp1, tp2, disp = False))
result = pd.Series(result, name="x variable")
ax = sns.distplot(result)
plt.show()
"""
