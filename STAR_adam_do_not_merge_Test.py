"""
Created on Thu Oct  8 12:03:26 2020

@author: keiedmo
"""

import json
import pandas as pd
import numpy as np
from STAR import STAR, TrueTie
import pytest


class TestSTAR:
    def test_original_example(self):
        Candidates = ['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4']
        Red = 61 * [[  5,   5,   5,   5,   3,   3,   3,   3,   0,   0,   0,   0]]
        blue = 39 * [[ 0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 5.0, 5.0, 5.0, 5.0]]
        tie_breaker = [[2.0,3.0,4.0,5.0,2.0,3.0,4.0,5.0,2.0,3.0,4.0,5.0]]
        all_parties = Red + blue + tie_breaker

        S = pd.DataFrame(all_parties, columns= Candidates)

        results = STAR(S, numwinners=2)
        print(json.dumps(results, indent = 2)) #TODO: write printing function to make this look good
        assert results['elected'] == ['A4', 'A3']

if __name__ == '__main__':
    pytest.main()
