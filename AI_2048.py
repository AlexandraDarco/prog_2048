# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:45:08 2020

@author: cecil
"""
import numpy as np
import random
import time
from multiprocessing.pool import Pool
import functools as fn
from PyQt5 import QtCore, QtWidgets,QtGui
from jeu2048_v2 import Jeu,JeuWidget

## 
DIRS = ["right","left","up","down"]
DIRECTIONS = {"right":(0,1),"left":(0,-1),"up":(-1,0),"down":(1,0)}
SIMULATION_NUMBER = 5
CORNER = [[0,0,0,0],[0,0,0,0],[0,0,0,100],[0,0,100,200]]
PYRAMID = [[2**(i+j) for i in range(0,4)] for j in range(0,4)]
##

class AI_solver(JeuWidget):
    def __init__(self,parent):
        JeuWidget.__init__(self,parent)
        QtWidgets.QApplication.processEvents()
        
    def get_score(self,tiles,first_dir,method):
        """
        Given a board and a first move, get a score by playing N_simulation random game
        """
        stiles = tiles.copy()
        stiles, moved, score = self.move(stiles, first_dir)
        if not moved:
            return -1
        total_score = 0
        for i in range(SIMULATION_NUMBER):
            game_score = score
            simulation_tiles = tiles.copy()
            simulation_tiles = self.add_tile(simulation_tiles)
            while self.game_state(simulation_tiles) == True:
                simulation_tiles,moved,move_score = self.move(simulation_tiles,DIRS[random.randint(0, 3)])
                evaluated_score = self.evaluation(tiles,move_score,method)
                if moved:
                    simulation_tiles = self.add_tile(simulation_tiles)
                game_score += evaluated_score
            total_score += game_score
        return total_score / SIMULATION_NUMBER

    def evaluation(self,tiles,move_score,method):
        if method == "score":
            return move_score
        elif method == "corner":
            return np.sum(tiles*CORNER_MAT)
        elif method == "pyramid":
            return np.sum(tiles*PYRAMID)
        
    def get_best_move(self,tiles,method):
        """ 
        Should I move left,right,up or down?"
        """
        results = []
        for d in DIRS:
            results.append(self.get_score(tiles,d,method))
        return DIRS[results.index(max(results))]
#        my_fun = self.get_score
#        mat = self.tiles
#        with Pool(4) as p:
#            results = p.starmap(self.get_score,[(self.tiles,DIRS[0]),(self.tiles,DIRS[1]),
#                                                (self.tiles,DIRS[2]),(self.tiles,DIRS[3])])  
#            results = p.starmap(my_fun,[(mat,DIRS[0]),(mat,DIRS[1])])
#            return DIRS[results.index(max(results))]                                  
        
    def play_move(self,method):
        """
        Moves in best direction
        """
        move = self.get_best_move(self.tiles,method)
        self.move_tiles(move)
        
    def play_moves(self,N,method):
        """
        Move N times in best direction
        """
        for i in range(0,N):
            self.play_move(method)
            self.update()
        
    def auto_solve(self,method):
        """
        Joue 10 coups tout seul
        On update le painter après chaque move pour voir l'AI jouer en direct
        Mais ça ne marche pas...
        """
        N=0
        tic = time.perf_counter()
        while self.game_state(self.tiles):
#        while N<10:
            move = self.get_best_move(self.tiles,method)

#        while self.game_state(self.tiles):
        while N<100:
            move = self.get_best_move(self.tiles)
            self.move_tiles(move)
            self.update()
            QtWidgets.QApplication.processEvents()
            N+=1
            print(N)
            time.sleep(0.2)
        toc = time.perf_counter()
        print("Nombre de coups joués:" + str(N))
        print("Temps écoulé:" + str(toc-tic)+"s")
        time.sleep(1) # arrête le programme 1s après chaque coup pour qu'on voit l'AI jouer
    
        
AI = AI_solver(None)
AI.show()
AI.auto_solve("corner") #fait jouer l'AI tout seul 10 coups
