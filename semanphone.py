""" get a list of word which are similar to the input_word both semantically and phonetically

"""

import sys
import csv
from wordnet import gather_from_wordnet
from oxford import gather_from_oxford
from datamuse import gather_from_datamuse
from compare import compare_phonemes


def semanphone(word_id):

    # get synonyms
    synonyms = set()
    from_oxford = gather_from_oxford(word_id)
    from_wordnet = gather_from_wordnet(word_id)
    from_datamuse = gather_from_datamuse(word_id)
    if from_oxford is not None:
        synonyms |= from_oxford
    if from_wordnet is not None:
        synonyms |= from_wordnet
    if from_datamuse is not None:
        synonyms |= from_datamuse

    # compare phonetic similarity
    comparison = []
    for ele in synonyms:
        comparison.append((ele, compare_phonemes(word_id, ele)))

    # clean out None similarity and sort by similarity
    comparison = [ x for x in comparison if x[1] is not None ]
    comparison = sorted(comparison, key=lambda x:x[1], reverse=True)

    # format similarity into percentage
    comparison = [ (x[0], format(x[1], '.2%')) for x in comparison ]

    # remove '_' between words
    comparison = [ (x[0].replace('_', ' '), x[1]) for x in comparison ]

    return comparison[0:min(100,len(comparison))]


def main():
    if len(sys.argv) == 2:
        word_id = sys.argv[1]
    else:
        print('Usage: python semanphone.py word\n')
        return

    comparison = semanphone(word_id)

    # output top results on command line
    for i in range(min(10, len(comparison))):
        print("{w}  ---  {p}".format(w=comparison[i][0], p=comparison[i][1]))

#    # write into file
#    output_file = word_id + '_semanphone_results.csv'
#    with open(output_file, 'w+') as output:
#        writer = csv.writer(output)
#        for ele in comparison:
#            writer.writerow(ele)
#        print(output_file + " was generated successfully!")


if __name__ == '__main__':
    main()

