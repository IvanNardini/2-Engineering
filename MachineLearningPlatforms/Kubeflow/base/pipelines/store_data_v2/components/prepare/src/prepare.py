#!/usr/bin/env python3

# prepare.py
# prepare is a simple example of data preparation component

import nltk
import logging
import argparse

# Settings
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Functions ------------------------------------------------------------------------------------------------------------
def prepare_data(text: str) -> list:
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    plain_text = tokenizer.tokenize(text=text)
    return plain_text

# Main -----------------------------------------------------------------------------------------------------------------
def run_prepare(args):
    logging.info('Data preparation process starts...')
    try:
        token_text = prepare_data(text=text)
    except RuntimeError as error:
        logging.info(error)
    else:
        logging.info('Data preparation process successfully completed!')
    return token_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Data Preprocess")
    parser.add_argument('--text',
                        type=str,
                        required=True,
                        help='Text to process')
    args = parser.parse_args()
    run_prepare(args=args)
