from typing import *
import sys
from string import punctuation
import json
from nltk.corpus import cmudict

with open('missing_words.json') as f:
    missing_words = json.load(f)
cmudict = cmudict.dict()


def count_syllables(words) -> int:
    words = words.replace('-','')
    words = words.lower().split()
    num_sylls = 0
    for word in words:
        word = word.strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]
    if word in missing_words:
        num_sylls += missing_words[word]

    else:
        for phonemes in cmudict[word][0]:
            for phoneme in phonemes:
                if phoneme[-1].isidigit():
                    num_sylls +=1
    return num_sylls