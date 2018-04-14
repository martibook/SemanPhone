"""
calculate semantic association value
"""

# import spacy
# nlp = spacy.load('en_vectors_web_lg')

import en_vectors_web_lg
nlp = en_vectors_web_lg.load()


def SAV(word1, word2):
    """return sense-like-similarity of word1 and word2
    @return: a float number between [0, 1]
    """
    vector1 = nlp.vocab[word1]
    vector2 = nlp.vocab[word2]
    return vector1.similarity(vector2)


def main(word1, word2):
    print('word1: ', word1)
    print('word2: ', word2)
    print('semantic association value: {v: .2%}'.format(v=SAV(word1, word2)))


if __name__ == '__main__':
    import plac
    plac.call(main)

