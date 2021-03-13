#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------
import argparse
import logging.config
import yaml
import sys
from src.prepare import DataPreparer
from src.helpers import load_data, save_data

# Settings -------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Main -----------------------------------------------------------------------------------------------------------------
def run_collect(args):
    config = args.config
    mode = args.mode
    #TODO: Add input path param 
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
        preparer = DataPreparer(config=config)
        for df in config['interim_data']:
            data = load_data(config['interim_path'], df)
            processed_data = preparer.transform(data)
            print(processed_data.head(5))
            save_data(processed_data, config['processed_path'], df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run data collector")
    parser.add_argument('--config',
                        help='path to configuration yaml file')
    parser.add_argument('--mode',
                        help='where you run the code')
    args = parser.parse_args()
    run_collect(args)