"""request words which sound like the given word from datamuse
"""

import requests
import spacy
import sys


nlp = spacy.load('en_vectors_web_lg')
url = "https://api.datamuse.com/words?sl={w}"

def soundslike(word):
    """find words whose sound is close to the given word
    @return: a dict of {'word': sounds_similarity_score}, the score locates between [0, 100]
    """
    # item {'word': --, 'score': --, 'numSyllables': --}
    item_list = requests.get(url.format(w=word)).json()
    return {item['word']:item['score'] for item in item_list}


def senselike(word1, word2):
    """return sense-like-similarity of word1 and word2
    @return: a float number between [0, 1]
    """
    vector1 = nlp.vocab[word1]
    vector2 = nlp.vocab[word2]
    return vector1.similarity(vector2)


def phoneseman(word_id):
    """find phonetically and semantically both related words of the given word w
    choose words first according to phonetic criteria and then semantic
    @w: input word
    @return: a list of tuple (word, similarity)
    """
    homonyms = soundslike(word_id)

    results = []
    for word, sound_similarity in homonyms.items():
        results.append((word, sound_similarity * senselike(word_id, word) / 100))

    # clear word_id itself out of homonyms
    results = [ x for x in results if x[0].find(word_id) == -1]

    # clean out None similarity and sort by similarity
    results = [ x for x in results if x[1] is not None ]
    results = sorted(results, key=lambda x: x[1], reverse=True)

    # format similarity into percentage
    results = [ (x[0], format(x[1], '.2%')) for x in results]

    return results[:min(100, len(results))]


def main():
    if len(sys.argv) == 2:
        word_id = sys.argv[1]
    else:
        print('Usage: python {} word\n'.format(sys.argv[0]))
        return

    results = phoneseman(word_id)
    for x in results[:min(10, len(results))]:
        print('{w}\t{s}'.format(w=x[0], s=x[1]))


if __name__ == '__main__':
    main()

