"""request words which sound like the given word from datamuse
"""

import requests
import spacy
import sys


nlp = spacy.load('en_vectors_web_lg')
url = "https://api.datamuse.com/words?sl={w}"

def soundlike(word):
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


def main():
    w = input('input a word:\n')
    while w != '':
        sound_score = soundlike(w)
        results = []
        for word in sound_score:
            so_score = sound_score[word]
            se_score = senselike(w, word)
            wh_score = so_score * se_score
            results.append((word, so_score, se_score, wh_score))
        results = sorted(results, key=lambda x: x[3], reverse=True)
        for x in results[:10]:
            print('{w}\t{s1}\t{s2}\t{s}'.format(w=x[0], s1=x[1], s2=x[2], s=x[3]))
        w = input('input a word:\n')


if __name__ == '__main__':
    main()

