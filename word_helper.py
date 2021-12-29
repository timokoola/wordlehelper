#!/usr/local/bin/python3
import argparse
from collections import Counter
from functools import reduce
from math import log
from random import sample

parser = argparse.ArgumentParser(
    description="Help solve the Wordle puzzle. See https://www.powerlanguage.co.uk/wordle/"
)
parser.add_argument(
    "-v", "--verbosity", action="count", default=0, help="increase output verbosity"
)
parser.add_argument(
    "-d",
    "--dictionary-file",
    type=str,
    default="/usr/share/dict/words",
    help="Location of the dictionary file",
)
parser.add_argument(
    "-l",
    "--length",
    type=int,
    default=5,
    help="Length of the words used in the search. Wordle game has words with 5 letters",
)
subparsers = parser.add_subparsers(help="sub-command help", dest="subcommand")


suggest_parser = subparsers.add_parser(
    "suggest", help="Suggest me a word to start the search"
)
suggest_parser = subparsers.add_parser(
    "distribution", help="Show distribution of letters in positions"
)
suggest_parser.add_argument(
    "-l",
    "--length",
    type=int,
    default=5,
    help="Length of the words to suggest",
)

anagram_parser = subparsers.add_parser(
    "anagrams", help="Print anagrams from the word list for a word"
)
anagram_parser.add_argument(
    "word", type=str, help="Print anagrams of this word from the dictionary"
)

solution_parser = subparsers.add_parser(
    "solve", help="Try to find a correct word given the constraints"
)
solution_parser.add_argument(
    "-1", "--first", type=str, default="", help="First letter is known to be this"
)
solution_parser.add_argument(
    "-2", "--second", type=str, default="", help="Second letter is known to be this"
)
solution_parser.add_argument(
    "-3", "--third", type=str, default="", help="Third letter is known to be this"
)
solution_parser.add_argument(
    "-4", "--fourth", type=str, default="", help="Fourth letter is known to be this"
)
solution_parser.add_argument(
    "-5", "--fifth", type=str, default="", help="Fifth letter is known to be this"
)

solution_parser.add_argument(
    "-n1",
    "--not-first",
    type=str,
    default="",
    help="First letter is known not to be these letters that are still present in the word",
)
solution_parser.add_argument(
    "-n2",
    "--not-second",
    type=str,
    default="",
    help="Second letter is known not to be these letters that are still present in the word",
)
solution_parser.add_argument(
    "-n3",
    "--not-third",
    type=str,
    default="",
    help="Third letter is known not to be these letters that are still present in the word",
)
solution_parser.add_argument(
    "-n4",
    "--not-fourth",
    type=str,
    default="",
    help="Fourth letter is known not to be these letters that are still present in the word",
)
solution_parser.add_argument(
    "-n5",
    "--not-fifth",
    type=str,
    default="",
    help="Fifth letter is known not to be these letters that are still present in the word",
)

solution_parser.add_argument(
    "-n",
    "--notin",
    type=str,
    default="",
    help="These letters are known not to be in the solution",
)


def word_score(word):
    """Score words, more common the letter for position, higher the score. If same letter appear
    more than once, score is '0"""
    assert len(word) == 5
    # severely punish words that have same letter multiple times
    if len(list(set(word))) < len(word):
        return 0
    result = []
    for i, l in enumerate(word):
        result.append(distribution[i][l])

    return log(reduce(lambda x, y: x * y, result))


def normalize(word):
    """Helper function for comparing words for anagram-ness"""
    return sorted(word)


def anagrams(letters, global_word_list):
    """Generate anagrams for letters"""
    return [x for x in global_word_list if normalize(x) == normalize(letters)]


def search_words(known, not_in, global_word_list):
    """Search words that fulfill the conditions"""
    assert len(known) == 5
    result = global_word_list
    for letter in not_in:
        result = [w for w in result if letter not in w]

    if args.verbosity:
        print(f"After eliminating letters not in word we have {len(result)} candidates")

    for i, k in enumerate(known):
        for letter in k:
            if args.verbosity:
                print(f"Checkin {letter} {len(result)}")
            if letter.lower() == letter:
                result = [w for w in result if letter == w[i]]
            else:
                not_letter = letter.lower()
                result = [
                    w for w in result if not_letter != w[i] and not_letter in w
                ]
    return sorted(
        [(x, word_score(x)) for x in result], key=lambda x: x[1], reverse=True
    )


def suggest(global_word_list):
    """Suggest words that have a high score"""
    return search_words(["", "", "", "", ""], "", global_word_list)


if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.dictionary_file) as f:
        words = [w.strip().lower() for w in f.readlines()]

    k_letter_words = list(set([w for w in words if len(w) == args.length]))
    anagram_groups = list(set(["".join(sorted(w)) for w in k_letter_words]))
    letter_count = {}
    for i in range(args.length):
        letter_count[i] = "".join([x[i] for x in k_letter_words])

    distribution = {}
    for i in range(args.length):
        distribution[i] = Counter(letter_count[i])
    anagram_groups_score = sorted(
        [(x, word_score(x)) for x in anagram_groups], key=lambda x: x[1], reverse=True
    )

    if args.subcommand == "suggest":
        suggestions = suggest(k_letter_words)[:100]
        suggestion_list = [w[0] for w in sample(suggestions, 20)]

        print(", ".join(suggestion_list))
    elif args.subcommand == "anagrams":
        print(", ".join(anagrams(args.word, words)))
    elif args.subcommand == "distribution":
        print(distribution)
    else:
        assert args.length == 5
        known = ["", "", "", "", ""]
        known[0] = f"{args.first}{args.not_first.upper()}"
        known[1] = f"{args.second}{args.not_second.upper()}"
        known[2] = f"{args.third}{args.not_third.upper()}"
        known[3] = f"{args.fourth}{args.not_fourth.upper()}"
        known[4] = f"{args.fifth}{args.not_fifth.upper()}"
        results = [
            f"{x[0]} score: {x[1]}"
            for x in search_words(known, args.notin, k_letter_words)
        ]
        if args.verbosity > 2:
            print("\n".join(results))
        else:
            print("\n".join(results[:20]))
