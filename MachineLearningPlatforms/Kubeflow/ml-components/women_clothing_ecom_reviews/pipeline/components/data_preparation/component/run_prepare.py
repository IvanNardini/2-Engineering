#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------
import argparse
import logging.config
from src.prepare import DataPreparer
from src.helpers import load_data, save_data

# Settings -------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Main -----------------------------------------------------------------------------------------------------------------
def run_collect(args):
    config = args.config
    mode = args.mode
    preparer = DataPreparer(config=config, mode=mode)

    for filename in config['interim_data']:
        data = load_data(config['interim_path'], filename)
        preparer.transform(data=data)
        save_data(data, config['processed_path'], filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run data collector")
    parser.add_argument('--config',
                        help='path to configuration yaml file')
    parser.add_argument('--mode',
                        help='where you run the code')
    args = parser.parse_args()
    run_collect(args)