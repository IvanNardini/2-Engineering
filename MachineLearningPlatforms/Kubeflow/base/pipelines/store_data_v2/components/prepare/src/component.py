#!/usr/bin/env python3

# component.py
# component is a simple component wrapper of data preparation step
# Notice: In this case I assume to read data from Cloud Storage.
# You have both pure storage APIs or tf. gfile.
# For portability, I prefer tf.gfile because you can debug your model
# locally and train it on cloud without changing a single line.

from tensorflow import gfile
from prepare import run_prepare
import pickle
import logging

# Settings
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Helpers --------------------------------------------------------------------------------------------------------------
def load_text(file_path: str) -> str:
    with gfile.Open(file=file_path, mode='r') as file:
        text = file.read().replace("\n", " ")
    file.close()
    return text

def store_data(word_list: list, out_path_pkl: str):
    with gfile.Open(out_path_pkl, 'w') as file:
        pickle.dump(word_list, file)

# Main -----------------------------------------------------------------------------------------------------------------
def run_component(args):
    logging.info('Initiating Data Preparation component...')
    text_path = args.text_path
    out_path_pkl = args.path_pkl
    try:
        text = load_text(file_path=text_path)
        token_text = run_prepare(text)
        store_data(word_list=token_text,
               out_path_pkl=out_path_pkl)
    except RuntimeError as error:
        logging.info(error)
    else:
        logging.info('Data Preparation component successfully completed!')
    return out_path_pkl
