# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 12:11:48 2020
@author: cecil
"""

import numpy as np
from PyQt5 import QtCore, QtWidgets,QtGui
import random
import functools as fn

DIRECTIONS = {"right":(0,1),"left":(0,-1),"up":(-1,0),"down":(1,0)}

    
class Widget2048(QtWidgets.QWidget):
    """ defines grid, colors, buttons on the widget """ 
    def __init__(self, parent, width=340, gridSize=4):
        QtWidgets.QWidget.__init__(self, parent)
        self.panelHeight = 80
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
        self.scoreRect = QtCore.QRectF(10,10,80,self.panelHeight-20)
        self.hiScoreRect = QtCore.QRectF(100,10,80,self.panelHeight-20)
        self.resetRect = QtCore.QRectF(190,10,80,self.panelHeight-20)
        self.scoreLabel = QtCore.QRectF(10,25,80,self.panelHeight-30)
        self.hiScoreLabel = QtCore.QRectF(100,25,80,self.panelHeight-30)
        self.lastPoint = None
        self.resize(QtCore.QSize(width,width+self.panelHeight))
      
    def resizeEvent(self,e):
        width = min(e.size().width(),e.size().height()-self.panelHeight)
        self.tileSize = (width-self.tileMargin*(self.gridSize+1))/self.gridSize
        self.font = QtGui.QFont('Arial',self.tileSize/4)
        
        
    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawRect(self.rect())
        painter.setBrush(self.brushes[1])
        painter.drawRect(self.scoreRect)
        painter.drawRect(self.hiScoreRect)
        painter.drawRect(self.resetRect)
        painter.setFont(QtGui.QFont('Arial',9))
        painter.setPen(self.darkPen)
        painter.drawText(QtCore.QRectF(10,15,80,20),'SCORE',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.drawText(QtCore.QRectF(100,15,80,20),'HIGHSCORE',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.setFont(QtGui.QFont('Arial',15))
        painter.setPen(self.lightPen)
        painter.drawText(self.resetRect,'RESET',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
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

class Jeu:
    def __init__(self, gridSize = 4):
        self.gameRunning = False
        self.gridSize =gridSize
        self.hiScore = 0
        self.reset_game()
        
    def reset_game(self):
        self.tiles = np.zeros((self.gridSize,self.gridSize))
        self.availableSpots = list(range(0,self.gridSize**2))
        self.score = 0
        self.addTile()
        self.addTile()
        #self.update()
        self.gameRunning = True
        
    def addTile(self):
        """ add randomly a 2 in the grid at each iteration, 10% chances it's a 4 """
        if len(self.availableSpots)>0:
            value = 2 if random.random()<0.9 else 4 
            ind = self.availableSpots.pop(int(random.random()*len(self.availableSpots)))
            print(self.tiles)
            print(ind)
            indx = ind%self.gridSize
            indy = ind//self.gridSize
            self.tiles[indx][indy] = value
            
    def movesAvailable(self):
        """ Look for available shots to find out if game over or not """
        if not len(self.availableSpots)==0:
            return True
        for i in range(0,self.gridSize):
            for j in range(0,self.gridSize):
                if i<self.gridSize-1 and self.tiles[i][j] == self.tiles[i+1][j]:
                    return True
                if j<self.gridSize-1 and self.tiles[i][j] == self.tiles[i][j+1]:
                    return True
        return False
    
    def updateTiles(self):
        """ update the value of the boxes following the move made:
         and add a 2 or 4""" 
        self.availableSpots = []
        for i in range(0,self.gridSize):
            for j in range(0,self.gridSize):
                if self.tiles[i][j] == 0:
                    self.availableSpots.append(i+j*self.gridSize)
        self.addTile()
        self.hiScore = max(self.score,self.hiScore)
        self.update()
        # si plus de coup dispo -> game over
        if not self.movesAvailable():
            self.gameRunning = False  
            QtWidgets.QMessageBox.information(self,'','Game Over')
            
    def rotateMatrix(self,mat):
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

                
    def rotateMatrixMultiple(self,mat,times):
        """ numerous rotations """
        for i in range(0,times):
            self.rotateMatrix(mat)
    
    def rotate(self,mat,d):
        """ rotation compared to left movement to use only one fonction move """
        times = 0
        if d[1] == 1: #right
            times = 2
        elif d[0] == -1: #up
            times = 3
        elif d[0] == 1: #down
            times = 1
        self.rotateMatrixMultiple(mat,times)
        return mat
    
    def rotate_back(self,tiles,d):
        """ rotation back after the movement """
        times = 0
        if d[1] == 1: #right
            times = 2
        elif d[0] == -1: #up
            times = 1
        elif d[0] == 1: #down
            times = 3
        self.rotateMatrixMultiple(tiles,times)
        return tiles                                
        
#    def move(self,direction):
#        """ rotate, move, rotate back ; depends on the direction """
#        tiles = np.array(self.tiles)
#        direction = DIRECTIONS[direction]
#        #rotates matrix
#        tiles = self.rotate(tiles,direction) 
#        #moves
#        moved,tiles_moved = self.move_left(tiles.tolist())
#        if moved:
#        #rotates matrix back
#            self.tiles = self.rotate_back(np.array(tiles_moved),direction)
#            self.tiles.tolist()
#            self.updateTiles()
        
    def move_left(self,tiles):
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
        
    def move(self,tiles,direction):
        d = DIRECTIONS[direction]
        rotated_tiles = self.rotate(tiles,d)
        moved,new_tiles,score = self.move_left(rotated_tiles)
        new_tiles = self.rotate_back(new_tiles,d)
        return new_tiles, moved, score
        
    def move_tiles(self,direction):
        self.tiles,moved,score = self.move(self.tiles,direction)
        self.score += score
        if moved:
            self.updateTiles()
            
    def up(self):
        self.up = fn.partial(self.move_tiles,direction="up")
            
    def down(self):
        self.down = fn.partial(self.move_tiles,direction="down")

    def right(self):
        self.right = fn.partial(self.move_tiles,direction="right")

    def left(self):
        self.left = fn.partial(self.move_tiles,direction="left")
    
     
#    def up(self):
#        moved = False
#        for gridX in range(0,self.gridSize):
#            for gridY in range(1,self.gridSize):
#                if self.tiles[gridX][gridY] is not None:
#                    i = gridY
#                    while i-1>=0 and self.tiles[gridX][i-1] is  None:
#                        i -= 1
#                    if i-1>=0 and self.tiles[gridX][i-1].value==self.tiles[gridX][gridY].value:
#                        self.score += self.tiles[gridX][gridY].value*2
#                        self.tiles[gridX][i-1].value *= 2
#                        self.tiles[gridX][gridY] = None
#                        moved = True
#                    elif i<gridY:
#                        self.tiles[gridX][i] = self.tiles[gridX][gridY]
#                        self.tiles[gridX][gridY] = None
#                        moved = True
#        if moved:
#            self.updateTiles()
#            
#    def down(self):
#        moved = False
#        for gridX in range(0,self.gridSize):
#            for gridY in range(self.gridSize-2,-1,-1):
#                if self.tiles[gridX][gridY] is not None:
#                    i = gridY
#                    while i+1<self.gridSize and self.tiles[gridX][i+1] is None:
#                        i += 1
#                    if i+1<self.gridSize and self.tiles[gridX][i+1].value==self.tiles[gridX][gridY].value:
#                        self.score += self.tiles[gridX][gridY].value*2
#                        self.tiles[gridX][i+1].value *= 2
#                        self.tiles[gridX][gridY] = None
#                        moved = True
#                    elif i>gridY:
#                        self.tiles[gridX][i] = self.tiles[gridX][gridY]
#                        self.tiles[gridX][gridY] = None
#                        moved = True
#        if moved:
#           self.updateTiles()
#           
#    def left(self):
#        moved = False
#        for gridX in range(1,self.gridSize):
#            for gridY in range(0,self.gridSize):
#                if self.tiles[gridX][gridY] is not None:
#                    i = gridX
#                    while i-1>=0 and self.tiles[i-1][gridY] is None:
#                        i -= 1
#                    if i-1>=0 and self.tiles[i-1][gridY].value==self.tiles[gridX][gridY].value:
#                        self.score += self.tiles[gridX][gridY].value*2
#                        self.tiles[i-1][gridY].value *= 2
#                        self.tiles[gridX][gridY] = None
#                        moved = True
#                    elif i<gridX:
#                        self.tiles[i][gridY] = self.tiles[gridX][gridY]
#                        self.tiles[gridX][gridY] = None
#                        moved = True
#        if moved:
#            self.updateTiles()
#            
#    def right(self):
#        moved = False
#        for gridX in range(self.gridSize-2,-1,-1):
#            for gridY in range(0,self.gridSize):
#                if self.tiles[gridX][gridY] is not None:
#                    i = gridX
#                    while i+1<self.gridSize and self.tiles[i+1][gridY] is None:
#                        i +=1
#                    if i+1<self.gridSize and self.tiles[i+1][gridY].value==self.tiles[gridX][gridY].value:
#                        self.score += self.tiles[gridX][gridY].value*2
#                        self.tiles[i+1][gridY].value *= 2
#                        self.tiles[gridX][gridY] = None
#                        moved = True
#                    elif i>gridX:
#                        self.tiles[i][gridY] = self.tiles[gridX][gridY]
#                        self.tiles[gridX][gridY] = None
#                        moved = True
#        if moved:
#            self.updateTiles()

    

            

    
       
    
class JeuWidget(Jeu,Widget2048):
    """ link between class jeu and class Widget, and effect of the keyboard and/or buttons"""
    def __init__(self,parent):
        Widget2048.__init__(self, parent)
        Jeu.__init__(self,gridSize = 4)
                     
                
    def keyPressEvent(self,e):
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
        self.lastPoint = e.pos()
        
    def mouseReleaseEvent(self,e):
        if self.resetRect.contains(self.lastPoint.x(),self.lastPoint.y()) and self.resetRect.contains(e.pos().x(),e.pos().y()):
            if QtWidgets.QMessageBox.question(self,'','Are you sure you want to start a new game?')==QtWidgets.QMessageBox.Yes:
                self.reset_game()
        elif self.gameRunning and self.lastPoint is not None:
            dx = e.pos().x()-self.lastPoint.x()
            dy = e.pos().y()-self.lastPoint.y()
            if abs(dx)>abs(dy) and abs(dx)>10:
                 if dx>0:
                     self.right()
                 else:
                     self.left()
                     
                     
#class AI_test(Jeu):
#    def __init__(self):
#        Jeu.__init__(self,gridSize=4)
#        
#    def get_score(tiles,first_dir):
#        """
#        Given a board and a first move, get a score by playing N_simulation random game
#        """
#        
#        stiles = tiles.copy()
#        
#        
#        
#AI = AI_test()
    

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