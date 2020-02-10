# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 12:11:48 2020

@author: cecil
"""

import sys
from PyQt5 import QtCore, QtWidgets,QtGui
import random


class Tile:
    def __init__(self,value):
        self.value = value
        
class Jeu:
    def __init__(self, gridSize = 4):
        self.gameRunning = False
        self.gridSize =gridSize
        self.hiScore = 0
        self.reset_game()
        
    def reset_game(self):
        self.tiles = [[None for i in range(0,self.gridSize)] for i in range(0,self.gridSize)]
        self.availableSpots = list(range(0,self.gridSize**2))
        self.score = 0
        self.addTile()
        self.addTile()
        self.update()
        self.gameRunning = True
        
    def addTile(self):
        if len(self.availableSpots)>0:
            value = 2 if random.random()<0.9 else 4 
            ind = self.availableSpots.pop(int(random.random()*len(self.availableSpots)))
            indx = ind%self.gridSize
            indy = ind//self.gridSize
            self.tiles[indx][indy] = Tile(value)
     
    def up(self):
        moved = False
        for gridX in range(0,self.gridSize):
            for gridY in range(1,self.gridSize):
                if self.tiles[gridX][gridY] is not None:
                    i = gridY
                    while i-1>=0 and self.tiles[gridX][i-1] is  None:
                        i -= 1
                    if i-1>=0 and self.tiles[gridX][i-1].value==self.tiles[gridX][gridY].value:
                        self.score += self.tiles[gridX][gridY].value*2
                        self.tiles[gridX][i-1].value *= 2
                        self.tiles[gridX][gridY] = None
                        moved = True
                    elif i<gridY:
                        self.tiles[gridX][i] = self.tiles[gridX][gridY]
                        self.tiles[gridX][gridY] = None
                        moved = True
        if moved:
            self.updateTiles()
            
    def down(self):
        moved = False
        for gridX in range(0,self.gridSize):
            for gridY in range(self.gridSize-2,-1,-1):
                if self.tiles[gridX][gridY] is not None:
                    i = gridY
                    while i+1<self.gridSize and self.tiles[gridX][i+1] is None:
                        i += 1
                    if i+1<self.gridSize and self.tiles[gridX][i+1].value==self.tiles[gridX][gridY].value:
                        self.score += self.tiles[gridX][gridY].value*2
                        self.tiles[gridX][i+1].value *= 2
                        self.tiles[gridX][gridY] = None
                        moved = True
                    elif i>gridY:
                        self.tiles[gridX][i] = self.tiles[gridX][gridY]
                        self.tiles[gridX][gridY] = None
                        moved = True
        if moved:
           self.updateTiles()
           
    def left(self):
        moved = False
        for gridX in range(1,self.gridSize):
            for gridY in range(0,self.gridSize):
                if self.tiles[gridX][gridY] is not None:
                    i = gridX
                    while i-1>=0 and self.tiles[i-1][gridY] is None:
                        i -= 1
                    if i-1>=0 and self.tiles[i-1][gridY].value==self.tiles[gridX][gridY].value:
                        self.score += self.tiles[gridX][gridY].value*2
                        self.tiles[i-1][gridY].value *= 2
                        self.tiles[gridX][gridY] = None
                        moved = True
                    elif i<gridX:
                        self.tiles[i][gridY] = self.tiles[gridX][gridY]
                        self.tiles[gridX][gridY] = None
                        moved = True
        if moved:
            self.updateTiles()
            
    def right(self):
        moved = False
        for gridX in range(self.gridSize-2,-1,-1):
            for gridY in range(0,self.gridSize):
                if self.tiles[gridX][gridY] is not None:
                    i = gridX
                    while i+1<self.gridSize and self.tiles[i+1][gridY] is None:
                        i +=1
                    if i+1<self.gridSize and self.tiles[i+1][gridY].value==self.tiles[gridX][gridY].value:
                        self.score += self.tiles[gridX][gridY].value*2
                        self.tiles[i+1][gridY].value *= 2
                        self.tiles[gridX][gridY] = None
                        moved = True
                    elif i>gridX:
                        self.tiles[i][gridY] = self.tiles[gridX][gridY]
                        self.tiles[gridX][gridY] = None
                        moved = True
        if moved:
            self.updateTiles()

    def updateTiles(self):
        self.availableSpots = []
        for i in range(0,self.gridSize):
            for j in range(0,self.gridSize):
                if self.tiles[i][j] is None:
                    self.availableSpots.append(i+j*self.gridSize)
        self.addTile()
        self.hiScore = max(self.score,self.hiScore)
        self.update()
        # si plus de coup dispo -> game over
        if not self.movesAvailable():
            self.gameRunning = False  
            QtWidgets.QMessageBox.information(self,'','Game Over')
            
    
    def movesAvailable(self):
        """
        quels sont les coups dispo ? 
        """
        if not len(self.availableSpots)==0:
            return True
        for i in range(0,self.gridSize):
            for j in range(0,self.gridSize):
                if i<self.gridSize-1 and self.tiles[i][j].value==self.tiles[i+1][j].value:
                    return True
                if j<self.gridSize-1 and self.tiles[i][j].value==self.tiles[i][j+1].value:
                    return True
        return False
    
    
class Widget2048(QtWidgets.QWidget):
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
        painter.drawText(self.scoreLabel,str(self.score),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.drawText(self.hiScoreLabel,str(self.hiScore),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
        painter.setFont(self.font)
        for gridX in range(0,self.gridSize):
            for gridY in range(0,self.gridSize):
                tile = self.tiles[gridX][gridY]
                if tile is None:
                    painter.setBrush(self.brushes[0])
                else:
                    painter.setBrush(self.brushes[tile.value])
                rect = QtCore.QRectF(self.gridOffsetX+gridX*(self.tileSize+self.tileMargin),
                                       self.gridOffsetY+gridY*(self.tileSize+self.tileMargin),
                                       self.tileSize,self.tileSize)
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawRect(rect)
                if tile is not None:
                    painter.setPen(self.darkPen if tile.value<16 else self.lightPen)
                    painter.drawText(rect,str(tile.value),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))


        
    
class JeuWidget(Jeu,Widget2048):
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
    