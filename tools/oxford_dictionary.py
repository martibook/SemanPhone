import requests
import json

app_id = '68c7da58'
app_key = '29980f894e9be2d74afd12a6a2afe67b'


def crawl_word(word):
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + word.lower()
    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    return r


def extract_definitions(j):
    """extract definitions from a word query response json object"""
    lexEn_list = j["results"][0]["lexicalEntries"]
    en_list = [(entry, lexEn["lexicalCategory"]) for lexEn in lexEn_list for entry in lexEn["entries"]]
    sense_list = [(sense, entry[1]) for entry in en_list for sense in entry[0]["senses"]]
    definitions = [(definition, sense[1]) for sense in sense_list for definition in sense[0]["definitions"]]
    return definitions


def extract_examples(j):
    """extract examples from a word query response json object"""
    lexEn_list = j["results"][0]["lexicalEntries"]
    en_list = [entry for lexEn in lexEn_list for entry in lexEn["entries"]]
    sense_list = [sense for entry in en_list for sense in entry["senses"]]
    examples = []
    for sense in sense_list:
        if "examples" in sense:
            examps = sense["examples"]
            examples.append(examps[0]["text"])
    return examples
