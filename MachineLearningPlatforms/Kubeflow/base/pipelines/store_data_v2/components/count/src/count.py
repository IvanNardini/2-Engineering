#!/usr/bin/env python3

# count.py
# count is the count module of a better version of store_data
# Improvements:
# - Wrapper python and annotations to simplify the pipeline
# - file_outputs option to avoid .add_pvolume repetitions

import pickle
import argparse
import logging

# Settings
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Helpers --------------------------------------------------------------------------------------------------------------

def load_data(input_path_pkl: str) -> list:
    with open(input_path_pkl, 'rb') as wl:
        word_list = pickle.load(wl)
    return word_list


# Functions ------------------------------------------------------------------------------------------------------------

def count_word(word_list: list, word: str) -> int:
    return word_list.count(word)


# Main -------------------------------------------------------------------------------------------------------------
def main(args):
    input_path_pkl = args.path_pkl
    word = args.word
    token_text = load_data(input_path_pkl=input_path_pkl)
    n_word = count_word(word_list=token_text, word=word)
    return n_word


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline builder")
    parser.add_argument('--path-pkl', help='The path to load pkl file with processed data')
    parser.add_argument('--word', help='The word to count occurrences')
    args = parser.parse_args()
    main(args=args)
