class TestSTAR:
    pass
    # def test_election_with_one_record_only(self):
    #     columns = ['Allison', 'Bill', 'Carmen']
    #     election = [[5, 2, 1, 4]]
    #     ballots = pd.DataFrame(columns=columns, data=election)
    #     results = STAR(ballots)
    #     assert results['elected'] == ['Allison']

    # def test_mismatch_between_number_of_candidates_and_ballots(self):
    #     with pytest.raises(ValueError):
    #         columns = ['Allison', 'Bill', 'Carmen']
    #         election = [[5, 2, 1, 4],
    #                     [5, 2, 1, 0],
    #        ]
    #         ballots = pd.DataFrame(columns=columns, data=election)
    #         results = STAR(ballots)
        # how to trigger error:
        # expected = raises(ValueError) - mismatch between number of candidates and election ballots:
        #                                 number of columns in election must be the same as number of candidates;
        # assert(False)

    # # should this test case work/pass?
    # # or we need a negative test case (confirm that it should fail)
    # def test_floats_and_strings(self):
    #     columns = ['Allison', 'Bill', 'Carmen', 'Doug']
    #     election = [[5.0, ' 2 ', 1, 4],
    #                 [5, 2, 1, 0],
    #                 [5, 2, 1, 0],
    #                 [5, 2, 1, 0],
    #                 [5, 3, 4, 0],
    #                 [5, 1, 4, 0],
    #                 [5, 1, 4, 0],
    #                 [4, 0, 5, 1],
    #                 [3, 4, 5, 0],
    #                 [3, 5, 5, 5]]
    #     ballots = pd.DataFrame(columns=columns, data=election)
    #     results = STAR(ballots)
    #
    #     # expected = do we want to convert the text '4' to a number?;
    #     # expected = [["Allison"], ["Carmen"], ["Bill", "Doug"]];
    #     assert results['elected'] == ['Allison']
    #     assert results['round_results'][0]['runner_up'] == 'Carmen'

if __name__ == '__main__':
    pytest.main()
