#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------
import argparse
import logging.config
import yaml
import sys
from src.collect import DataCollector
from collections import namedtuple

# Settings -------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Main -----------------------------------------------------------------------------------------------------------------
def run_collect(args):
    mode = args.mode
    bucket = args.bucket
    config = args.config

    logging.info('Initializing pipeline configuration...')
    try:
        # TODO: Check for one to one portability with cloud
        if mode == 'cloud':
            config = yaml.safe_load(config)
        else:
            stream = open(config, 'r')
            config = yaml.load(stream=stream, Loader=yaml.FullLoader)
    except RuntimeError as error:
        logging.info(error)
        sys.exit(1)
    else:
        collector = DataCollector(config=config)
        raw_df = collector.extract()
        # TODO: Add metadata in the pipeline
        print(raw_df.head(5))
        x_train, x_test, x_val, y_train, y_test, y_val = collector.transform(raw_df)
        out_paths_tuple = collector.load(x_train, x_test, x_val,
                       y_train, y_test, y_val, mode=mode, bucket=bucket)
        out_paths = namedtuple('output_paths', ['train', 'test', 'val'])
        return out_paths(out_paths_tuple)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run data collector")
    parser.add_argument('--config',
                        help='path to configuration yaml file')
    parser.add_argument('--mode',
                        required=False,
                        default='local',
                        help='where you run the pipeline')
    parser.add_argument('--bucket',
                        required=False,
                        default=None,
                        help='if cloud, the bucket to stage output')
    args = parser.parse_args()
    run_collect(args)