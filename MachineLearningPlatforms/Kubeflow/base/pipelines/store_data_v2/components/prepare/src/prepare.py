#!/usr/bin/env python3

# prepare.py
# prepare is a simple example of data preparation component

import nltk
import argparse


# Functions ------------------------------------------------------------------------------------------------------------
def prepare_data(text: str) -> list:
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    plain_text = tokenizer.tokenize(text=text)
    return plain_text


# Main -----------------------------------------------------------------------------------------------------------------
def run_prepare(text: str):
    token_text = prepare_data(text=text)
    return token_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Data Preprocess")
    parser.add_argument('--text',
                        type=str,
                        required=True,
                        help='Text to process')
    args = parser.parse_args()
    run_prepare(args=args)
