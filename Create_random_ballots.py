import random
import itertools
import string, collections


def create_rand_ballots(voters=None, candidates=None, groups=None, max_score=None, compressed=True):
    MAX_SCORE = 10
    if max_score is None:
        max_score = 3  # entered as 'plus one'
    else:
        if max_score > MAX_SCORE:
            entered_max_score = max_score
            max_score = MAX_SCORE
            print(f" (!) Warning: max score reduced from {entered_max_score} to {MAX_SCORE} ")
        elif max_score <= MAX_SCORE:
            max_score = max_score

    MAX_VOTERS = 99_999_999
    if voters is None:
        voters = random.randint(9, 22)
    else:
        if voters > MAX_VOTERS:
            entered_max_voters = voters
            voters = MAX_VOTERS
            print(f" (!) Warning: voters reduced from {entered_max_voters} to {MAX_VOTERS} ")
        elif voters <= MAX_VOTERS:
            voters = voters

    MAX_CANDIDATES = 50
    if candidates is None:
        candidates = random.randint(5, 5)
    else:
        if candidates > MAX_CANDIDATES:
            entered_max_candidates = candidates
            candidates = MAX_CANDIDATES
            print(f" (!) Warning: candidates reduced from {entered_max_candidates} to {MAX_CANDIDATES} ")
        elif candidates <= MAX_CANDIDATES:
            candidates = candidates

    if groups is None:
        if candidates == 2:
            groups = 1
        elif candidates == 3:
            groups = random.randint(1, 3)
        elif candidates <= 6:
            groups = random.randint(1, 3)
        elif candidates > 6:
            groups = random.randint(2, 4)
    else:
        entered_groups = groups
        if groups > candidates:
            print(f" (!) Warning: groups reduced from {entered_groups} to {candidates}")
            groups = candidates
        else:
            groups = entered_groups

    candidates_names_potential = list(string.ascii_uppercase + string.ascii_lowercase)
    candidates_names = candidates_names_potential[0:candidates]
    random.shuffle(candidates_names)

    product = itertools.product(list(range(max_score)), repeat=candidates)
    temp_prod = list(product)
    ballots = random.choices(list(temp_prod), k=voters)
    ballots_as_string = []
    for e in list(ballots):
        temp = str(e)
        temp = temp.replace("(", "")
        temp = temp.replace(")", "")
        temp = temp.replace(" ", "")
        ballots_as_string.append(temp)
        c = collections.Counter(ballots_as_string)
    final_as_string = "\n".join(ballots_as_string)
    final_as_counter = ""
    for e, i in c.items():
        final_as_counter += f"{i}: {e} \n"

        if compressed is True:
            result = str(final_as_counter)
        else:
            result = final_as_string

    # assign candidates to groups / affiliation
    # candidate who remain unaffiliated are in special group 'zero'
    temp_dict_with_groups = {}
    for e in candidates_names:
        temp = random.randint(0, groups)
        temp = "Grp " + str(temp)
        temp_dict_with_groups[temp] = temp_dict_with_groups.get(temp, '') + str(e)
    temp_dict_with_groups = sorted(temp_dict_with_groups.items())

    groups_as_table = ""
    len_of_groups = len(temp_dict_with_groups)
    for e in temp_dict_with_groups:
        groups_as_table += "".join(e[0]) + ":   " + "".join(e[1]) + "\n"
    return (
        "Number of Voters = " + str(voters),
        "Max Score = " + str(max_score - 1),
        "Affiliation Grps = " + str(groups),
        "Affiliation and Candidates assignment: ",
        groups_as_table,
        "Number of Candidates = " + str(candidates),
        ",".join(sorted(candidates_names)),
        result,
    )


for e in range(3):
    a = create_rand_ballots()
    for e in a:
        print(e)
