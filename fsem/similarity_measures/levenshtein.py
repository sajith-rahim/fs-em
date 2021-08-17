from utils.utils import check_if_none, check_if_type

"""
modified from https://github.com/nap/jaro-winkler" \
"""


def levenshtein_similarity(s1, s2, insert=None, delete=None, substitute=None,
                           insert_default=1, delete_default=1, substitute_default=1):
    """
    Computed as 1 - normalized_levenshtein_distance.
    """
    return 1.0 - normalized_levenshtein_distance(s1, s2, insert, delete, substitute,
                                                 insert_default, delete_default, substitute_default)


def normalized_levenshtein_distance(s1, s2, insert=None, delete=None, substitute=None,
                                    insert_default=1, delete_default=1, substitute_default=1):
    """
    Computed as levenshtein - max-insert-cost(s1,s2)
    """

    insert = insert if isinstance(insert, dict) else {}
    delete = delete if isinstance(delete, dict) else {}
    substitute = substitute if isinstance(substitute, dict) else {}

    def compute_insert_cost(s):
        cost = 0
        for c in s:
            cost += insert[c] if c in insert else insert_default
        return cost

    lev = levenshtein_distance(s1, s2, insert, delete, substitute,
                               insert_default, delete_default, substitute_default)

    max_cost = max(compute_insert_cost(s1), compute_insert_cost(s2))

    if max_cost < lev:
        raise ValueError('Illegal value of operation cost')

    if max_cost == 0:
        return 0

    return float(lev) / max_cost


def levenshtein_distance(s1, s2, insert=None, delete=None, substitute=None,
                         insert_default=1, delete_default=1, substitute_default=1):
    """
    The Levenshtein distance between two words is the minimum number of single-character edits (insertions, deletions or
     substitutions) required to change one word into the other.
    Args:
        s1 (str): Sequence 1.
        s2 (str): Sequence 2.
        insert (dict(str, int), optional): Insert cost of characters. Defaults to None.
        delete (dict(str, int), optional): Delete cost of characters. Defaults to None.
        substitute (dict(str, dict(str, int)), optional): Substitute cost of characters. Defaults to None.
        insert_default (int, optional): Default value of insert cost. Defaults to 1.
        delete_default (int, optional): Default value of delete cost. Defaults to 1.
        substitute_default (int, optional): Default value of substitute cost. Defaults to 1.
    Returns:
        int: Levenshtein Distance.
    Examples:
        >>> levenshtein_distance('ab', 'abc')
        1
        >>> levenshtein_distance('a', 'abc', insert = {'c':50},
        ... insert_default=100, delete_default=100, substitute_default=100)
        150
    """

    check_if_none(s1, s2)
    check_if_type(str, s1, s2)

    insert = insert if isinstance(insert, dict) else {}
    delete = delete if isinstance(delete, dict) else {}
    substitute = substitute if isinstance(substitute, dict) else {}

    # s1 = utils.unicode_normalize(s1)
    # s2 = utils.unicode_normalize(s2)

    n1, n2 = len(s1), len(s2)
    if n1 == 0 and n2 == 0:
        return 0

    # if n1 == 0 or n2 == 0:
    #     return max(n1, n2)

    dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    for i in range(n1 + 1):
        for j in range(n2 + 1):
            if i == 0 and j == 0:  # [0,0]
                continue
            elif i == 0:  # most top row
                c = s2[j - 1]
                dp[i][j] = insert[c] if c in insert else insert_default
                dp[i][j] += dp[i][j - 1]
            elif j == 0:  # most left column
                c = s1[i - 1]
                dp[i][j] = delete[c] if c in delete else delete_default
                dp[i][j] += dp[i - 1][j]
            else:
                c1, c2 = s1[i - 1], s2[j - 1]
                insert_cost = insert[c2] if c2 in insert else insert_default
                delete_cost = delete[c1] if c1 in delete else delete_default
                substitute_cost = substitute[c1][c2] \
                    if c1 in substitute and c2 in substitute[c1] else substitute_default

                if c1 == c2:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i][j - 1] + insert_cost,
                                   dp[i - 1][j] + delete_cost,
                                   dp[i - 1][j - 1] + substitute_cost)
    return dp[n1][n2]
