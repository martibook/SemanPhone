""" get sense like words of a word from wordnet

Usage: python wordnet.py word
output: a file contains sense like words of the given word
"""

import nltk
import sys
from nltk.corpus import wordnet

nltk.data.path.append('./nltk_data/')


def gather_itself(synset):
    """
    gather the lemmas of a synset itself
    """
    s = set()
    for l in synset.lemmas():
        s.add(l.name())
    return s


def gather_hyponyms(synset):
    """
    gather the lemmas of all hyponym synsets
    """
    s = set()
    for hypo_synset in synset.hyponyms():
        for l in hypo_synset.lemmas():
            s.add(l.name())
    return s


def gather_hypernyms(synset):
    """
    gather the lemmas of all hypernym synsets
    """
    s = set()
    for hyper_synset in synset.hypernyms():
        for l in hyper_synset.lemmas():
            s.add(l.name())
    return s


def gather_sisterms(synset):
    """
    gather all sister terms of this synset ( actually the other hyponym synset of this synset's hypernyms )
    """
    s = set()
    for hyper_synset in synset.hypernyms():
        for sis_synset in hyper_synset.hyponyms():
            for l in sis_synset.lemmas():
                s.add(l.name())
    return s


def gather_all(synset):
    """
    gather synonyms from all sources
    """
    s = set()
    s |= gather_itself(synset)
    s |= gather_hyponyms(synset)
    s |= gather_hypernyms(synset)
    s |= gather_sisterms(synset)
    return s


def senselike(word):
    """ get a list of sense like words of the given word from wordnet corpus

    arguments:
    @word_id  a word

    returns:
    a set of synonyms of word_id
    """
    s = set()
    for synset in wordnet.synsets(word):
        s |= gather_all(synset)
    return s


def main(word):

    output_file = word + "_wordnet"
    with open(output_file, "w+") as output:
        for w in list(senselike(word)):
            output.write(w)
            output.write("\n")
        print(output_file + " generated successfully!")


if __name__ == "__main__":
    import plac
    plac.call(main)

