import pandas as pd
import numpy as np

class InvalidElection(Exception):
    pass

class TrueTie:
    def __init__(self, tied):
        self.tied = tied

def summary_data(ballots: pd.DataFrame):
    # The below quantities can be emitted however is most useful
    score_hist = {a : ballots[a].value_counts() for a in ballots.columns}
    score_sums = ballots.sum()
    pairwise_matrix = { a :
            { b : pairwise_winner(ballots, a, b) for b in ballots.columns }
        for a in ballots.columns
    }
    return (score_hist, score_sums, pairwise_matrix)

def score_winners(ballots: pd.DataFrame):
    #Score winners
    scores = ballots.sum()
    top_score = scores.max()
    return [a for a in ballots.columns if np.isclose(scores[a], top_score)]
    
def pairwise_winner(a: pd.Series, b: pd.Series):
    # Returns 1 if a is preferred to b, -1 if b is preferred to a, and 0 for a tie
    margin = (a > b).sum() - (b > a).sum()
    if margin > 0:
        return 1
    elif margin < 0:
        return -1
    else:
        return 0

def has_defeat(ballots: pd.DataFrame, a):
    for b in ballots.columns:
        if pairwise_winner(ballots[b], ballots[a]) == 1:
            return 1
    return 0

def fivestar(ballots: pd.DataFrame):
    fstars = (ballots == ballots.max().max()).sum()
    top_fstars = fstars.max()
    return [a for a in ballots.columns if np.isclose(fstars[a], top_fstars)]

def weak_condorcet_winners(ballots: pd.DataFrame):
    return [a for a in ballots.columns if not has_defeat(ballots, a)]

##############################################################################
# The above functions are mainly helpers for easier reading of the main logic.
##############################################################################

def default_scoring_tiebreaker(ballots: pd.DataFrame):
    tmp = weak_condorcet_winners(ballots)
    if len(tmp) == 1:
        return tmp[0]
    elif len(tmp) == 0:
        return TrueTie(list(ballots.columns))
    else:
        return TrueTie(tmp)

def default_runoff_tiebreaker(ballots: pd.DataFrame):
    # Any pre-runoff ties must be resolved
    assert len(ballots.columns) == 2

    a,b = ballots.columns
    scores = ballots.sum()
    if np.isclose(scores[a], scores[b]):
        return TrueTie(list(ballots.columns))
    else:
        return scores.argmax()

def STAR(ballots: pd.DataFrame, scoring_tiebreaker=default_scoring_tiebreaker, runoff_tiebreaker=default_runoff_tiebreaker):
    """
        Given an election instance and optionally specified tiebreakers, return the STAR winner.

        Parameters:
            ballots (pd.DataFrame): contains a dataframe oriented such that each column name is a candidate
                and each row is a voter's ballot. That is, the score voter A gives to candidate X is ballots[X][A]
            
            scoring_tiebreaker (function): Given an election instance, returns a winner according to the tiebreaker
                or a TrueTie instance if it is not sufficiently resolute. Called during the scoring round of STAR.
            
            runoff_tiebreaker (function): Given an election instance, returns a winner according to the tiebreaker
                or a TrueTie instance if it is not sufficiently resolute. Called during the runoff round of STAR.
    """

    if ballots.shape[1] < 1:
        raise InvalidElection("Not enough candidates to fill desired number of seats")

    # If there is only one candidate, elect them
    if ballots.shape[1] == 1:
        return ballots.columns[0]

    runoff_candidates = []
    while len(runoff_candidates) < 2:

        eligible = ballots.drop(runoff_candidates, axis=1)
        w = scoring_tiebreaker(ballots[score_winners(eligible)])
        if isinstance(w, TrueTie):

            if len(w.tied) == 2 and len(runoff_candidates) == 0:
                runoff_candidates.extend(w.tied)

            else:
                # In this case, the election returned a tie unresolvable by stated tiebreakers
                w.tied.extend(runoff_candidates)
                return w

        else:
            runoff_candidates.append(w)
    
    # At this point, either we have already exited or runoff_candidates contains exactly two candidates
    a,b = runoff_candidates
    runoff_outcome = pairwise_winner(ballots[a], ballots[b])

    if runoff_outcome == 1:
        return a
    elif runoff_outcome == -1:
        return b
    else:
        return runoff_tiebreaker(ballots[runoff_candidates])

def Bloc_STAR(ballots: pd.DataFrame, numwinners: int, scoring_tiebreaker=default_scoring_tiebreaker, runoff_tiebreaker=default_runoff_tiebreaker):
    elected = []
    while len(elected) < numwinners:
        
        eligible = ballots.drop(elected, axis=1)
        w = STAR(eligible, scoring_tiebreaker=scoring_tiebreaker, runoff_tiebreaker=runoff_tiebreaker)
        if isinstance(w, TrueTie):

            if len(w.tied) + len(elected) <= numwinners:
                # If multiple candidates are tied in STAR but we have enough seats to elect them all, do so
                elected.extend(w.tied)

            else:
                # In this case, the election returned a tie unresolveable by stated tiebreakers
                w.tied.extend(elected)
                return w
        else:
            elected.append(w)
    
    return elected
