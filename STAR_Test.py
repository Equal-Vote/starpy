# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:03:26 2020

@author: keiedmo
"""

import json
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

        S = pd.DataFrame(all_parties, columns= Candidates)

        results = STAR(S)
        print(json.dumps(results, indent = 2)) #TODO: write printing function to make this look good
        self.assertEqual(results['elected'],['A4'])


    def test_tennessee(self):
        # Standard Tennessee example
        # https://en.wikipedia.org/wiki/STAR_voting#Example
        # https://electowiki.org/wiki/STAR_voting#Example
        columns = ['Memphis', 'Nashville', 'Chattanooga', 'Knoxville']
        ballots = pd.DataFrame(columns=columns,
                               data=[*42*[[5,      2,        1,          0]],
                                     *26*[[0,      5,        2,          1]],
                                     *15*[[0,      3,        5,          3]],
                                     *17*[[0,      2,        4,          5]]])

        self.assertEqual(STAR(ballots)['elected'], ['Nashville'])


if __name__ == '__main__':
    unittest.main()
