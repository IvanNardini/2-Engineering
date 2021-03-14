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
    if mode == 'cloud':
        with gfile.GFile(name=input_data, mode='r') as file:
            df = pd.read_csv(file)
    else:
        df = pd.read_csv(input_data)
    logging.info(f'{input_data} successfully loaded!')
    return df

def save_data(df, mode, path, out_data):
    out_csv = f'{path}/{out_data}'
    logging.info(f'Writing {out_csv} file...')
    if mode == 'cloud':
        with gfile.GFile(name=out_csv, mode='w') as file:
            df.to_csv(file, index=False)
        return out_csv
    else:
        p = Path(path)
        if not p.exists():
            os.mkdir(path)
        df.to_csv(out_csv)
    logging.info(f'{out_csv} successfully loaded!')
