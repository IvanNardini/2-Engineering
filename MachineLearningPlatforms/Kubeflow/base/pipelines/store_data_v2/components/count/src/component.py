#!/usr/bin/env python3

# component.py
# component is a simple component wrapper of data preparation step
# Notice: In this case I assume to read data from Cloud Storage.
# You have both pure storage APIs or tf. gfile.
# For portability, I prefer tf.gfile because you can debug your model
# locally and train it on cloud without changing a single line.

from tensorflow.io import gfile
from count import run_count_word
import pickle
import logging
import argparse

# Helpers --------------------------------------------------------------------------------------------------------------
def load_file(file_path: str) -> str:
    logging.info(f"Loading {file_path} file...")
    with gfile.GFile(name=file_path, mode='r') as file:
        text = file.read().replace("\n", " ")
    file.close()
    return text

# Main -----------------------------------------------------------------------------------------------------------------
def run_component(pkl_path:str, word:str):
    logging.info('Initiating Count Words component...')
    try:
        words_list = load_file(file_path=text_path)
        word_count = run_count_words(pkl_path=pkl_path, word=word)
    except RuntimeError as error:
        logging.info(error)
    else:
        logging.info('Count words component successfully completed!')
    return out_path_pkl

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Cound Words component")

    parser.add_argument('--pkl-path',
                        type=str,
                        required=True,
                        help='Path to store pickle')

    parser.add_argument('--word',
                        type=str,
                        required=True,
                        help='Word to count')

    args = parser.parse_args()
    input_pkl_path=args.pkl_path
    input_word=args.word
    run_component(pkl_path=input_pkl_path, word=input_word)