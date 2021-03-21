#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------

## General
import sys
import logging
from .helpers import fit_tf_idf, get_text_features, get_nlp_features

# FeatureEngineer ------------------------------------------------------------------------------------------------------


class FeaturesGenerator:

    def __init__(self, config):
        self.random_state = config['random_state']
        self.tf_idf_vectorizer = None

    def fit(self, data):
        tf_idf_vectorizer = fit_tf_idf(data)
        self.tf_idf_vectorizer = tf_idf_vectorizer

    def transform(self, data):
        logging.info('Initiating features engineering process...')
        try:
            logging.info('Processing text features...')
            df_text_feats = get_text_features(data)
            logging.info('Processing nlp features...')
            df_nlp_feats = get_nlp_features(df_text_feats)
            tf_idf_matrix = self.tf_idf_vectorizer.transform(df_nlp_feats)
        except RuntimeError as error:
            logging.error(error)
            sys.exit(1)
        return tf_idf_matrix



