import pytest
import pandas as pd


@pytest.fixture()
def original_example() -> pd:
    # load_configuration
    # load_all_votes(test_file_1)
    Candidates = ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4']
    Red = 61 * [[5.0, 5.0, 5.0, 5.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0]]
    blue = 39 * [[0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 5.0, 5.0, 5.0, 5.0]]
    tie_breaker = [[2.0, 3.0, 4.0, 5.0, 2.0, 3.0, 4.0, 5.0, 2.0, 3.0, 4.0, 5.0]]
    all_parties = Red + blue + tie_breaker

    s = pd.DataFrame(all_parties, columns=Candidates)

    return s

@pytest.fixture()
def original_results() -> list:
    return ['A4']

