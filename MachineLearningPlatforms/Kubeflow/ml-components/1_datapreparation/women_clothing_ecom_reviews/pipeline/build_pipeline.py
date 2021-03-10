#!/usr/bin/env python3

# build_pipeline.py
# build_pipeline is a module to compile the pipeline

import kfp
import kfp.compiler as cmp
import kfp.dsl as dsl
from kfp.gcp import use_gcp_secret

import datetime
import os
import argparse

# Variables ------------------------------------------------------------------------------------------------------------
REGISTRY = "docker.io/in92"

# Components -----------------------------------------------------------------------------------------------------------
@kfp.dsl.component
def data_collection(config_file: dsl.PipelineParam):
    return kfp.dsl.ContainerOp(
        name='Collect Data',
        image=f'{REGISTRY}/data_collect:1.0.0',
        arguments=['--config-file', config_file]
    ).apply(use_gcp_secret('user-gcp-sa'))

# run_build_pipeline ---------------------------------------------------------------------------------------------------
def run_build_pipeline(args):
    out_pipe_dir = args.out_pipe_dir
    pipe_name = f"women_clothing_rev_classification_pipeline_{datetime.datetime.now().strftime('%y%m%d-%H%M%S')}.yaml"

    @dsl.pipeline(name="Women Clothing Reviews Classification ML Pipeline",
                  description="An example of Machine Learning Pipeline")
    def build_pipeline(config_file: dsl.PipelineParam):
        step_1 = data_collection(config_file=config_file)

    pipeline_complier = cmp.Compiler()
    pipeline_complier.compile(pipeline_func=build_pipeline,
                              package_path=os.path.join(out_pipe_dir, pipe_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run pipeline builder")
    parser.add_argument('--out-pipe-dir', default='.')
    args = parser.parse_args()
    run_build_pipeline(args=args)
