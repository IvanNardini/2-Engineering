#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------
import argparse
import logging.config
from src.collect import DataCollector

# Settings -------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Variables ------------------------------------------------------------------------------------------------------------
CONFIGFILE = './config.yaml'

# Main -----------------------------------------------------------------------------------------------------------------
def run_collect(args):
    config_file = args.config_file
    collector = DataCollector(config_file=config_file)
    raw_df = collector.extract()
    x_train, x_test, x_val, y_train, y_test, y_val = collector.transform(raw_df)
    collector.load(x_train, x_test, x_val,
                   y_train, y_test, y_val)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run data collector")
    parser.add_argument('--config-file',
                        default=CONFIGFILE,
                        help='path to configuration yaml file')
    args = parser.parse_args()
    run_collect(args)