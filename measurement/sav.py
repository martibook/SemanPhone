"""
calculate semantic association value

value locates in [0, 1]
"""

# import spacy
# nlp = spacy.load('en_vectors_web_lg')

import en_vectors_web_lg
nlp = en_vectors_web_lg.load()


def SAV(word1, word2):
    """calculate semantic association value of two words

    @word1 -- the first word
    @word2 -- the second word
    @return -- a float number means semantic association value
    """
    vector1 = nlp.vocab[word1]
    vector2 = nlp.vocab[word2]
    return vector1.similarity(vector2)


def main(word1, word2):
    """for testing functions in this module
    """
    print('word1: ', word1)
    print('word2: ', word2)
    print('semantic association value: {v: .2%}'.format(v=SAV(word1, word2)))


if __name__ == '__main__':
    import plac
    plac.call(main)

