"""
calculate phonetic association value

value locates in [0,1]
"""


from measurement.lcs import lcs
from pronouncing import phones_for_word


def get_phoneme(word):
    """get phoneme from CMU dictionary
    
    @word -- the given word
    @return -- phonetic symbol presentation of the given word
    """
    words = word.split()
    words_pro = []

    # e.g. english dictionary -- 'IH1 NG G L IH0 SH' + 'D IH1 K SH AH0 N EH2 R IY0'  ->  'IH1 NG G L IH0 SH D IH1 K SH AH0 N EH2 R IY0'
    for w in words:
        # every word will get a list of pronunciation, we just get the first element in this list
        phoneme_list = phones_for_word(word)
        if phoneme_list:
            words_pro.append(phoneme_list[0])
        else:
            # if any part of the phrase gets no pronounciation
            return None

    return ' '.join(words_pro)


def PAV(word1, word2):
    """ compare the pronunciation of two words using LCS

    @word1 -- the first word
    @word2 -- the second word
    @return -- phonetic association value of two given words
    """
    phoneme1 = get_phoneme(word1)
    phoneme2 = get_phoneme(word2)
    if phoneme1 is None or phoneme2 is None:
        return None

    common_phoneme = lcs(phoneme1, phoneme2)
    len1 = len(phoneme1.replace(' ', ''))
    len2 = len(phoneme2.replace(' ', ''))
    lencommon = len(common_phoneme.replace(' ', ''))
    similarity = 2.0 * lencommon / (len1 + len2)  # weighted average
    return similarity


def main(word1, word2):
    """for testing functions in this module
    """
    print('word1: ', word1)
    print('word2: ', word2)
    print('phonetic association value: {v: .2%}'.format(v=PAV(word1, word2)))


if __name__ == '__main__':
    import plac
    plac.call(main)

