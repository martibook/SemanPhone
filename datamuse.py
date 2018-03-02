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


def extract_from_json(jobject):
    """ extract words from the passing json object

    arguments
    a json object

    returns
    a set of words
    """
    s = set()
    for item in jobject:
        s.add(item.get('word'))
    return s


def gather_from_datamuse(word_id):
    """gather synonyms of word_id from datamuse

    returns:
    a set of synonyms
    """
    url = request_url.format(c="ml", w=word_id)
    response = requests.get(url)
    synonyms = extract_from_json(response.json())
    return synonyms


def main():
    if len(sys.argv) == 2:
        word_id = sys.argv[1]
        output_file = word_id + "_datamuse_synonyms"
    else:
        print('Usage: python datamuse.py word')
        return

    with open(output_file, 'w+') as output:
        for w in gather_from_datamuse(word_id):
            output.write(w)
            output.write('\n')
        print(output_file + " generated successfully!")


if __name__ == '__main__':
    main()


