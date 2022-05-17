# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:03:26 2020

@author: keiedmo
"""

import pandas as pd
import numpy as np


Candidates = ['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4']
Red = 61 * [[5.0,5.0,5.0,5.0,3.0,3.0,3.0,3.0,0.0,0.0,0.0,0.0]]
blue = 39 * [[0.0,0.0,0.0,0.0,3.0,3.0,3.0,3.0,5.0,5.0,5.0,5.0]]
tie_breaker = [[2.0,3.0,4.0,5.0,2.0,3.0,4.0,5.0,2.0,3.0,4.0,5.0]]
all_parties = Red + blue + tie_breaker
W = 5
K = 5.0

S = pd.DataFrame(all_parties, columns= Candidates) 


def STAR(K, W, S):
    #Score winners
    df_tops = S[S.sum().nlargest(2, keep='all').index]
    
    #Run off
    winner = df_tops.eq(df_tops.max(1), axis=0).sum().idxmax()  
    
    return winner


winner = STAR(K, W, S)

print('STAR')       
print(winner)   