from ast import Starred
import pandas as pd
import numpy as np
import copy
from typing import Union
class InvalidElection(Exception):
    pass

class TrueTie(set):
    def __repr__(self) -> str:
        return 'TrueTie(' + repr(set(self)) + ')'
class SummaryData:
    def __init__(self,score_hist, score_sums, pairwise_matrix, preference_matrix):
        self.score_hist = score_hist
        self.score_sums = score_sums
        self.pairwise_matrix = pairwise_matrix
        self.preference_matrix = preference_matrix

    def drop(self,candidates):
        self.score_hist.drop(candidates, axis=0, inplace=True)
        self.score_sums.drop(candidates, axis=0, inplace=True)
        self.pairwise_matrix.drop(candidates, axis=0, inplace=True)
        self.pairwise_matrix.drop(candidates, axis=1, inplace=True)
        self.preference_matrix.drop(candidates, axis=0, inplace=True)
        self.preference_matrix.drop(candidates, axis=1, inplace=True)
        return self

    def keep(self,candidates):
        self.score_hist = self.score_hist.loc[candidates, :]
        self.score_sums = self.score_sums.loc[candidates]
        self.pairwise_matrix = self.pairwise_matrix.loc[candidates, candidates]
        self.preference_matrix = self.preference_matrix.loc[candidates, candidates]
        return self

def get_summary_data(ballots: pd.DataFrame):
    # The below quantities can be emitted however is most useful
    score_hist = pd.DataFrame(0, columns = range(6), index = ballots.columns)
    for a in ballots.columns:
        score_hist.loc[a] = ballots[a].value_counts().sort_index()
    score_hist = score_hist.fillna(0)
    
    score_sums = ballots.sum()
    
    preference_matrix = pd.DataFrame(0, columns = ballots.columns, index = ballots.columns)
    for a in ballots.columns:
        for b in ballots.columns:
            preference_matrix.loc[a][b] = (ballots.loc[:][a]>ballots.loc[:][b]).sum()
    pairwise_matrix = (preference_matrix > preference_matrix.T).astype(int)

    return SummaryData(score_hist, score_sums, pairwise_matrix, preference_matrix)

def score_winners(scores: pd.DataFrame):
    #Score winners
    # scores = ballots.sum()
    top_score = scores.max()
    return [a for a in scores.index if np.isclose(scores[a], top_score)]
    
def pairwise_winner(a: pd.Series, b: pd.Series):
    # Returns 1 if a is preferred to b, -1 if b is preferred to a, and 0 for a tie
    margin = (a > b).sum() - (b > a).sum()
    if margin > 0:
        return 1
    elif margin < 0:
        return -1
    else:
        return 0

def has_defeat(pairwise_matrix: pd.DataFrame, a):
    for b in pairwise_matrix.columns:
        if pairwise_matrix.loc[b][a] == 1:
            return 1
    return 0

def fivestar(ballots: pd.DataFrame):
    fstars = (ballots == ballots.max().max()).sum()
    top_fstars = fstars.max()
    return [a for a in ballots.columns if np.isclose(fstars[a], top_fstars)]

def weak_condorcet_winners(pairwise_matrix: pd.DataFrame):
    return [a for a in pairwise_matrix.columns if not has_defeat(pairwise_matrix, a)]

##############################################################################
# The above functions are mainly helpers for easier reading of the main logic.
##############################################################################

def default_scoring_tiebreaker(pairwise_matrix: pd.DataFrame):
    tmp = weak_condorcet_winners(pairwise_matrix)
    if len(tmp) == 1:
        return tmp[0]
    elif len(tmp) == 0:
        return TrueTie(pairwise_matrix.columns)
    else:
        return TrueTie(tmp)

def default_runoff_tiebreaker(summary_data: SummaryData):
    # Any pre-runoff ties must be resolved
    assert len(summary_data.score_sums.index) == 2

    a,b = summary_data.score_sums.index
    scores = summary_data.score_sums
    if np.isclose(scores[a], scores[b]):
        return TrueTie(summary_data.score_sums.index)
    else:
        return scores.index[scores.argmax()]

def Run_STAR_Round(summary_data: SummaryData, scoring_tiebreaker=default_scoring_tiebreaker, runoff_tiebreaker=default_runoff_tiebreaker):
    # If there is only one candidate, elect them
    
    round_results = {'winners':[], 'runner_up':[], 'logs':[]}
    
    if len(summary_data.score_sums.index) == 1:
        round_results['winners'] = summary_data.score_sums.index
        round_results['logs'].append({'top_score': summary_data.score_sums.index})
        round_results['logs'].append({'runoff_candidates': summary_data.score_sums.index})
        return round_results
 
    runoff_candidates = []
    while len(runoff_candidates) < 2:

        eligible = copy.deepcopy(summary_data).drop(runoff_candidates)
        top_scorers = score_winners(eligible.score_sums)
        # round_results['logs'].append({'top_scorers': top_scorers})
        if len(top_scorers)==1:
            round_results['logs'].append({'top_score': top_scorers})
            runoff_candidates.extend(top_scorers)
        else:
            round_results['logs'].append({'score_tie': top_scorers})
            w = scoring_tiebreaker(eligible.pairwise_matrix[top_scorers][top_scorers])
            if isinstance(w, TrueTie):
                round_results['logs'].append({'score_true_tie': w})

                if len(w) == 2 and len(runoff_candidates) == 0:
                    runoff_candidates.extend(w)

                else:
                    # In this case, the election returned a tie unresolvable by stated tiebreakers
                    w.union(set(runoff_candidates))
                    round_results['winners'] = w
                    return round_results

            else:
                runoff_candidates.extend([w])
    
    round_results['logs'].append({'runoff_candidates': runoff_candidates})
    # At this point, either we have already exited or runoff_candidates contains exactly two candidates
    a,b = runoff_candidates

    if summary_data.pairwise_matrix.loc[a][b] == 1:
        round_results['winners'] = [a]
        round_results['runner_up'] = b
        return round_results
    elif summary_data.pairwise_matrix.loc[b][a] == 1:
        round_results['winners'] = [b]
        round_results['runner_up'] = a
        return round_results
    else:
        runoff_tiebreaker_results = runoff_tiebreaker(copy.deepcopy(summary_data).keep(runoff_candidates))
        if runoff_tiebreaker_results == a:
            round_results['winners'] = [a]
            round_results['runner_up'] = b
            return round_results
        elif runoff_tiebreaker_results == b:
            round_results['winners'] = [b]
            round_results['runner_up'] = a
            return round_results
        else:
            round_results['winners'] = runoff_tiebreaker_results
            return round_results

def STAR(input_data: Union[pd.DataFrame,SummaryData], numwinners=1, scoring_tiebreaker=default_scoring_tiebreaker, runoff_tiebreaker=default_runoff_tiebreaker):
    """
    Given election data and optionally specified number of winners and tiebreaker protocols, return the STAR winners.

    Parameters:
        input_data (pd.DataFrame OR SummaryData): 
            If pd.DataFrame: contains a dataframe oriented such that each column name is a candidate
            and each row is a voter's ballot. That is, the score voter A gives to candidate X is ballots[X][A]

            if SummaryData: contains instance of SummaryData object. Would be used in the event that SummaryData 
            is processed and summed accross multiple precincts

        numwinners (int): number of winners for this eleciton
            
        scoring_tiebreaker (function): Given an election instance, returns a winner according to the tiebreaker
            or a TrueTie instance if it is not sufficiently resolute. Called during the scoring round of STAR.
            
        runoff_tiebreaker (function): Given an election instance, returns a winner according to the tiebreaker
            or a TrueTie instance if it is not sufficiently resolute. Called during the runoff round of STAR.

        Returns:
            A dict containing the election results.

        Examples:
            Candace and Allie are the favorite of two voters, while Billy is
            the favorite of one.  Since all voters give Billy high scores,
            Billy and Allie proceed to the runoff.  In the runoff, Billy is
            preferred by three out of five voters over Allie, and wins.

            >>> import pandas as pd
            >>> ballots = pd.DataFrame(columns=['Allie', 'Billy', 'Candace'],
                                       data=[*2*[[5,      4,       0]],
                                             *1*[[2,      5,       1]],
                                             *2*[[0,      4,       5]],])
            >>> print(ballots)
               Allie  Billy  Candace
            0      5      4        0
            1      5      4        0
            2      2      5        1
            3      0      4        5
            4      0      4        5
            >>> print(ballots.sum())
            Allie      12
            Billy      21
            Candace    11
            dtype: int64
            >>> STAR(ballots)
            {'elected': ['Billy'],
             'round_results': [{'winners': ['Billy'],
               'runner_up': 'Allie',
               'logs': [{'top_score': ['Billy']},
                {'top_score': ['Allie']},
                {'runoff_candidates': ['Billy', 'Allie']}]}]}
    """
    results = {'elected': [], 'round_results': []}
    if isinstance(input_data,SummaryData):
        if len(input_data.scores.index) < numwinners:
            raise InvalidElection("Not enough candidates to fill desired number of seats")
        summary_data = input_data
    else:
        if input_data.shape[1] < numwinners:
            raise InvalidElection("Not enough candidates to fill desired number of seats")
        summary_data = get_summary_data(input_data)
    
    while len(results['elected']) < numwinners:
        
        eligible = copy.deepcopy(summary_data).drop(results['elected'])
        round_results = Run_STAR_Round(eligible, scoring_tiebreaker=scoring_tiebreaker, runoff_tiebreaker=runoff_tiebreaker)
        results['round_results'].append(round_results)
        if isinstance(round_results['winners'], TrueTie):

            if len(round_results['winners']) + len(results['elected']) <= numwinners:
                # If multiple candidates are tied in STAR but we have enough seats to elect them all, do so
                results['elected'].extend(round_results['winners'])

            else:
                # In this case, the election returned a tie unresolveable by stated tiebreakers
                results['elected'].extend([round_results['winners']])
                return results
        else:
            results['elected'].extend(round_results['winners'])
    
    return results
