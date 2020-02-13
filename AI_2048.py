# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:45:08 2020

@author: cecil
"""
import numpy as np
import random
from jeu2048_v2 import Jeu

## FONCTIONS
DIRS = ["right","left","up","down"]
DIRECTIONS = {"right":(0,1),"left":(0,-1),"up":(-1,0),"down":(1,0)}
SIMULATION_NUMBER = 10

def rotateMatrix(mat):
    """rotates a N x N matrix by 90 degrees in 
    anti-clockwise direction"""
    N = len(mat)
    for x in range(0, int(N/2)): 
    # Consider elements in group    
    # of 4 in current square 
        for y in range(x, N-x-1): 
            # store current cell in temp variable 
            temp = mat[x][y] 
            # move values from right to top 
            mat[x][y] = mat[y][N-1-x] 
            # move values from bottom to right 
            mat[y][N-1-x] = mat[N-1-x][N-1-y] 
            # move values from left to bottom 
            mat[N-1-x][N-1-y] = mat[N-1-y][x] 
            # assign temp to left 
            mat[N-1-y][x] = temp 

            
def rotateMatrixMultiple(mat,times):
    """ numerous rotations """
    for i in range(0,times):
        rotateMatrix(mat)

def rotate(mat,d):
    """ rotation compared to left movement to use only one fonction move """
    times = 0
    if d[1] == 1: #right
        times = 2
    elif d[0] == -1: #up
        times = 3
    elif d[0] == 1: #down
        times = 1
    rotateMatrixMultiple(mat,times)
    return mat

def rotate_back(tiles,d):
    """ rotation back after the movement """
    times = 0
    if d[1] == 1: #right
        times = 2
    elif d[0] == -1: #up
        times = 1
    elif d[0] == 1: #down
        times = 3
    rotateMatrixMultiple(tiles,times)
    return tiles 
    
def move_left(tiles):
    """ moves all the tiles to the left if it is possible """
    moved = False
    score = 0
    for gridX in range(1,len(tiles)):
        for gridY in range(0,len(tiles)):
            if tiles[gridX][gridY] != 0:
                i = gridX
                while i-1>=0 and tiles[i-1][gridY] == 0:
                   i -= 1
                if i-1>=0 and tiles[i-1][gridY] == tiles[gridX][gridY]:
                    score += tiles[gridX][gridY]*2
                    tiles[i-1][gridY] *= 2
                    tiles[gridX][gridY] = 0
                    moved = True
                elif i<gridX:
                    tiles[i][gridY] = tiles[gridX][gridY]
                    tiles[gridX][gridY] = 0
                    moved = True
        
    return moved,tiles,score
    
def move_test(tiles,direction):
    d = DIRECTIONS[direction]
    rotated_tiles = rotate(tiles,d)
    moved,new_tiles,score = move_left(rotated_tiles)
    new_tiles = rotate_back(new_tiles,d)
    return new_tiles, moved, score
                       
def add_tile(tiles):
    zeros = np.argwhere(tiles == 0)
    if zeros.any():
        value = 2 if random.random()<0.9 else 4 
        ind = zeros[int(random.random()*len(zeros))]
        indx = ind[0]
        indy = ind[1]
        tiles[indx][indy] = value
    return tiles

def game_state(tiles):      
    """ Look for available shots to find out if game over or not """
    zeros = np.argwhere(tiles == 0)
    if zeros.any():
        return True
    for i in range(0,len(tiles)):
        for j in range(0,len(tiles)):
            if i<len(tiles)-1 and tiles[i][j] == tiles[i+1][j]:
                return True
            if j<len(tiles)-1 and tiles[i][j] == tiles[i][j+1]:
                return True
    return False
            
##

class AI_solver(Jeu):
    def __init__(self):
        Jeu.__init__(self,gridSize=4)
        
    def get_score(self,tiles,first_dir):
        """
        Given a board and a first move, get a score by playing N_simulation random game
        """
        stiles = tiles.copy()
        stiles, moved, score = move_test(stiles, first_dir)
        if not moved:
            return -1
        total_score = 0
        for i in range(SIMULATION_NUMBER):
            game_score = score
            simulation_tiles = tiles.copy()
            simulation_tiles = add_tile(simulation_tiles)
            while game_state(simulation_tiles) == True:
                simulation_tiles,moved,move_score = move_test(simulation_tiles,DIRS[random.randint(0, 3)])
                if moved:
                    simulation_tiles = add_tile(simulation_tiles)
                game_score += move_score
            total_score += game_score
        return total_score / SIMULATION_NUMBER
    
                    
        
        
        
        
AI = AI_solver()
        