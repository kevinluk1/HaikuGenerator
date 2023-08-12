import sys
import count_syllables
from typing import *

with open('train.txt') as in_file:
    words = set(in_file.read().split())


missing: list = []
for word in words:
    try:
        num_syllables = count_syllables.count_syllables(word)
        print(word, num_syllables)

    except KeyError:  # if word not in missing words or if word is not in cmudict
        missing.append(word)


print("Missing words:", missing, file=sys.stderr)


