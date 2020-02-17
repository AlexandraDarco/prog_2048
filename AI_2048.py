# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:45:08 2020

@author: cecil
"""
import numpy as np
import math
import random
import time
import functools as fn
from PyQt5 import QtCore, QtWidgets,QtGui
from jeu2048_v2 import Jeu,JeuWidget

## 
DIRS = ["right","left","up","down"]
DIRECTIONS = {"right":(0,1),"left":(0,-1),"up":(-1,0),"down":(1,0)}

SIMULATION_NUMBER = 100
CORNER = [[0,0,0,0],[0,0,0,0],[0,0,0,100],[0,0,100,200]]
PYRAMID = [[2**(i+j) for i in range(0,4)] for j in range(0,4)]
##

class AI_solver(JeuWidget):
    def __init__(self,parent):
        JeuWidget.__init__(self,parent)
        QtWidgets.QApplication.processEvents()
        
    def get_score(self,tiles,first_dir,method):
        """ get score according to the method chosen for resolution """
        scoring_methods = ["corner","pyramid","empty","snake"]
        if method == "montecarlo":
            return self.get_score_montecarlo(tiles,first_dir)
        elif method in scoring_methods:
            return self.get_score_scoring(tiles,first_dir,method)
        
    def get_score_montecarlo(self,tiles,first_dir):
        """
        Given a board and a first move, get a score by playing N_simulation random game
        The score is evaluated by averaging the maximum tile obtained in each simulation
        """
        stiles = tiles.copy()
        stiles, moved, score = self.move(stiles, first_dir)
        if not moved:
            return -1
        total_score = 0
        max_tile = 0
        for i in range(SIMULATION_NUMBER):
            game_score = score
            simulation_tiles = tiles.copy()
            simulation_tiles = self.add_tile(simulation_tiles)
            while self.game_state(simulation_tiles) == True:
                simulation_tiles,moved,move_score = self.move(simulation_tiles,DIRS[random.randint(0, 3)])
                if moved:
                    simulation_tiles = self.add_tile(simulation_tiles)
                game_score += move_score
            total_score += game_score
            max_tile += np.max(simulation_tiles)
            
        return max_tile / SIMULATION_NUMBER
    
    def get_score_scoring(self,tiles,first_dir,method):
        """ 
        Given a board and a first move, get a score by playing one game
        The score is evaluated by comparison with a snake-like pattern
        """
        stiles = tiles.copy()
        stiles, moved, score = self.move(stiles, first_dir)
        stiles = self.add_tile(stiles)
        if not moved:
            return False
        return self.evaluation(stiles,method)        

    def evaluation(self,tiles,method):
        """ evaluation fonction according to the methode chosen, used in get_score"""
        if method == "corner":
            return np.sum(tiles*CORNER)
        elif method == "pyramid":
            return np.sum(tiles*PYRAMID)
        elif method == "empty":
            # gives 1 point per empty cell
            return self.gridSize**2 - len(np.argwhere(self.tiles))
        elif method == "snake":
            snake = []
            for i,col in enumerate(zip(*tiles)):
                snake.extend(reversed(col) if i%2 == 0 else col)
                
            m = max(snake)
            return sum(x/10**n for n,x in enumerate(snake)) - math.pow((tiles[3][0] != m)*abs(tiles[3][0]-m),2)
               
    def get_best_move(self,tiles,method):
        """ 
        Should I move left,right,up or down?
        Tests the 4 moves and returns the one with best score
        """
        available_dirs = []
        results = []
        for d in DIRS:
            result = (self.get_score(tiles,d,method))
            if result != False:
                results.append(result)
                available_dirs.append(d)
        return available_dirs[results.index(max(results))]                                
        
    def play_move(self,method):
        """
        Moves in best direction
        """
        move = self.get_best_move(self.tiles,method)
        self.move_tiles(move)        
        
    def auto_solve(self,method):
        """
        Auto-plays the game from current tile until game over
        """
        N=0
        tic = time.perf_counter()
        while self.game_state(self.tiles):
 #       while N<10:
            move = self.get_best_move(self.tiles,method)
            self.move_tiles(move)
            self.update()
            QtWidgets.QApplication.processEvents() #updates the Widget
            N+=1
            time.sleep(0.2)
        toc = time.perf_counter()
        print("Nombre de coups joués:" + str(N))
        print("Temps écoulé:" + str(toc-tic)+"s")
        time.sleep(1)
    
        
AI = AI_solver(None)
AI.show()
AI.auto_solve("snake")
