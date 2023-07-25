# 1. Training Corpus
# 2. Syllable Count Corpus
# 3. Missing Words dictionary

# Overlay the syllable count corpus with the training corpus --> words that appear in the training corpus
# but NOT the syllable count corpus get added to the MISSING WORDS DICTIONARY
# Write a program that uses the syllable count corpus and the MISSING WORDS DICTIONARY to determine the number of syllables
# of every word in the TRAINING corpus

import sys
from string import punctuation
import pprint
import json
from nltk.corpus import cmudict

cmudict = cmudict.dict()

def main():
    haiku = load_haiku('train.txt')
    exceptions = cmudict_missing(haiku)
    build_dict = input("\n Build exceptions dictionary (y/n)\n")
    if build_dict.lower() == 'n':
        sys.exit()

    else:
        missing_words_dict = make_exceptions_dict(exceptions)
        save_exceptions(missing_words_dict)


def load_haiku(filename):
    haiku = set(filename.read().replace('-', '').split())
    return haiku

def cmudict_missing(word_set):
    exceptions = set()
    for word in word_set:
        word = word.lower().strip(punctuation)
        if word.endswith("s") or word.endswith("'s"):
            word = word[:-2]
        if word not in cmudict:
            exceptions.add(word)
        print("\nexceptions:")
        print(*exceptions, sep='\n')
        print("\nNumber of unique words in haiku corpus = {}".format(len(word_set)))
        membership = (1-(len(exceptions) / len(word_set))) * 100
        print("cmudict membership = {:.1f}{}".format(membership, '%'))
        return exceptions

def make_exceptions_dict(exceptions_set):
    """For each word in the exception_set (the set that we created by overlaying the cmudict and the haiku training corpus)
    make a dictionary with the word as the key and the number of syllables as the value (user supplied), and give the option
    to add new words"""
    missing_words = {}
    print("Input # of syllables in word. Mistakes can be corrected at the end. \n")

    # Account for all the missing words in the haiku training corpus
    for word in exceptions_set:
        while True:
            num_sylls = input("Enter the number of syllables in {}:".format(word))
            if num_sylls.isdigit():
                break
            else:
                print(" Not a valid answer!", file=sys.stderr)
            missing_words[word]=int(num_sylls)
            print("\n")
            pprint.pprint(missing_words, width=1)
        # Give the option to add new words after the above loop has concluded
        print("\nMake Changes to Dictionary Before Saving?")
        print(""" 0 - Exit & Save 
                      1 - Add a Word or Change a Syllable Count
                      2 - Remove a Word 
                      """)

        while True:
            choice = input("\nEnter choice")
            if choice == "0":
                break
            elif choice == "1":
                word = input("\nWord to add or change:")
                missing_words[word] = int(input("Enter number syllables in {}:".format(word)))
            elif choice == '2':
                word = input("\nEnter word to delete: ")
                missing_words.pop(word, None)



def save_exceptions(missing_words):
    """Save the missing_words dictionary to a file"""
    json_string = json.dumps(missing_words)
    f = open('missing_words.json', 'w')
    f.write(json_string)
    f.close()
    print("\nFile saved as missing_words.json in current working directory")

if __name__ == '__main__':
    main()
