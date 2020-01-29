# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 13:52:25 2020

@author: alexa
"""

from PyQt5 import QtCore, QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.lay = QtWidgets.QHBoxLayout()
        self.setLayout(self.lay)
        
        self.button = QtWidgets.QPushButton("coucou", parent=self)
        self.button2 = QtWidgets.QPushButton("coucou2", parent=self)
        
        self.lay.addWidget(self.button)
        self.lay.addWidget(self.button2)
        
        
        self.button.clicked.connect(self.update_gui)
        
        self.show()
        
        
    def update_gui(self):
        print('coucou')


if __name__=='__main__':
    APP = QtWidgets.QApplication.instance()
    IS_STANDARD_CONSOLE = (APP is None)
    if IS_STANDARD_CONSOLE: # launched from standard console (not ipython console)
        APP = QtWidgets.QApplication(["test"])
    M = MyWidget()
    if IS_STANDARD_CONSOLE:
        APP.exec_()


