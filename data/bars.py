# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 19:38:50 2020

@author: alexa
"""
import numpy as np
import matplotlib.pyplot as plt


def plot_stat(self):
    data_score, data_max_tile, data_time, data_N_moves = self.run_stat()
    
    ##
    plt.figure()
    plt.plot(range(0,self.N_trials),data_max_tile)
    plt.plot(range(0,self.N_trials),data_score)
    plt.show()
    
            
    distrib = []
    i = 1
    while i<12:
        distrib.append(np.count_nonzero(np.array(data_max_tile) == 2**i))
        i += 1

distrib_snake = [0, 0, 0, 1, 15, 71, 254, 424, 209, 25, 1]
distrib_pyramid2 = [0, 0, 0, 0, 36, 254, 493, 212, 5, 0, 0]
distrib_merge = [0, 0, 0, 0, 4, 63, 389, 485, 59, 0, 0]
distrib_montecarlo = [0, 0, 0, 0, 0, 3, 7, 0, 0, 0, 0]


bars2 = np.array([0,0,0,0])
bars4 = np.array([0,0,0,0])
bars8 =np.array([0,0,0,0])
bars16 =np.array([1,0,0,0])/10
bars32 =np.array([15,36,4,0])/10
bars64 = np.array([71, 254, 63,300])/10
bars128 = np.array([254, 493, 389,700])/10
bars256 = np.array([424, 212, 485,0])/10
bars512 = np.array([209,5,59,0])/10
bars1024 = np.array([25,0,0,0])/10
bars2048 = np.array([1,0,0,0])/10


# The position of the bars on the x-axis
r = [3,1,2,0]
 
# Names of group and bar width
names = ['snake','pyramid','merge','montecarlo']
liste = ['2','4','8','16','32','64','128','256','512','1024','2048']
barWidth = 0.50

bars = bars2 

plt.bar(r, bars2, color='goldenrod', edgecolor='white', width=barWidth)
plt.bar(r, bars4, bottom=bars, color='lemonchiffon', edgecolor='white', width=barWidth)
bars = bars + bars4
plt.bar(r, bars8, bottom=bars, color='#f2b179', edgecolor='white', width=barWidth)
bars = bars + bars8
plt.bar(r, bars16, bottom=bars, color='moccasin', edgecolor='white', width=barWidth)
bars = bars + bars16
plt.bar(r, bars32, bottom=bars, color='#ede0c8', edgecolor='white', width=barWidth)
bars += bars32
plt.bar(r, bars64, bottom=bars, color= 'yellow', edgecolor='white', width=barWidth)
bars += bars64
plt.bar(r, bars128, bottom=bars, color='gold', edgecolor='white', width=barWidth)
bars += bars128
plt.bar(r, bars256, bottom=bars, color='darkorange', edgecolor='white', width=barWidth)
bars += bars256
plt.bar(r, bars512, bottom=bars, color='red', edgecolor='white', width=barWidth)
bars += bars512
plt.bar(r, bars1024, bottom=bars, color='darkred', edgecolor='white', width=barWidth)
bars += bars1024
plt.bar(r, bars2048, bottom=bars, color='black', edgecolor='white', width=barWidth)
        

plt.xticks(r, names)
plt.title('Répartition de la valeur des tuiles maximales atteintes')
plt.ylabel('%')
plt.legend(liste)
plt.xlim([-0.5,4])
