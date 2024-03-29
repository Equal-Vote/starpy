# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:03:26 2020

@author: keiedmo
"""

import pandas as pd
import sys
sys.path.append('.')
from starpy.Allocated_Score import Allocated_Score

# #Centerist bias 3 
# Candidates = ['A','B','C']
# Red = 61 * [[5.0,3.0,0.0]]
# blue = 39 * [[0.0,3.0,5.0]]
# all_parties = Red + blue
# W = 5.0

# #Centerist bias 3 no clones
# Candidates = ['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4']
# Red = 61 * [[5.0,5.0,5.0,5.0,3.0,3.0,3.0,3.0,0.0,0.0,0.0,0.0]]
# blue = 39 * [[0.0,0.0,0.0,0.0,3.0,3.0,3.0,3.0,5.0,5.0,5.0,5.0]]
# all_parties = Red + blue
# W = 5.0

# Candidates = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14','A15','A16','A17','A18','A19','A20','A21','B1','B2','B3']
# G1 =   100 * [[5,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G2 =   100 * [[5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G3 =   100 * [[0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G4 =   100 * [[0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G5 =   100 * [[0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G6 =   100 * [[0,0,0,5,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G7 =   100 * [[0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G8 =   100 * [[0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G9 =   100 * [[0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G10 =  100 * [[0,0,0,0,0,0,5,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G11 =  100 * [[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G12 =  100 * [[0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G13 =  100 * [[0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G14 =  100 * [[0,0,0,0,0,0,0,0,0,5,0,5,0,0,0,0,0,0,0,0,0,0,0,0]]
# G15 =  100 * [[0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G16 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0]]
# G17 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0]]
# G18 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,5,0,5,0,0,0,0,0,0,0,0,0]]
# G19 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0]]
# G20 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0]]
# G21 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0]]
# G22 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,5,0,0,0,0,0,0]]
# G23 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0]]
# G24 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0]]
# G25 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0]]
# G26 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,5,0,0,0]]
# G27 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0]]
# G28 =  100 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0]]
# G29 =   71 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,5]]
# G30 =   71 * [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,5,0]]

# all_parties = G1 + G2 + G3 + G4 + G5 + G6 + G7 + G8 + G9 + G10 + G11 + G12 + G13 + G14 + G15 + G16 + G17 + G18 + G19 + G20 + G21 + G22 + G23 + G24 + G25 + G26 + G27 + G28 + G29 + G30
# W = 21.0 

# Candidates = ['A','B1','B2','B3','B4','B5','B6']
# # # 
# G1 =  1 * [[1,5,0,0,0,0,0]]
# G2 =  5 * [[1,0,5,0,0,0,0]]
# G3 =  5 * [[1,0,0,5,0,0,0]]
# G4 =  5 * [[0,0,0,0,5,0,0]]
# G5 =  5 * [[0,0,0,0,0,5,4]]
# G6 =  5 * [[0,0,0,0,0,3,5]]
# all_parties = G1 + G2 + G3 + G4 + G5 + G6
# W = 5.0


# Candidates = ['A','B1','B2','B3','B4','C1','C2','D1','D2','D3','D4','D5','D6','D7','D8','D9','D10']
# # # 
# G1 =  5 * [[3,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0]]
# G2 =  5 * [[3,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0]]
# G3 =  6 * [[0,3,0,0,0,2,0,0,0,5,0,0,0,0,0,0,0]]
# G4 =  6 * [[0,3,0,0,0,2,0,0,0,0,5,0,0,0,0,0,0]]
# G5 =  6 * [[0,0,3,0,0,2,0,0,0,0,0,5,0,0,0,0,0]]
# G6 =  6 * [[0,0,3,0,0,2,0,0,0,0,0,0,5,0,0,0,0]]
# G7 =  6 * [[0,0,0,3,0,0,2,0,0,0,0,0,0,5,0,0,0]]
# G8 =  6 * [[0,0,0,3,0,0,2,0,0,0,0,0,0,0,5,0,0]]
# G9 =  6 * [[0,0,0,0,3,0,2,0,0,0,0,0,0,0,0,5,0]]
# G10 =  6 * [[0,0,0,0,3,0,2,0,0,0,0,0,0,0,0,0,5]]

# all_parties = G1 + G2 + G3 + G4 + G5 + G6 + G7 + G8 + G9 + G10
# W = 6.0


# Candidates = ['A','B1','B2','B3','B4','B5','B6','C1','C2']
# # # 
# G1 =  1 * [[1,5,0,0,0,0,0,0,0]]
# G2 =  5 * [[1,5,1,0,0,0,0,0,1]]
# G3 =  5 * [[1,0,5,5,0,0,0,0,1]]
# G4 =  5 * [[0,0,0,0,5,0,0,1,1]]
# G5 =  5 * [[0,0,0,0,0,5,0,1,0]]
# G6 =  5 * [[1,0,0,0,0,0,5,1,0]]
# all_parties = G1 + G2 + G3 + G4 + G5 + G6
# W = 5.0

Candidates = ['FL1','FL2','L1','L2','C1','C2','R1','R2','FR1','FR2']
# # 
G1 =  10 * [[5,5,0,0,0,0,0,0,0,0]]
G2 =  15 * [[5,5,5,5,0,0,0,0,0,0]]
G3 =  15 * [[0,0,5,5,5,5,0,0,0,0]]
G4 =  20 * [[0,0,0,0,5,5,0,0,0,0]]
G5 =  15 * [[0,0,0,0,5,5,5,5,0,0]]
G6 =  15 * [[0,0,0,0,0,0,5,5,5,5]]
G7 =  10 * [[0,0,0,0,0,0,0,0,5,5]]
all_parties = G1 + G2 + G3 + G4 + G5 + G6 +G7
W = 5.0

# Candidates = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14','A15','A16','A17','A18','A19','A20', 'A21','A22','A23','A24','A25','A26','A27','A28','A29','A30','B1','B2','B3','B4','B5']
# G1 =  10 * [[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5]]
# G2 =  10 * [[0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5]]
# G3 =  10 * [[0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5]]
# G4 =  10 * [[0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5]]
# G5 =  10 * [[0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5]]
# G6 =  10 * [[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G7 =  10 * [[1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G8 =  10 * [[1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G9 =  10 * [[1,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G10 =  10 * [[1,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G11 =  10 * [[1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G12 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G13 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G14 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G15 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G16 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G17 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G18 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G19 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G20 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G21 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G22 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# G23 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]]
# G24 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]]
# G25 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]]
# G26 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]]
# G27 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]]
# G28 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]]
# G29 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]]
# G30 =  10 * [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]]

# all_parties = G1 + G2 + G3 + G4 + G5 + G6 + G7 + G8 + G9 + G10 + G11 + G12 + G13 + G14 + G15 + G16 + G17 + G18 + G19 + G20 + G21 + G22 + G23 + G24 + G25 + G26 + G27 + G28 + G29 + G30

# W = 30.0 

K = 5.0
S = pd.DataFrame(all_parties, columns= Candidates) 

winner_list = Allocated_Score(K, W, S)

print('Allocated score')
print(winner_list)
