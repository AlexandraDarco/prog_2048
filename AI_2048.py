# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:45:08 2020

@author: cecil
"""

from jeu2048 import Jeu,Tile

class AI_solver(Jeu):
    def __init__(self):
        Jeu.__init__(self,gridSize=4)
        
    def get_score(tiles,first_dir):
        """
        Given a board and a first move, get a score by playing N_simulation random game
        """
        
        stiles = tiles.copy()
        
        
        
AI = AI_solver()
        