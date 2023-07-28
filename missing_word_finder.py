# 1. Training Corpus
# 2. Syllable Count Corpus
# 3. Missing Words dictionary

# Overlay the syllable count corpus (cmudict) with the training corpus (train.txt). Wwords that appear in the training -->
# corpus but NOT the syllable count corpus get added to the MISSING WORDS DICTIONARY, which iswritten to missing_words.json

# Write a program that takes the training corpus(train.txt) and compares it against cmudict (syllable count corpus) then ->
# finds the words in the training corpus that are not in cmudict and allows the user to manually enter the number ->
# of syllables for those words, which is then saved to the missing_words.json file

import sys
from string import punctuation
import pprint
import json
from nltk.corpus import cmudict
from typing import *

cmudict = cmudict.dict()


def main() -> None:
    haiku: Set[str] = load_haiku('train.txt')
    exceptions: Set[str] = cmudict_missing(haiku)
    build_dict: str = input("\n Build exceptions dictionary (y/n)\n")
    if build_dict.lower() == 'n':
        sys.exit()

    else:
        missing_words_dict: dict[str, int] = make_exceptions_dict(exceptions)
        save_exceptions(missing_words_dict)


def load_haiku(filename) -> Set[str]:
    with open(filename) as filename:
        haiku: set = set(filename.read().replace('-', '').split())
        return haiku


def cmudict_missing(word_set) -> Set[str]:
    exceptions = set()
    for word in word_set:
        word = word.lower().strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):  # curly and straight apostrophe
            word = word[:-2]
        if word not in cmudict:
            exceptions.add(word)
    print("\nexceptions:")
    print(*exceptions, sep='\n')  # splat operator to unpack, newline between each when printing
    print("\nNumber of unique words in haiku corpus = {}".format(len(word_set)))
    membership = (1 - (len(exceptions) / len(word_set))) * 100
    print("cmudict membership = {:.1f}{}".format(membership, '%'))
    return exceptions


def make_exceptions_dict(exceptions_set) -> dict[str, int]:
    """For each word in the exception_set (the set that we created by overlaying the cmudict and the haiku training corpus)
    make a dictionary with the word as the key and the number of syllables as the value (user supplied), and give the option
    to add new words"""
    missing_words = {}
    print("Input # of syllables in word. Mistakes can be corrected at the end. \n")

    # Account for all the missing words in the haiku training corpus
    for word in exceptions_set:
        while True:
            num_sylls: str = input("Enter the number of syllables in {}:".format(word))
            if num_sylls.isdigit():
                break
            else:
                print(" Not a valid answer!", file=sys.stderr)
        missing_words[word] = int(num_sylls)
        print("\n")
        pprint.pprint(missing_words, width=1)
        # Give the option to add new words after the above loop has concluded
        print("\nMake Changes to Dictionary Before Saving?")
        print(""" 0 - Exit & Save 
                      1 - Add a Word or Change a Syllable Count
                      2 - Remove a Word 
                      """)

        while True:
            choice = input("\nEnter choice: ")
            if choice == "0":
                break
            elif choice == "1":
                word = input("\nWord to add or change:")
                missing_words[word] = int(input("Enter number syllables in {}:".format(word)))
            elif choice == '2':
                word = input("\nEnter word to delete: ")
                if missing_words[word]:
                    missing_words.pop(word, None)
                else:
                    print("Does not exist in missing words!")
        return missing_words


def save_exceptions(missing_words) -> None:
    """Save the missing_words dictionary to a file"""
    json_string = json.dumps(missing_words)  # convert the missing_words dict (an object) to a json_string
    f = open('missing_words.json', 'w')  # create if it doesn't exist
    f.write(json_string)
    f.close()
    print("\nFile saved as missing_words.json in current working directory")


if __name__ == '__main__':
    main()
