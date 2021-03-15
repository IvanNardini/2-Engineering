#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------
import argparse
import logging.config
import yaml
from collections import namedtuple
from typing import NamedTuple
import sys
from src.collect import DataCollector

# Settings -------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


# Main -----------------------------------------------------------------------------------------------------------------
def run_collect(mode: str,
                bucket: str,
                config: str) -> NamedTuple('output_paths', [('train', str), ('test', str), ('val', str)]):
    logging.info('Initializing pipeline configuration...')
    try:
        # TODO: Check for one to one portability with cloud
        if mode == 'cloud':
            config = yaml.safe_load(config)
        else:
            stream = open(config, 'r')
            config = yaml.load(stream=stream, Loader=yaml.FullLoader)

        collector = DataCollector(config=config)
        raw_df = collector.extract()
        # TODO: Add metadata in the pipeline
        print(raw_df.head(5))
        x_train, x_test, x_val, y_train, y_test, y_val = collector.transform(raw_df)

        if mode == 'cloud':
            (train_path_gcs, test_path_gcs, val_path_gcs) = collector.load(x_train, x_test, x_val,
                                                                           y_train, y_test, y_val, mode=mode,
                                                                           bucket=bucket)
            out_gcs = namedtuple('output_paths', ['train', 'test', 'val'])
            return out_gcs(train_path_gcs, test_path_gcs, val_path_gcs)
        else:
            (train_path, test_path, val_path) = collector.load(x_train, x_test, x_val,
                                                               y_train, y_test, y_val, mode=mode, bucket=bucket)
            out_path = namedtuple('output_paths', ['train', 'test', 'val'])
            return out_path(train_path, test_path, val_path)
    except RuntimeError as error:
        logging.info(error)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run data collector")
    parser.add_argument('--mode',
                        required=False,
                        default='local',
                        help='where you run the pipeline')
    parser.add_argument('--bucket',
                        required=False,
                        default=None,
                        help='if cloud, the bucket to stage output')
    parser.add_argument('--config',
                        default='config.yaml',
                        help='path to configuration yaml file')
    args = parser.parse_args()
    MODE = args.mode
    BUCKET = args.bucket
    CONFIG = args.config
    run_collect(mode=MODE, bucket=BUCKET, config=CONFIG)
