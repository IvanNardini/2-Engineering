#!/usr/bin/env python3

import kfp.components as cpt
from component.run_collect import run_collect
import argparse

def main(args):
    out_components_dir = args.output_component_dir
    cpt.create_component_from_func(func=run_collect,
                                   output_component_file=f'{out_components_dir}/hello_kubeflow.component')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run component builder")
    parser.add_argument('--output-component-dir', default='../../../deliverables/components')
    args = parser.parse_args()
    main(args=args)