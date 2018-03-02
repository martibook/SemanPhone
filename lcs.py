""" calculate the lcs of two sequences
"""

import numpy as np
from pronouncing import phones_for_word as pronounce
import sys

def lcs(a, b):
    """ find the longest common subsequence of two sequences

    arguments
    a, b  a sequence

    returns
    the longest common subsequence

    """
    m, n = len(a), len(b)

    D = np.zeros((m+1, n+1), dtype=object)
    D[:] = ''

    for i_a, unit_a in enumerate(a, 1):
        for i_b, unit_b in enumerate(b, 1):
            if unit_a == unit_b:
                D[i_a, i_b] = D[i_a-1, i_b-1] + unit_a
            else:
                D[i_a, i_b] = D[i_a-1, i_b] if len(D[i_a-1, i_b]) > len(D[i_a, i_b-1]) else D[i_a, i_b-1]

    return D[m,n]


def lcs_count(a, b):
    """ find the length of longest common subsequence of two sequences

    arguments
    a, b  a sequence

    returns
    the length of the lcs

    """
    m, n = len(a), len(b)

    D = np.zeros((m+1, n+1), dtype=object)
    D[:] = 0

    for i_a, unit_a in enumerate(a, 1):
        for i_b, unit_b in enumerate(b, 1):
            if unit_a == unit_b:
                D[i_a, i_b] = D[i_a-1, i_b-1] + 1
            else:
                D[i_a, i_b] = D[i_a-1, i_b] if D[i_a-1, i_b] > D[i_a, i_b-1] else D[i_a, i_b-1]

    return D[m,n]


if __name__ == '__main__':
    if len(sys.argv) == 3:
        a = sys.argv[1]
        b = sys.argv[2]
        print('longest common subsequence of {a} and {b} is\n{lcs}'.format(a=a, b=b, lcs=lcs(a, b)))
        print('the length of the longest common subsequence of {a} and {b} is\n{lcs}'.format(a=a, b=b, lcs=lcs_count(a, b)))
    else:
        print('Usage:\npython lcs.py string1 string2')

