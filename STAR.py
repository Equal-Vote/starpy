import pandas as pd
import numpy as np
import random

def pairwise_winner(a, b):
    # Returns 1 if a is preferred to b, -1 if b is preferred to a, and 0 for a tie
    margin = (a > b).sum() - (b > a).sum()
    if margin > 0:
        return 1
    elif margin < 0:
        return -1
    else:
        return 0

def has_defeat(S, a):
    for b in S.columns:
        if pairwise_winner(S[b], S[a]) == 1:
            return 1
    return 0

def break_ties(S, tied, k=5, highstar=True):
    _S = S[tied]

    finalists = [a for a in tied if not has_defeat(_S, a)]

    if highstar:
        # 5-star selection among tied candidates if applicable
        finalists = (_S[finalists] == k).sum().nlargest(1, keep="all").index

    if len(finalists) == 1:
        # If there is only one remaining candidate, return them
        return finalists[0]
    
    else:
        # Otherwise, some randomness may be required
        return random.choice(finalists)

def scoring_phase(S, w, k=5, highstar=True):

    #Score winners
    stars = S.sum()
    top_score = stars.max()
    tied_winners = [a for a in S.columns if np.isclose(stars[a], top_score)]
    
    
    winner = break_ties(S, tied_winners, k=k, highstar=highstar)

    if w == 1:
        return [winner]
    else:
        S = S.drop(winner)
        return [winner] + scoring_phase(S, w-1, k=k, highstar=highstar)

def STAR(S, k=5, highstar=True):
    if S.size[1] == 1:
        return S.columns[0]

    # Otherwise, there is real competition!
    two_advancing = scoring_phase(S, 2, k=k, highstar=highstar)
    return break_ties(S, two_advancing)