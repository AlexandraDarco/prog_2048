# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 18:01:03 2020

@author: cecil
"""

from PyQt5 import QtCore, QtWidgets
import random

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent, width=340, gridSize=4):
        QtWidgets.QWidget.__init__(self, parent)
        self.gameRunning = False
        self.panelHeight = 80
        self.gridSize = gridSize
        
        self.reset_game()
        
    def reset_game(self):
        self.tiles = [[None for i in range(0,self.gridSize)] for i in range (0,self.gridSize)]
        self.availableSpots = range(0,self.gridSize**2)
        
    def addTile(self):
        if len(self.availableSpots)>0:
            value = 2 if random.random()<0.9 else 4
            ind = self.availableSpots.pop(int(random.random()*len(self.availableSpots)))
        

jeu = MyWidget(None,340,4)