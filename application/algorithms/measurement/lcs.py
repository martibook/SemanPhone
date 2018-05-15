"""
calculate the longest common sequence of two sequences
"""

import numpy as np


def lcs(a, b):
    """ find the longest common subsequence of two sequences

    @a -- a sequence
    @b -- a sequence
    @return -- the longest common subsequence
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


def main(sequence1, sequence2):
    """for testing functions in this module
    """

    a, b = sequence1, sequence2
    print('longest common subsequence of {a} and {b} is\n{lcs}'.format(a=a, b=b, lcs=lcs(a, b)))


if __name__ == '__main__':
    import plac
    plac.call(main)

