#!/usr/bin/env python3

#
# Description
#

# Libraries ------------------------------------------------------------------------------------------------------------
import argparse
import logging.config
import yaml
import sys
import os
from src.prepare import DataPreparer
from src.helpers import load_data, save_data

# Settings -------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Main -----------------------------------------------------------------------------------------------------------------
def run_collect(args):
    mode = args.mode
    config = args.config
    train_path = args.train_path
    test_path = args.test_path
    val_path = args.val_path

    #TODO: Add input path param 
    try:
        # TODO: Check for one to one portability with cloud
        if mode == 'cloud':
            config = yaml.safe_load(config)
        else:
            stream = open(config, 'r')
            config = yaml.load(stream=stream, Loader=yaml.FullLoader)

        preparer = DataPreparer(config=config)

        if mode == 'cloud':
            input_paths_gcs = [train_path, test_path, val_path]
            output_paths_gcs = []
            for input_path, filename in zip(input_paths_gcs, config['processed_data']):
                data = load_data(mode, input_path)
                processed_data = preparer.transform(data)
                # TODO: Add metadata in the pipeline
                print(processed_data.head(5))
                out_path = save_data(processed_data, mode, config['processed_path'], filename)
            output_paths_gcs.append(out_path)
            return tuple(output_paths_gcs)

        else:
            for input_filename, out_filename in zip(config['interim_data'], config['processed_data']):
                data_path = os.path.join(config['interim_path'], input_filename)
                data = load_data(mode, data_path)
                processed_data = preparer.transform(data)
                print(processed_data.head(5))
                save_data(processed_data, mode, config['processed_path'], out_filename)
    except RuntimeError as error:
        logging.info(error)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run data collector")
    parser.add_argument('--mode',
                        required=False,
                        default='local',
                        help='where you run the pipeline')
    parser.add_argument('--config',
                        default='config.yaml',
                        help='path to configuration yaml file')
    parser.add_argument('--train-path',
                        required=False,
                        help='if cloud, the path to train data')
    parser.add_argument('--test-path',
                        required=False,
                        help='if cloud, the path to test data')
    parser.add_argument('--val-path',
                        required=False,
                        help='if cloud, the path to val data')

    args = parser.parse_args()
    run_collect(args)