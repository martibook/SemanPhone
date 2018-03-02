""" get synonyms of a word from wordnet

Usage: python wordnet.py word
output: a file contains synonyms of the word
"""

import nltk
import sys
from nltk.corpus import wordnet

similar_baseline = 0.5

def is_similar(sense1, sense2):
    """
    using wordnet.wup_similarity() to measure the similarity of two synsets

    returns:
    return true if two senses are similar
    """
    if wordnet.wup_similarity(sense1, sense2) >= similar_baseline:
        return True
    else:
        return False


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
        if not is_similar(synset, hypo_synset):
            continue
        for l in hypo_synset.lemmas():
            s.add(l.name())
    return s


def gather_hypernyms(synset):
    """
    gather the lemmas of all hypernym synsets
    """
    s = set()
    for hyper_synset in synset.hypernyms():
        if not is_similar(synset, hyper_synset):
            continue
        for l in hyper_synset.lemmas():
            s.add(l.name())
    return s


def gather_sisterms(synset):
    """
    gather all sister terms of this synset ( actuall the other hyponym synset of this synset's hypernyms )
    """
    s = set()
    for hyper_synset in synset.hypernyms():
        for sis_synset in hyper_synset.hyponyms():
            if not is_similar(synset, sis_synset):
                continue
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


def gather_from_wordnet(word_id):
    """ get a set of synonyms of the word_id from wordnet corpus

    arguments:
    @word_id  a word

    returns:
    a set of synonyms of word_id
    """

    synonyms = set()
    core_sets = set()  # record all the synsets can be derived from all close words(depth=1)

    core_sets |= set(wordnet.synsets(word_id))

#    # get all core words
#    core_words = set()
#    for synset in wordnet.synsets(word_id):
#        for l in synset.lemmas():
#            core_words.add(l.name())
#
#    # get all core synsets
#    for word in core_words:
#        core_sets |= set(wordnet.synsets(word))

    for synset in core_sets:
        synonyms |= gather_all(synset)

    # take out the word itself
    synonyms -= set([ word_id ])

    return synonyms


def main():
    # get command line arguments
    if len(sys.argv) == 2:
        word_id = sys.argv[1]
        output_file = sys.argv[1] + "_wordnet_synonyms"
    else:
        print("usage: python wordnet.py word")
        return

    synonyms = gather_from_wordnet(word_id)

    with open(output_file, "w+") as output:
        for synonym in synonyms:
            output.write(synonym)
            output.write("\n")
        print(output_file + " generated!")


if __name__ == "__main__":
    main()

