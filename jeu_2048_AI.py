# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:20:18 2020

@author: alexa
"""

import time
import math
import numpy as np
from PyQt5 import QtCore, QtWidgets,QtGui
import random
import functools as fn

"""
2048 game with Artificial Intelligence solver

class structure:
    - Widget2048 defines Widget structure
    - Jeu defines games logic
    - AI_solver is an Artificial Intelligence that auto-solves the game
    - JeuWidget connects users inputs to game functions
    
to run the game from console:
    APP = JeuWidget(None)
    APP.show()
"""


DIRECTIONS = {"right":(0,1),"left":(0,-1),"up":(-1,0),"down":(1,0)}
DIRS = ["right","left","up","down"]
SIMULATION_NUMBER = 500 # number of simulation for AI Monte Carlo method
# tiles weighting for AI evaluation: 
CORNER = [[1,1,1,1],[1,1,1,1],[1,1,1,100],[1,1,100,200]]
PYRAMID = [[10**(i+j) for i in range(0,4)] for j in range(0,4)]
    
class Widget2048(QtWidgets.QWidget):
    """ defines grid, colors, buttons on the widget """ 
    def __init__(self, parent, width=400, gridSize=4):
        QtWidgets.QWidget.__init__(self, parent)
        self.panelHeight = 80
        self.panelWidth = 80
        self.gridSize = gridSize
        
        self.backgroundBrush = QtGui.QBrush(QtGui.QColor(0xbbada0))
        self.tileMargin = 16
        self.gridOffsetX = self.tileMargin
        self.gridOffsetY = self.panelHeight + self.tileMargin
        self.brushes={
			0:QtGui.QBrush(QtGui.QColor(0xcdc1b4)),
			1:QtGui.QBrush(QtGui.QColor(0x999999)),
			2:QtGui.QBrush(QtGui.QColor(0xeee4da)),
			4:QtGui.QBrush(QtGui.QColor(0xede0c8)),
			8:QtGui.QBrush(QtGui.QColor(0xf2b179)),
			16:QtGui.QBrush(QtGui.QColor(0xf59563)),
			32:QtGui.QBrush(QtGui.QColor(0xf67c5f)),
			64:QtGui.QBrush(QtGui.QColor(0xf65e3b)),
			128:QtGui.QBrush(QtGui.QColor(0xedcf72)),
			256:QtGui.QBrush(QtGui.QColor(0xedcc61)),
			512:QtGui.QBrush(QtGui.QColor(0xedc850)),
			1024:QtGui.QBrush(QtGui.QColor(0xedc53f)),
			2048:QtGui.QBrush(QtGui.QColor(0xedc22e)),
		}
        self.lightPen = QtGui.QPen(QtGui.QColor(0xf9f6f2))
        self.darkPen = QtGui.QPen(QtGui.QColor(0x776e65))
        self.scoreRect = QtCore.QRectF(10,10,self.panelWidth,self.panelHeight-20)
        self.hiScoreRect = QtCore.QRectF(100,10,self.panelWidth,self.panelHeight-20)
        self.resetRect = QtCore.QRectF(190,10,self.panelWidth,self.panelHeight-20)
        self.scoreLabel = QtCore.QRectF(10,25,self.panelWidth,self.panelHeight-30)
        self.hiScoreLabel = QtCore.QRectF(100,25,self.panelWidth,self.panelHeight-30)
        self.solveRect = QtCore.QRectF(280,10,self.panelWidth,self.panelHeight-20)
        self.lastPoint = None
        self.resize(QtCore.QSize(width,width+self.panelHeight))
        self.tileSize = (width-self.tileMargin*(self.gridSize+1))/self.gridSize
        self.font = QtGui.QFont('Arial',self.tileSize/4)
      
        
    def paintEvent(self,event):
        """ set colors of tiles and boxes according to their values"""
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawRect(self.rect())
        painter.setBrush(self.brushes[1])
        painter.drawRect(self.scoreRect)
        painter.drawRect(self.hiScoreRect)
        painter.drawRect(self.resetRect)
        painter.drawRect(self.solveRect)
        painter.setFont(QtGui.QFont('Arial',9))
        painter.setPen(self.darkPen)
        painter.drawText(QtCore.QRectF(10,15,80,20),'SCORE',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.drawText(QtCore.QRectF(100,15,80,20),'HIGHSCORE',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.setFont(QtGui.QFont('Arial',15))
        painter.setPen(self.lightPen)
        painter.drawText(self.resetRect,'RESET',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.drawText(self.solveRect,'SOLVE',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.setFont(QtGui.QFont('Arial',15))
        painter.setPen(self.lightPen)
        painter.drawText(self.scoreLabel,str(int(self.score)),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.drawText(self.hiScoreLabel,str(int(self.hiScore)),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.setFont(self.font)
        for gridX in range(0,self.gridSize):
            for gridY in range(0,self.gridSize):
                tile = int(self.tiles[gridX][gridY])
                if tile == 0:
                    painter.setBrush(self.brushes[0])
                else:
                    painter.setBrush(self.brushes[tile])
                rect = QtCore.QRectF(self.gridOffsetX+gridX*(self.tileSize+self.tileMargin),
                                       self.gridOffsetY+gridY*(self.tileSize+self.tileMargin),
                                       self.tileSize,self.tileSize)
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawRect(rect)
                if tile != 0:
                    painter.setPen(self.darkPen if tile<16 else self.lightPen)
                    painter.drawText(rect,str(tile),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.end()
        

class Jeu:
    """ contains game's logic: moves in order to play at 2048 """
    def __init__(self, gridSize = 4):
        self.gameRunning = False
        self.gridSize =gridSize
        self.hiScore = 0
        self.reset_game()

    def add_tile(self,tiles):
        """ adds randomly a 2 in the grid at each iteration, 10% chances it's a 4 """
        zeros = np.argwhere(tiles == 0)
        if zeros.any():
            value = 2 if random.random()<0.9 else 4 
            ind = zeros[int(random.random()*len(zeros))]
            indx = ind[0]
            indy = ind[1]
            tiles[indx][indy] = value
        return tiles
    
    def reset_game(self):
        """ resets the game: clears board and adds two tiles"""
        self.tiles = np.zeros((self.gridSize,self.gridSize))
        self.availableSpots = list(range(0,self.gridSize**2))
        self.score = 0
        self.add_tile(self.tiles)
        self.add_tile(self.tiles)
        self.gameRunning = True        
    
    def game_state(self,tiles):      
        """ looks for available shots to find out if game over or not """
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
            
    
    def update_tiles(self):
        """ updates the value of the boxes and adds a 2 or 4""" 
        self.availableSpots = []
        for i in range(0,self.gridSize):
            for j in range(0,self.gridSize):
                if self.tiles[i][j] == 0:
                    self.availableSpots.append(i+j*self.gridSize)
        self.add_tile(self.tiles)
        self.hiScore = max(self.score,self.hiScore)
        self.update()
        # if no move available -> game over
        if not self.game_state(self.tiles):
            self.add_tile(self.tiles)
            self.gameRunning = False
            QtWidgets.QApplication.processEvents()
            QtWidgets.QMessageBox.information(self,'','Game Over')
            
    def rotate_matrix(self,mat):
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

                
    def rotate_matrix_multiple(self,mat,times):
        """ numerous rotations """
        for i in range(0,times):
            self.rotate_matrix(mat)
    
    def rotate(self,mat,d):
        """ rotates tiles so that the move is equivalent to moving left """
        times = 0
        if d[1] == 1: #right
            times = 2
        elif d[0] == -1: #up
            times = 3
        elif d[0] == 1: #down
            times = 1
        self.rotate_matrix_multiple(mat,times)
        return mat
    
    def rotate_back(self,tiles,d):
        """ rotates back after the movement """
        times = 0
        if d[1] == 1: #right
            times = 2
        elif d[0] == -1: #up
            times = 1
        elif d[0] == 1: #down
            times = 3
        self.rotate_matrix_multiple(tiles,times)
        return tiles                                
        
    def move_left(self,tiles):
        """ moves all the tiles to the left if it is possible """
        moved = False
        score = 0
        for gridX in range(1,len(tiles)):
            for gridY in range(0,len(tiles)):
                if tiles[gridX][gridY] != 0: # continues if tile is non zero
                    i = gridX
                    while i-1>=0 and tiles[i-1][gridY] == 0: # go all over null tiles
                       i -= 1
                    if i-1>=0 and tiles[i-1][gridY] == tiles[gridX][gridY]: # merge tiles with the same value
                        score += tiles[gridX][gridY]*2
                        tiles[i-1][gridY] *= 2
                        tiles[gridX][gridY] = 0
                        moved = True
                    elif i<gridX: # replaces tiles
                        tiles[i][gridY] = tiles[gridX][gridY]
                        tiles[gridX][gridY] = 0
                        moved = True
            
        return moved,tiles,score
        
    def moves(self,tiles,direction):
        """ moves all the tiles in requested directions """
        d = DIRECTIONS[direction]
        rotated_tiles = self.rotate(tiles,d)
        moved,new_tiles,score = self.move_left(rotated_tiles)
        new_tiles = self.rotate_back(new_tiles,d)
        return new_tiles, moved, score
        
    def move_tiles(self,direction):
        """ performs moves in the requested direction """
        self.tiles,moved,score = self.moves(self.tiles,direction)
        self.score += score
        if moved:
            self.update_tiles()
            
    def up(self):
        self.up = fn.partial(self.move_tiles,direction="up")
            
    def down(self):
        self.down = fn.partial(self.move_tiles,direction="down")

    def right(self):
        self.right = fn.partial(self.move_tiles,direction="right")

    def left(self):
        self.left = fn.partial(self.move_tiles,direction="left")                


class AI_solver(Jeu):
    """
    Artificial Intelligence to solve 2048 game
    Several resolution methods can be used : Monte-Carlo or scoring methods with 
    different heuristics (Corner, Pyramid, Merge or Snake) 
    """
    def __init__(self):
        Jeu.__init__(self)
        QtWidgets.QApplication.processEvents()
        
    def get_score(self,tiles,first_dir,method):
        """ gets score according to the method chosen for resolution """
        scoring_methods = ["corner","pyramid","empty","snake","merge","compound"]
        if method == "montecarlo":
            return self.get_score_montecarlo(tiles,first_dir)
        elif method in scoring_methods:
            return self.get_score_scoring(tiles,first_dir,method)
        
    def get_score_montecarlo(self,tiles,first_dir):
        """
        Given a board and a first move, gets a score by playing N_simulation random game
        The score is evaluated by averaging the maximum tile obtained in each simulation
        """
        stiles = tiles.copy()
        stiles, moved, score = self.moves(stiles, first_dir)
        if not moved:
            return -1
        total_score = 0
        max_tile = 0
        for i in range(SIMULATION_NUMBER):
            game_score = score
            simulation_tiles = tiles.copy()
            simulation_tiles = self.add_tile(simulation_tiles)
            while self.game_state(simulation_tiles) == True:
                simulation_tiles,moved,move_score = self.moves(simulation_tiles,DIRS[random.randint(0, 3)])
                if moved:
                    simulation_tiles = self.add_tile(simulation_tiles)
                game_score += move_score
            total_score += game_score
            max_tile += np.max(simulation_tiles)
            
        return max_tile / SIMULATION_NUMBER #returns the macimum tile obtained on average
    
    def get_score_scoring(self,tiles,first_dir,method):
        """ 
        Given a board and a first move, gets a score by playing one game
        The score is evaluated by comparison with an heuristic pattern specified
        in the 'method' argument
        """
        stiles = tiles.copy()
        stiles, moved, score = self.moves(stiles, first_dir)
        stiles = self.add_tile(stiles)
        if not moved:
            return False
        return self.evaluation(stiles,score,method)        

    def evaluation(self,tiles,score,method):
        """ evaluates the board score according to the chosen heuristics"""
        if method == "corner":
            # gives point to configurations with bigger values in the bottom-right hand corner
            return np.sum(tiles*CORNER)
        
        elif method == "pyramid":
            # gives point to configurations with ascending values in pyramidal 
            # organization towards the bottom-right hand corner 
            return np.sum(tiles*PYRAMID)
        
        elif method == "empty":
            # gives 1 point per empty cell
            return self.gridSize**2 - len(np.argwhere(self.tiles))
        
        elif method == "snake":
            # gives point to configurations with ascending values organized in a 
            # snake-like pattern
            snake = []
            for i,col in enumerate(zip(*tiles)):
                snake.extend(reversed(col) if i%2 == 0 else col)                
            m = max(snake)
            return sum(x/10**n for n,x in enumerate(snake)) - math.pow((tiles[3][0] != m)*abs(tiles[3][0]-m),2)
               
        elif method == "merge":
            # gives point to configurations that merged tiles compared to precedent 
            # step
            return max(score,1)
        
        elif method == "compound":
            # takes into account the merge and snake methods
            # score = snake_score + k*merge_score
            snake_score = self.evaluation(tiles,score,"snake")
            merge_score = self.evaluation(tiles,score,"merge")
            print("Score de snake: " + str(snake_score))
            print("Score de merge: " + str(merge_score))
            k = 1
            return snake_score + k*merge_score
            
        
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
        Uses the specified method to solve the game
        """
        N=0
        tic = time.perf_counter()
        while self.game_state(self.tiles):
            move = self.get_best_move(self.tiles,method)
            self.move_tiles(move)
            self.update()
            QtWidgets.QApplication.processEvents() #updates the Widget
            N+=1
            time.sleep(0.1)
        toc = time.perf_counter()
        print("Nombre de coups joués:" + str(N))
        print("Temps écoulé:" + str(toc-tic)+"s")
        time.sleep(1)
        return self.score, np.max(self.tiles),toc-tic,N
           
class JeuWidget(Widget2048,AI_solver):
    """ 
    Link between class AI_solver and class Widget2048,
    Connects the keyboard and mouse inputs to AI_solver's functions
    """
    def __init__(self,parent):
        Widget2048.__init__(self, parent)
        AI_solver.__init__(self)
        QtWidgets.QApplication.processEvents()                     
                
    def keyPressEvent(self,e):
        """ link between key press and event (left, right, down, up)"""
        if not self.gameRunning:
            return
        if e.key() == QtCore.Qt.Key_Escape:
            self.reset_game()
        elif e.key() == QtCore.Qt.Key_Up:
            self.up()
        elif e.key() == QtCore.Qt.Key_Down:
            self.down()
        elif e.key() == QtCore.Qt.Key_Left:
            self.left()
        elif e.key() == QtCore.Qt.Key_Right:
            self.right()
            
    def mousePressEvent(self,e):
        """ detects if button is clicked """
        self.lastPoint = e.pos()
        
    def mouseReleaseEvent(self,e):
        """ acts if button clicked """
        if self.resetRect.contains(self.lastPoint.x(),self.lastPoint.y()) and self.resetRect.contains(e.pos().x(),e.pos().y()):
            if QtWidgets.QMessageBox.question(self,'','Are you sure you want to start a new game?')==QtWidgets.QMessageBox.Yes:
                self.reset_game()
        elif self.solveRect.contains(self.lastPoint.x(),self.lastPoint.y()) and self.solveRect.contains(e.pos().x(),e.pos().y()):
            reply = QtWidgets.QMessageBox.question(self,'','Do you want to solve the game with Snake (Yes) or Monte-Carlo (No) method?')
            if reply == QtWidgets.QMessageBox.No:
                self.auto_solve("montecarlo")
            elif reply == QtWidgets.QMessageBox.Yes:
                self.auto_solve("snake")
                
class Stats(JeuWidget):
    """
    Computes statistical analysis over AI_solver's performances 
    Launches runs of several games
    """
    def __init__(self,parent, N_trials = 1000, method = "compound"):
        JeuWidget.__init__(self,parent)
        self.N_trials = N_trials
        self.method = method
        
    def run_stat(self):
        data_score = []
        data_max_tile = []
        data_time = []
        data_N_moves = []

        for i in range(0,self.N_trials):
            score,max_tile,t,N_moves = self.auto_solve(self.method)
            data_score.append(score)
            data_max_tile.append(max_tile)
            data_time.append(t)
            data_N_moves.append(N_moves)
            self.reset_game()
            print("Simulation " + str(i))
        
        return data_score, data_max_tile, data_time, data_N_moves
    
    def save_data(self, filename,data_score, data_max_tile, data_time, data_N_moves):      
        """ writes data in textfile """
        f = open(filename, "w")
        f.write("# score max_tile time N_moves\n")        # column names
        np.savetxt(f, np.array([data_score,data_max_tile,data_time,data_N_moves]).T)
         
    def load_data(self,file_name):
        """ reads data from file """
        data_score, data_max_tile, data_time, data_N_moves = np.loadtxt(file_name, unpack=True)
        
        
               
# To run the game from console or terminal : 
if __name__=='__main__':
    APP = QtWidgets.QApplication.instance()
    IS_STANDARD_CONSOLE = (APP is None)
    print('running')
    if IS_STANDARD_CONSOLE: # launched from standard console (not ipython console)
        print('running in console')
        APP = QtWidgets.QApplication(["test"])
    M = JeuWidget(None)
    M.show()
    if IS_STANDARD_CONSOLE:
        APP.exec_()
        