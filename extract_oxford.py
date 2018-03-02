"""
extract synonyms from a json file of a word ( the json file is crawled from oxford dictionary api )

usage: python extract_synonyms.py input.json output.txt

"""

import json
import sys

the_key = "synonyms"


def extract(synonym_list):
    l = []
    for obj in synonym_list:
        l.append(obj["text"])
    return l

def get_synonyms(jobject):
    """ a generator
    extract all synonyms of a word from a json object
    and the structure of the json object is known as that in the response of oxford dictionary api

    arguments
    json object

    returns
    a list of synonyms
    """
    if not isinstance(jobject, dict):
        # some where a string instead of a dict may be inside a list
        return

    if the_key in jobject:
        yield extract(jobject[the_key])

    for each in jobject:
        if isinstance(jobject[each], list):
            for obj in jobject[each]:
                for synonym in get_synonyms(obj):
                    yield synonym



if __name__ == "__main__":

    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = "school_synonyms.json"
        output_file = "extracted_synonyms.txt"

    with open(input_file, "r") as jfile:
        jobject = json.load(jfile)
        results = []
        for synonym_list in get_synonyms(jobject):
            results += synonym_list

        with open(output_file, "w+") as output:
            for result in results:
                output.write(result)
                output.write('\n')


