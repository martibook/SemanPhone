"""
gather synonyms from datamuse ( it has dozens of dictionaries besides Wordnet )
but it seems doesn't has oxford dictionary included

after trials, this is not a good idea...
gather other related words ( except for synonyms ) from datamuse ( particularlly google books ngram )

they are all not good constraints actually...
rel_jja: popular nouns modified by the given adjective
rel_jjb: popular adjectives to modify the given noun
rel_trg: words that are statistically associated with the query word in the same piece of text
rel_bga: frequent followers
rel_bgb: frequent predecessors
"""

import sys
import requests
import json

# c means constraint, w mean word
request_url = "https://api.datamuse.com/words?{c}={w}"


def soundslike(word):
    """find sounds like words from datamuse

    @word -- the given word
    @return -- a set of words
    """
    # item {'word': --, 'score': --, 'numSyllables': --}
    item_list = requests.get(request_url.format(c="sl", w=word)).json()
    return set([item['word'] for item in item_list])


def meanslike(word):
    """gather means like words from datamuse

    @word -- the given word
    @return -- a set of words
    """
    item_list = requests.get(request_url.format(c="ml", w=word)).json()
    return set([item['word'] for item in item_list])


def main(word):
    """for testing functions in this module

    @word -- the given word
    """
    output_file = word + "_datamuse"
    with open(output_file, 'w+') as output:
        # test meanslike
#        for w in list(meanslike(word)):
        # test soundslike
        for w in list(soundslike(word)):
            output.write(w)
            output.write('\n')
        print(output_file + " generated successfully!")


if __name__ == '__main__':
    import plac
    plac.call(main)

