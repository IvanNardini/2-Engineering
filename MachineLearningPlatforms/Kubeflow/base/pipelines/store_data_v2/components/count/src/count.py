#!/usr/bin/env python3

# count.py
# count is a simple example of processing

import pickle
import argparse
import logging

# Settings
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Function -------------------------------------------------------------------------------------------------------------

def count_word(word_list: list, word: str) -> int:
    return word_list.count(word)


# Main -----------------------------------------------------------------------------------------------------------------
def run_count_word(pkl_path:str, word:str):
    logging.info("Count words processing starts...")
    try:
        logging.info("Counting...")
        n_word = count_word(word_list=token_text, word=word)
    except RuntimeError as error:
        logging.info(error)
    else:
        logging.info("Count words processing successfully completed!")
    return n_word


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Cound Words processing")

    parser.add_argument('--pkl-path',
                        required=True,
                        help='The path to load pkl file with processed data')

    parser.add_argument('--word',
                        required=True,
                        help='The word to count occurrences')

    args = parser.parse_args()
    input_pkl_path = args.pkl_path
    input_word = args.word
    run_count_word(pkl_path=input_pkl_path, word=input_word)
