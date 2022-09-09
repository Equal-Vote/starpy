"""
Created on Thu Oct  8 12:03:26 2020

@author: keiedmo
"""

import json
import pandas as pd
from starpy.STAR import STAR, TrueTie


class TestSTAR:
    def test_original_example(self):
        Candidates = ['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4']
        Red = 61 * [[5.0,5.0,5.0,5.0,3.0,3.0,3.0,3.0,0.0,0.0,0.0,0.0]]
        blue = 39 * [[0.0,0.0,0.0,0.0,3.0,3.0,3.0,3.0,5.0,5.0,5.0,5.0]]
        tie_breaker = [[2.0,3.0,4.0,5.0,2.0,3.0,4.0,5.0,2.0,3.0,4.0,5.0]]
        all_parties = Red + blue + tie_breaker

        S = pd.DataFrame(all_parties, columns= Candidates)

        results = STAR(S)
        print(json.dumps(results, indent = 2)) #TODO: write printing function to make this look good
        assert results['elected'] == ['A4']

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

        assert STAR(ballots)['elected'] == ['Nashville']

    # https://github.com/Equal-Vote/star-core/blob/master/src/Tests/ties.test.js
    def test_star_condorcet_winner(self):
        columns = ['Allison', 'Bill', 'Carmen', 'Doug']
        election = [[5, 2, 1, 4],
                    [5, 2, 1, 0],
                    [5, 2, 1, 0],
                    [5, 2, 1, 0],
                    [5, 3, 4, 0],
                    [5, 1, 4, 0],
                    [5, 1, 4, 0],
                    [4, 0, 5, 1],
                    [3, 4, 5, 0],
                    [3, 5, 5, 5]]
        ballots = pd.DataFrame(columns=columns, data=election)
        results = STAR(ballots)

        # expected = [["Allison"], ["Carmen"], ["Bill", "Doug"]];
        assert results['elected'] == ['Allison']
        assert results['round_results'][0]['runner_up'] == 'Carmen'

    def test_star_runner_up_tie(self):
        columns = ['Allison', 'Bill', 'Carmen', 'Doug']
        election = [[5, 4, 3, 3],
                    [4, 5, 1, 1],
                    [4, 5, 1, 2],
                    [3, 5, 1, 0],
                    [5, 4, 3, 0],
                    [5, 0, 4, 1],
                    [5, 0, 4, 0],
                    [4, 0, 5, 1],
                    [3, 4, 5, 0],
                    [3, 5, 5, 4]]
        ballots = pd.DataFrame(columns=columns, data=election)
        results = STAR(ballots)

        # expected = [["Allison"], ["Bill", "Carmen"], ["Doug"]];
        assert results['elected'] == ['Allison']

    def test_star_true_tie(self):
        columns = ['Allison', 'Bill', 'Carmen', 'Doug']
        election = [[5, 4, 1, 4],
                    [5, 4, 1, 4],
                    [2, 4, 1, 2],
                    [4, 3, 2, 1],
                    [0, 5, 4, 4],
                    [3, 2, 4, 2],
                    [3, 1, 5, 3],
                    [3, 1, 5, 3],
                    [1, 3, 2, 2],
                    [4, 3, 5, 5]]
        ballots = pd.DataFrame(columns=columns, data=election)
        results = STAR(ballots)

        # expected = [["Allison", "Bill", "Carmen"], [], ["Doug"]];
        assert isinstance(results['elected'][0], TrueTie)

    def test_star_PR_ties(self):
        columns = ['Allison', 'Bill', 'Carmen', 'Doug']
        election = [[5, 4, 1, 4],
                    [5, 4, 1, 4],
                    [2, 4, 1, 2],
                    [4, 3, 2, 1],
                    [0, 5, 4, 4],
                    [3, 2, 4, 2],
                    [3, 1, 5, 3],
                    [3, 1, 5, 3],
                    [1, 3, 2, 2],
                    [4, 3, 5, 5]]
        ballots = pd.DataFrame(columns=columns, data=election)
        results = STAR(ballots)

        # expectedWinners = ["Allison", "Carmen", "Bill"];
        assert isinstance(results['elected'][0], TrueTie)

    def test_tiebreaker_cases(self):
        # 1. One highest-scoring, one 2nd-highest. B preferred in runoff:
        election = [[0, 5],
                    [2, 4],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert results['elected'] == [1]

        # 2. One highest-scoring, one 2nd-highest. Both tied in runoff, break
        # tie using scores, B wins:
        election = [[0, 5],
                    [3, 2],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert results['elected'] == [1]

        # 3. Two tied for highest-scoring, B wins in runoff:
        election = [[0, 2],
                    [1, 2],
                    [4, 1],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert results['elected'] == [1]

        # 4. Two tied for highest-scoring, also tied in runoff:
        election = [[1, 3],
                    [4, 2],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert isinstance(results['elected'][0], TrueTie)
        assert results['elected'][0] == {0, 1}

        # 5. One highest-scoring, two or more tied for second-highest. One
        # Condorcet winner among tied (C). One is preferred in runoff (A):
        election = [[5, 2, 3],
                    [5, 2, 3],
                    [5, 2, 0],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert results['elected'] == [0]

        # 6. One highest-scoring, two or more tied for second-highest. One
        # Condorcet winner among tied (C). Runoff is tied, highest-scoring A
        # wins:
        election = [[5, 2, 3],
                    [5, 2, 3],
                    [1, 2, 2],
                    [1, 4, 2],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert results['elected'] == [0]

        # 7. One highest-scoring, two or more tied for second-highest. No
        # Condorcet winner among tied, break 2nd place (B or C). A is preferred
        # in runoff regardless:
        election = [[5, 2, 3],
                    [5, 2, 3],
                    [4, 3, 2],
                    [1, 4, 3],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        # assert results['elected'] == [0]

        # 8. One highest-scoring, two or more tied for second-highest. No
        # Condorcet winner among tied, break 2nd place (B or C). Both are
        # also tied in runoff regardless, and highest-scoring wins (A):
        election = [[5, 2, 3],
                    [5, 2, 3],
                    [1, 3, 2],
                    [1, 4, 3],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        # assert results['elected'] == [0]

        # 9. Three or more tied for highest-scoring. One Condorcet winner and
        # one 2nd-place Condorcet winner go to runoff. Condorcet winner is A:
        election = [[2, 1, 0],
                    [2, 1, 0],
                    [2, 1, 0],
                    [2, 1, 0],
                    [1, 0, 0],
                    [0, 0, 4],
                    [0, 5, 5],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert results['elected'] == [0]

        # 10. Three or more tied for highest-scoring. Two tied for Condorcet
        # winner (A and B), both go to runoff. True Tie in runoff:
        election = [[2, 2, 0],
                    [2, 2, 0],
                    [1, 1, 5],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert isinstance(results['elected'][0], TrueTie)
        assert results['elected'][0] == {0, 1}

        # 11. Three or more tied for highest-scoring. One Condorcet winner in
        # tiebreaker and two or more tied for 2nd place CW. Break tie (B or C).
        # Regardless, Condorcet winner A wins runoff:
        election = [[2, 1, 1],
                    [2, 1, 1],
                    [3, 5, 5],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        # assert results['elected'] == [0]

        # 12. Three or more tied for highest-scoring. No Condorcet winners
        # either:
        election = [[5, 5, 5],
                    [2, 2, 2],
                    ]
        ballots = pd.DataFrame(data=election)
        results = STAR(ballots)
        assert isinstance(results['elected'][0], TrueTie)
        assert results['elected'][0] == {0, 1, 2}


if __name__ == '__main__':
    pytest.main()
