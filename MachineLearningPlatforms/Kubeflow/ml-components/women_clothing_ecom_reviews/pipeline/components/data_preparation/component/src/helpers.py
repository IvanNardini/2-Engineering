#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
from nltk.stem import PorterStemmer


# Helpers ------------------------------------------------------------------------------------------------------------

def remove_sw(words_list):
    stop_words = stopwords.words("english")
    return [word for word in words_list if word not in stop_words]


def stemmer(words_list):
    ps = PorterStemmer()
    return [ps.stem(word) for word in words_list]

def load_data(path):
    pass

def store_data(path, filename):
    pass
