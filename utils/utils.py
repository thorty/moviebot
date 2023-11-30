from langdetect import detect
from difflib import get_close_matches
import re
import json

# Function to find all close matches of 
# input string in given list of possible strings
def closeMatches(patterns, word):
     return get_close_matches(word, patterns)

def dump_json(data):
    json_object = json.dumps(data, indent=4)
    with open("dump.json", "w") as outfile:
        outfile.write(json_object)

def read_jsondump():
    # Opening JSON file
    with open('dump.json', 'r') as openfile: 
        # Reading from json file
        json_object = json.load(openfile)
    return json_object

def detect_ipnut_lang(input: str):
    lang = detect(input)
    return lang

def getTitlesFromOutput(text: str):

    titles =""
    pattern = re.compile(r'^(.*?):\s', re.MULTILINE)
    matches = re.findall(pattern, text)

    for match in matches:
       titles += ", " +match

    if len(titles.split("("))>1:
        titles=""
        pattern = r'\d+\.\s([^:]+)'
        matches = re.findall(pattern, text)

        for match in matches:
            titles += ", " +match

    return titles




