#!/usr/bin/env python3

# build_pipeline.py
# build_pipeline is a module to compile the pipeline

import kfp
import kfp.compiler as cmp
import kfp.dsl as dsl
from kfp.gcp import use_gcp_secret

import datetime
from uri import URI
from typing import NamedTuple
import os
import argparse

# Variables ------------------------------------------------------------------------------------------------------------
GCS_COMPONENT_PATH = 'components/config_init/component.yaml'
DATA_COLLECT_COMP_PATH = 'components/data_collection/component/women_clt_rev_clf_cloud_data_collection_component.yaml'
REGISTRY = "docker.io/in92"

# Components -----------------------------------------------------------------------------------------------------------

gcs_download_component = kfp.components.load_component_from_file(filename=GCS_COMPONENT_PATH)
data_collection_component = kfp.components.load_component_from_file(filename=DATA_COLLECT_COMP_PATH)


# @kfp.dsl.component
# def data_collection(mode,bucket,config):
#     return kfp.dsl.ContainerOp(
#         name='Collect Data',
#         image=f'{REGISTRY}/data_collect:1.0.3',
#         arguments=[
#             '--mode', mode,
#             '--bucket', bucket,
#             '--config', config
#         ],
#     ).apply(use_gcp_secret('user-gcp-sa'))
#
#
# @kfp.dsl.component
# def data_preparation(mode, bucket, config,
#                      train_path, test_path, val_path):
#     return kfp.dsl.ContainerOp(
#         name='Prepare Data',
#         image=f'{REGISTRY}/data_prepare:1.0.0',
#         arguments=[
#             '--mode', mode,
#             '--bucket', bucket,
#             '--config', config,
#             '--train-path', train_path,
#             '--test-path', test_path,
#             '--val-path', val_path
#         ],
#     ).apply(use_gcp_secret('user-gcp-sa'))


# run_build_pipeline ---------------------------------------------------------------------------------------------------
def run_build_pipeline(args):
    out_pipe_dir = args.out_pipe_dir
    mode = args.mode

    pipe_name = f"women_clt_rev_clf_pipe_{mode}_{datetime.datetime.now().strftime('%y%m%d-%H%M%S')}.yaml"

    # TODO: Check for one to one portability with cloud, add on prem in case
    if mode == 'cloud':
        @dsl.pipeline(name="Women Clothing Reviews Classification ML Pipeline",
                      description="An example of Machine Learning Pipeline")
        def build_pipeline(mode, bucket, config_file):
            config_url = f'{bucket}/{config_file}'
            step_0 = gcs_download_component(config_url)
            step_1 = data_collection_component(mode=mode,
                                               bucket=bucket,
                                               config=step_0.output).apply(use_gcp_secret('user-gcp-sa'))
            step_1.after(step_0)
            # step_2 = data_preparation(mode=mode, bucket=bucket, config=step_0.output,
            #                           train_path=step_1.outputs['train'],
            #                           test_path=step_1.outputs['test'],
            #                           val_path=step_1.outputs['val'])
            # step_2.after(step_1)

    pipeline_compiler = cmp.Compiler()
    pipeline_compiler.compile(pipeline_func=build_pipeline,
                              package_path=os.path.join(out_pipe_dir, pipe_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run pipeline builder")
    parser.add_argument('--out-pipe-dir',
                        default='.')
    parser.add_argument('--mode',
                        default='cloud')
    args = parser.parse_args()
    run_build_pipeline(args=args)
