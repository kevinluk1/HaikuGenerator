import sys
import logging
import random
from collections import defaultdict
from count_syllables import count_syllables
from typing import *

logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def load_training_file(file) -> str:
    with open(file) as f:
        raw_haiku = f.read()
        return raw_haiku


def prep_training(raw_haiku: str) -> List:
    corpus = raw_haiku.replace('\n', ' ').split()
    return corpus


def map_word_to_word(corpus: List) -> Dict[str, List]:  # one word markov model
    limit = len(corpus) - 1  # off by 1 indexing
    dict1_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            key = word
            suffix = corpus[index + 1]
            dict1_to_1[key].append(suffix)

    return dict1_to_1


def map_2_words_to_word(corpus: List) -> Dict:  # two word markov model
    limit = len(corpus) - 2
    dict2_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            key = word + ' ' + corpus[index + 1]  # two word key
            suffix = corpus[index + 2]
            dict2_to_1[key].append(suffix)

    return dict2_to_1


def seed_word(corpus: List) -> Tuple[str, int]:
    word = random.choice(corpus)
    num_sylls = count_syllables(word)
    if num_sylls <= 4:
        return (word, num_sylls)
    else:
        return seed_word(corpus)



def word_after_single(prefix, markov1, current_sylls, target_sylls) -> List:
    accepted_words = []
    suffixes = markov1.get(prefix)
    if suffixes is not None:
        for candidate in suffixes:
            num_sylls = count_syllables(candidate)
            if current_sylls + num_sylls <= target_sylls:
                accepted_words.append(candidate)

    logging.debug(f'accepted words after "{prefix}" = {set(accepted_words)}\n')
    return accepted_words


def word_after_double(prefix, markov2, current_sylls, target_sylls) -> List:
    accepted_words = []
    suffixes = markov2.get(prefix)
    if suffixes is not None:
        for candidate in suffixes:
            num_sylls = count_syllables(candidate)
            if current_sylls + num_sylls <= target_sylls:
                accepted_words.append(candidate)

    logging.debug(f'accepted words after "{prefix}" = {set(accepted_words)}\n')
    return accepted_words


def haiku_line(markov1: Dict, markov2: Dict, corpus: List[str], end_prev_line: List, target_sylls: int) -> Tuple[List[str], List[str]]:
    line = '2 or 3'
    line_sylls = 0
    current_line = []
    if len(end_prev_line) == 0:  # on line 1
        line = '1'
        word, num_sylls = seed_word(corpus)
        current_line.append(word)  # first word
        line_sylls += num_sylls
        word_choices: List = word_after_single(word, markov1, line_sylls, target_sylls)

        while len(word_choices) == 0:   # ghost prefix, not added to the line, just used to re-access markov model
            backup_prefix = random.choice(corpus)
            logging.debug(f'new random prefix = "{backup_prefix}"')
            word_choices: List = word_after_single(backup_prefix, markov1, line_sylls, target_sylls) # pass the ghost prefix

        word: str = random.choice(word_choices)  # second word
        num_sylls: int = count_syllables(word)
        logging.debug(f'"word and syllables = {word},{num_sylls}"')
        line_sylls += num_sylls
        current_line.append(word)

        if line_sylls == target_sylls:  # in the case that the first two words (as opposed to first 3 or 4) are equal to 5 syllables
            end_prev_line.extend(current_line[-2:])  # prep to use 2nd order markov chain
            return current_line, end_prev_line  # pass the end of the prev line to use as markov chain key

    else:
        current_line.extend(end_prev_line)

    while True:
        logging.debug(f'line={line}')
        prefix = current_line[-2] + ' ' + current_line[-1]
        word_choices: List = word_after_double(prefix, markov2, line_sylls, target_sylls)

        while len(word_choices) == 0:  # ghost seeding
            index = random.randint(0, len(corpus) - 2)
            prefix = corpus[index] + ' ' + corpus[index+1]
            logging.debug(f'new random prefix = {prefix}')
            word_choices = word_after_double(prefix, markov2, line_sylls, target_sylls)

        word = random.choice(word_choices)
        num_sylls = count_syllables(word)
        logging.debug(f'word and syllables = {word, num_sylls}')

        if line_sylls + num_sylls > target_sylls:  # choose another word from word_choices
            continue
        elif line_sylls + num_sylls < target_sylls:
            current_line.append(word)
            line_sylls += num_sylls
            continue
        elif line_sylls + num_sylls == target_sylls:
            line_sylls += num_sylls
            current_line.append(word)
            break

    end_prev_line = []
    end_prev_line.extend(current_line[-2:])

    if line == '1':
        completed_line = current_line[:]
    else:
        completed_line = current_line[2:]

    return (completed_line, end_prev_line)



def main():

    raw_haiku = load_training_file("train.txt")
    corpus = prep_training(raw_haiku)
    markov_1 = map_word_to_word(corpus)
    markov_2 = map_2_words_to_word(corpus)
    final = []

    choice = None
    while choice != "0":
        print(
            """
            Japanese Haiku Generator
            0 - Quit
            1 - Generate a Haiku
            2 - Regenerate Line 2
            3 - Regenerate Line 3
            """
        )

        choice = input("Choice: ")
        print()

        if choice == "0":
            print("bye!")
            sys.exit()

        elif choice == "1":
            final:List[List[str]] = []
            end_prev_line0 = []
            first_line, end_prev_line1 = haiku_line(markov_1, markov_2, corpus, end_prev_line0, 5)
            final.append(first_line)
            line2, end_prev_line2 = haiku_line(markov_1, markov_2, corpus, end_prev_line1, 7)
            final.append(line2)
            line3, end_prev_line3 = haiku_line(markov_1, markov_2, corpus, end_prev_line2, 5)
            final.append(line3)

        elif choice == "2":
            if not final:
                print("Please generate a full haiku first")
                continue
            else:
                line2, end_prev_line2 = haiku_line(markov_1, markov_2, corpus, end_prev_line1, 7)
                final[1] = line2

        elif choice == "3":
            if not final:
                print("Please generate a full haiku first")
                continue
            else:
                line3, end_prev_line3 = haiku_line(markov_1, markov_2, corpus, end_prev_line2, 5)
                final[2] = line3

        else:
            print("Not a valid choice")
            continue

    # display results


        print("Your generated haiku:")
        print()
        print(f'List form: {final}')
        for g in range(3):
            final[g][0] = final[g][0].capitalize()
        print(f"Final: \n\n {' '.join(final[0])} \n {' '.join(final[1])} \n {' '.join(final[2])}")


if __name__ == '__main__':
    main()


