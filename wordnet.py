"""
get sense like words of a word from wordnet

"""

import nltk
import sys
from nltk.corpus import wordnet

nltk.data.path.append('./nltk_data/')


def gather_itself(synset):
    """
    gather the lemmas of a synset itself

    @synset -- the given synset
    @return -- a set of words in the given synset
    """
    s = set()
    for l in synset.lemmas():
        s.add(l.name())
    return s


def gather_hyponyms(synset):
    """
    gather the lemmas of all hyponym synsets

    @synset -- the given synset
    @return -- a set of words in the hyponyms synsets of the given synset
    """
    s = set()
    for hypo_synset in synset.hyponyms():
        for l in hypo_synset.lemmas():
            s.add(l.name())
    return s


def gather_hypernyms(synset):
    """
    gather the lemmas of all hypernym synsets

    @synset -- the given synset
    @return -- a set of words in the hypernyms synsets of the given synset
    """
    s = set()
    for hyper_synset in synset.hypernyms():
        for l in hyper_synset.lemmas():
            s.add(l.name())
    return s


def gather_sisterms(synset):
    """
    gather all sister terms of this synset ( actually the other hyponym synset of this synset's hypernyms )

    @synset -- the given synset
    @return -- a set of words in the sibling synsets of the given synset
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

