"""
request for sysnonyms of a word in json format
and then extract those synonyms words only to output into a file

usage: python synonym.py word
"""

import requests
import json
import sys

from extract_oxford import get_synonyms


def gather_from_oxford(word_id):
    """ gather a set of synonyms of a word from oxford dictionary

    arguments:
    @word_id  a word

    returns:
    a set of synonyms
    """

    # replace with your own app_id and app_key
    app_id = '68c7da58'
    app_key = '29980f894e9be2d74afd12a6a2afe67b'

    # find the synonyms
    language = 'en'
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() + '/synonyms'
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    if r.status_code == 200:
#        print("get data from oxford dictionary successfully")
        jobject = r.json()
    else:
#        print("get no results about the word")
        return

    synonyms = set()
    for synonym_list in get_synonyms(jobject):
        synonyms |= set(synonym_list)

    return synonyms


def main():

    if len(sys.argv) == 2:
        word_id = sys.argv[1]
        output_file = sys.argv[1] + "_oxford_synonnyms"
    else:
        print("usage: python synonym.py word")
        return

    synonyms = gather_from_oxford(word_id)

    with open(output_file, "w+") as output:
        for synonym in synonyms:
            output.write(synonym)
            output.write("\n")
        print("{} generated!".format(output_file))


if __name__ == "__main__":
    main()


