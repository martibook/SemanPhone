"""
get sense like words of a word from wordnet

"""

import nltk
import sys
from nltk.corpus import wordnet

nltk.data.path.append('./nltk_data/')


def gather_all(synset):
    """
    gather synonyms from all sources
    """
    s = set()
    s |= {l.name() for l in synset.lemmas()}
    s |= {l.name() for hypo_synset in synset.hyponyms() for l in hypo_synset.lemmas()}
    s |= {l.name() for hyper_synset in synset.hypernyms() for l in hyper_synset.lemmas()}
    s |= {l.name() for hyper_synset in synset.hypernyms() for sis_synset in hyper_synset.hyponyms() for l in sis_synset.lemmas()}
    return s


def senselike(word):
    """ get a list of sense like words of the given word from wordnet corpus

    @word -- the given word
    @return -- a set of words which sense like the given word
    """
    s = set()
    for synset in wordnet.synsets(word):
        s |= gather_all(synset)
    return s


def main(word):
    """for testing functions in this module
    """

    output_file = word + "_wordnet"
    with open(output_file, "w+") as output:
        for w in list(senselike(word)):
            output.write(w)
            output.write("\n")
        print(output_file + " generated successfully!")


if __name__ == "__main__":
    import plac
    plac.call(main)

