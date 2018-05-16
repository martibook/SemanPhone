"""
run this script seperately to prepare the test database

but since we already have backup database so we don't need to run this anymore

if you are going to run this script
remember to set working directory to semanphone/
"""

import requests


def download_test_words():

    # for getting random words
    url = "https://randomwordgenerator.com/json/words.json"

    r = requests.get(url)
    if r:
        item_list = r.json()["data"]
        with open("random_test_words", "w") as f:
            for item in item_list:
                f.write(item["word"])
                f.write('\n')

    else:
        print("failed to collect random test words from ", url)


from application.tools.database import add_new_word
from application.tools.oxford_dictionary import crawl_word, extract_definitions, extract_examples
from application.algorithms.semanphone import semanphone


def prepare_test_words():
    """
    prepare random test words and their definition, examples etc information in the database
    :return:
    """
    with open("random_test_words", "r") as f:
        for word in f:
            r = crawl_word(word)
            if r:
                definitions = extract_definitions(r.json())
                examples = extract_examples(r.json())
                asso_words = semanphone(word)
                if asso_words:
                    add_new_word(word=word, definitions=definitions, examples=examples, asso_words=asso_words)
                else:
                    print("failed to get associated words")
            else:
                print("failed to get detailed information of word '{}'".format(word))


if __name__ == '__main__':
    prepare_test_words()
