#!/usr/bin/env python3

import kfp.components as cpt
from component.run_collect import run_collect
import datetime
import argparse

REGISTRY = "docker.io/in92"

def run_build_component(args):
    mode = args.mode
    out_components_dir = args.output_component_dir
    comp_name = f"women_clt_rev_clf_{mode}_data_collection_component.yaml"
    component = cpt.func_to_container_op(run_collect,
                                         base_image=f'{REGISTRY}/data_collect:1.0.3',
                                         output_component_file=f'{out_components_dir}/{comp_name}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run component builder")
    parser.add_argument('--mode',
                        default='cloud')
    parser.add_argument('--output-component-dir',
                        default='.')
    args = parser.parse_args()
    run_build_component(args=args)