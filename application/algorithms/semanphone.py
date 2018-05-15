"""
get words which are both semantically and phonetically associated with the given word

"""

from .candidate.datamuse import meanslike
from .candidate.wordnet import senselike
from .measurement.measure import measure


def get_candidate(word):
    """get candidate word set

    @word -- the given word
    @return -- a set of candidate words
    """

    candidates = set()
    candidates |= meanslike(word)
    candidates |= senselike(word)


    # remove '_' and '-' between words --> candidates is a LIST now
    candidates = [w.replace('_', ' ') for w in candidates]
    candidates = [w.replace('-', ' ') for w in candidates]

    # remove words which contains special characters (e.g. Ann's book)
    candidates = [w for w in candidates if ''.join(w.split()).isalpha()]

    # remove phrase has more than two words
    candidates = [w for w in candidates if len(w.split()) < 3]

    # turn all words into lowercase
    candidates = [w.lower() for w in candidates]

    # remove words contain word itself
    candidates = [w for w in candidates if not (word in w)]

    return candidates


def semanphone(word):
    """finish all works here

    @word -- the given word
    @return -- a list of (word, score) pairs
    """
    # word should be lower case
    word = word.lower()

    candidates = get_candidate(word)
    performance = [(w, measure(word, w)) for w in candidates]
    winners = sorted(performance, key=lambda x:x[1], reverse=True)

    QUOTA = 5
    # change format for the database
    return [w[0] for w in winners[:min(QUOTA, len(winners))]]


def main(word):
    """for testing functions in this module
    """
    output_file = word + '_semanphone'
    with open(output_file, 'w+') as output:
        for w in semanphone(word):
            output.write("{w}\t{s}".format(w=w[0], s=w[1]))
            output.write('\n')
        print(output_file + " was generated successfully!")


if __name__ == '__main__':
    import plac
    plac.call(main)

