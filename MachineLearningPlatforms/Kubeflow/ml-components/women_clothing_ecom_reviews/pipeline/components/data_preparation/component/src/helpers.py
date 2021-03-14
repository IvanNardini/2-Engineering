#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------

import os
import logging
import sys
from pathlib import Path

import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import PorterStemmer

from tensorflow.io import gfile


# Helpers ------------------------------------------------------------------------------------------------------------

def remove_sw(words_list):
    stop_words = stopwords.words("english")
    return [word for word in words_list if word not in stop_words]


def stemmer(words_list):
    ps = PorterStemmer()
    return [ps.stem(word) for word in words_list]

def load_data(mode, input_data):
    logging.info(f'Loading data to {input_data}...')
    try:
        if mode == 'cloud':
            with gfile.GFile(name=input_data, mode='r') as file:
                df = pd.read_csv(file)
        else:
            df = pd.read_csv(input_data)
    except RuntimeError as error:
        logging.info(error)
        sys.exit(1)
    else:
        print(df.head(5))
    return df


def save_data(df, mode, path, filename):
    data_path = os.path.join(path, filename)
    logging.info(f'Writing {data_path} file...')
    try:
        p = Path(path)
        if not p.exists():
            os.mkdir(path)
        df.to_csv(data_path)
    except RuntimeError as error:
        logging.info(error)
        sys.exit(1)
    else:
        logging.info(f'Data successfully saved under {path}')
