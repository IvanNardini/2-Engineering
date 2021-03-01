#!/usr/bin/env python3

# prepare.py
# prepare is the prepare module of a better version of store_data
# Improvements:
# - Wrapper python and annotations to simplify the pipeline
# - file_outputs option to avoid .add_pvolume repetitions

import pickle
import nltk
import logging
import os
import argparse

# Settings
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Helpers --------------------------------------------------------------------------------------------------------------
def load_text(file_path: str) -> str:
    with open(file=file_path, mode='r') as file:
        text = file.read().replace("\n", " ")
    file.close()
    return text

def store_data(word_list: list, out_path_pkl: str):
    with open(out_path_pkl, 'wb') as file:
        pickle.dump(word_list, file)

# Functions ------------------------------------------------------------------------------------------------------------
def prepare_data(text: str) -> list:
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    plain_text = tokenizer.tokenize(text=text)
    return plain_text

# Main -------------------------------------------------------------------------------------------------------------
def main(args):

    text_path = args.text_path
    out_path_pkl = args.path_pkl
    text = load_text(file_path=text_path)
    token_text = prepare_data(text=text)
    store_data(word_list=token_text, out_path_pkl=out_path_pkl)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline builder")
    parser.add_argument('--text-path', help='The path of text to process')
    parser.add_argument('--path-pkl', help='The path to store pkl file with processed data')
    args = parser.parse_args()
    main(args=args)
