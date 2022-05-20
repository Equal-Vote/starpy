import pandas as pd
import numpy as np

def STAR(K, W, S):
    #Score winners
    df_tops = S[S.sum().nlargest(2, keep='all').index]
    
    #Run off
    winner = df_tops.eq(df_tops.max(1), axis=0).sum().idxmax()  
    
    return winner