# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:03:26 2020

@author: keiedmo
"""

import pandas as pd
import numpy as np
from STAR import STAR
import unittest

class STARTest(unittest.TestCase):
    def test_original_example(self):
        Candidates = ['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4']
        Red = 61 * [[5.0,5.0,5.0,5.0,3.0,3.0,3.0,3.0,0.0,0.0,0.0,0.0]]
        blue = 39 * [[0.0,0.0,0.0,0.0,3.0,3.0,3.0,3.0,5.0,5.0,5.0,5.0]]
        tie_breaker = [[2.0,3.0,4.0,5.0,2.0,3.0,4.0,5.0,2.0,3.0,4.0,5.0]]
        all_parties = Red + blue + tie_breaker

        W = 5
        K = 5.0
        S = pd.DataFrame(all_parties, columns= Candidates) 

        winner = STAR(K, W, S)
        print(winner)   
        self.assertEqual(winner,'A4')    



if __name__ == '__main__':
    unittest.main()