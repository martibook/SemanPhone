"""
get words which are both semantically and phonetically associated with the given word

"""

import sys
import csv
from datamuse import meanslike
from wordnet import senselike
from pav import PAV
from sav import SAV


def get_candidate(word):

    ## get candidate word set
    candidates = set()
    candidates |= meanslike(word)
    candidates |= senselike(word)

    ## clean words in candidate set
    # words contain word itself
    # ! candidates is a LIST now
    candidates = [w for w in candidates if not (word in w)]

    # remove '_' and '-' between words
    candidates = [w.replace('_', ' ') for w in candidates]
    candidates = [w.replace('-', ' ') for w in candidates]

    # remove words which contains special characters (e.g. Ann's book)
    candidates = [w for w in candidates if ''.join(w.split()).isalpha()]

    # remove phrase hase more than two words
    candidates = [w for w in candidates if len(w.split()) < 3]

    # turn all words into lowercase
    candidates = [w.lower() for w in candidates]

    return candidates


def metric(word1, word2):
    """
    combine phonetic association value and semantic association value
    """
    # contribution parameter of phonetic association value
    ALPHA = 0.68

    pa_v = PAV(word1, word2)
    sa_v = SAV(word1, word2)
    if pa_v is None or sa_v is None:
        return 0

    return ALPHA * pa_v + (1 - ALPHA) * sa_v


def semanphone(word):
    """finish all works here
    """
    QUOTA = 5
    candidates = get_candidate(word)
    performance = [(w, metric(word, w)) for w in candidates]
    winners = sorted(performance, key=lambda x:x[1], reverse=True)
    return winners[:min(QUOTA, len(winners))]


def main(word):

    # write into file
    output_file = word + '_semanphone'
    with open(output_file, 'w+') as output:
        for w in semanphone(word):
            output.write("{w}\t{s}".format(w=w[0], s=w[1]))
            output.write('\n')
        print(output_file + " was generated successfully!")


if __name__ == '__main__':
    import plac
    plac.call(main)

