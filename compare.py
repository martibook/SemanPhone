import sys
from hyphenate import hyphenate_word
from pronouncing import phones_for_word
import requests
import re
from lcs import lcs
from lcs import lcs_count


def compare_syllables(word1, word2):
    """ compare the results of hyphenate_word(word1) and hyphenate_word(word2)

    WELL THIS ONE IS NOT A GOOD METHOD, AND I WILL NOT USE IT IN FACT

    arguments
    word1, word2  a list of syllable parts of a word

    returns
    a percentage which shows the extend of similarity
    """
    output = "The Longest Common Subsequence of syllables of {a} and {b} is '{c}'"
    syllable1 = hyphenate_word(word1)
    syllable2 = hyphenate_word(word2)
    common_syllable = lcs(syllable1, syllable2)
#    print(output.format(a=syllable1, b=syllable2, c=common_syllable))
    len1 = len(syllable1)
    len2 = len(syllable2)
    lencommon = lcs_count(syllable1, syllable2)
    similarity = 2.0 * lencommon / (len1 + len2)  # weighted average
    return similarity
#    return format(similarity, '.2%')
#    print('Similarity: {}'.format(format(similarity, '.2%')))


def get_phoneme(word):
    """ get phoneme from CMU dictionary """
    if word.isalpha():
        phoneme_list = phones_for_word(word)
        if phoneme_list:
            return phoneme_list[0]

    # phrase
    word = word.replace(' ', '_')
    words = word.split('_')
    words_pron = []
    for w in words:
        p_list = phones_for_word(w)
        if p_list:
            words_pron.append(p_list[0])
        else:
            return None  # if any part of the phrase gets no pronounciation
    return ' '.join(words_pron)


def compare_phonemes(word1, word2):
    """ compare the results of phones_for_word(word1) and phones_for_word(word2)

    arguments
    word1, word2  a string of phonetic representation of a word

    returns
    a percentage which shows the extend of similarity
    """
    output = "The Longest Common Subsequence of phonemes of [{a}] and [{b}] is '{c}'"

    phoneme1 = get_phoneme(word1)
    phoneme2 = get_phoneme(word2)
    if phoneme1 is None or phoneme2 is None:
        return None

    common_phoneme = lcs(phoneme1, phoneme2)
#    print(output.format(a=phoneme1, b=phoneme2, c=common_phoneme))
    len1 = len(phoneme1.replace(' ', ''))
    len2 = len(phoneme2.replace(' ', ''))
    lencommon = len(common_phoneme.replace(' ', ''))
    similarity = 2.0 * lencommon / (len1 + len2)  # weighted average
    return similarity
#    return format(similarity, '.2%')
#    print('Similarity: {}'.format(format(similarity, '.2%')))


def main():
    if len(sys.argv) == 3:
        # command line mode
        word1 = sys.argv[1]
        word2 = sys.argv[2]
        print('Compare syllables -- Similarity: {}'.format(compare_syllables(word1, word2)))
        print('Compare phonemes -- Similarity: {}'.format(compare_phonemes(word1, word2)))
    elif len(sys.argv) == 2:
        input_file = sys.argv[1]
        output_file = 'comparison_result_of_' + input_file
        compare_result = '{w1}\t{w2}\t{sim_syllable}\t{sim_phoneme}'
        with open(input_file, 'r') as vocabulary:
            with open(output_file, 'w+') as output:
                output.write(compare_result.format(w1='word1', w2='word2', sim_syllable='Compare Syllables', sim_phoneme='Compare Phonemes'))
                output.write('\n\n')
                for line in vocabulary:
                    words = line.split()
                    if len(words) != 2:
                        continue
                    # only process those independent words
                    word1 = words[0]
                    word2 = words[1]
                    output.write(compare_result.format(w1=word1, w2=word2, sim_syllable=compare_syllables(word1, word2), sim_phoneme=compare_phonemes(word1, word2)))
                    output.write('\n')
        print('{} generated successfully!'.format(output_file))

    else:
        print("Usage:\n  python compare.py word1 word2\n  python compare.py file")


if __name__ == '__main__':
    main()

