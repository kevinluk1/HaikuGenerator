import sys
import logging
import random
from collections import defaultdict
from count_syllables import count_syllables
from typing import *

# logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def load_training_file(file) -> str:
    with open(file) as f:
        raw_haiku = f.read()
        return raw_haiku


def prep_training(raw_haiku  : str) -> list:
    corpus = raw_haiku.replace('\n', ' ').split()
    return corpus


def map_word_to_word(corpus : list) -> dict:  # one word markov model
    limit = len(corpus) - 1  # off by 1 indexing
    dict1_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            key = word
            suffix = corpus[index + 1]
            dict1_to_1[key].append(suffix)

    logging.debug("map_word_to_word results for \"sake\" = %s\n",
                  dict1_to_1['sake'])

    return dict1_to_1


def map_2_words_to_word(corpus: list) -> dict:  # two word markov model
    limit = len(corpus) - 2
    dict2_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            key = word + ' ' + corpus[index + 1]  # two word key
            suffix = corpus[index + 2]
            dict2_to_1[key].append(suffix)

    logging.debug("map_2_words_to_word results for \"sake jug\" = %s\n",
                  dict2_to_1['sake jug'])
    return dict2_to_1


def seed_word(corpus: list) -> tuple:
    word = random.choice(corpus)
    num_sylls = count_syllables(word)
    if num_sylls <= 4:
        return (word, num_sylls)
    else:
        return seed_word(corpus)
