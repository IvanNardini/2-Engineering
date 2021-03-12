#!/usr/bin/env python3

# build_pipeline.py
# build_pipeline is a module to compile the pipeline

import kfp
import kfp.compiler as cmp
import kfp.dsl as dsl
from kfp.gcp import use_gcp_secret

import datetime
from uri import URI
import os
import argparse

# Variables ------------------------------------------------------------------------------------------------------------
GCS_COMPONENT_PATH = 'components/config_init/component.yaml'
REGISTRY = "docker.io/in92"

# Components -----------------------------------------------------------------------------------------------------------

gcs_download_component = kfp.components.load_component_from_file(filename=GCS_COMPONENT_PATH)

@kfp.dsl.component
def data_collection(config, mode):
    return kfp.dsl.ContainerOp(
        name='Collect Data',
        image=f'{REGISTRY}/data_collect:1.0.0',
        arguments=['--config', config,
                   '--mode', mode]
    ).apply(use_gcp_secret('user-gcp-sa'))

@kfp.dsl.component
def data_preparation(config, mode):
    # TODO add data prep function
    return kfp.dsl.ContainerOp(
        name='Prepare Data',
        image=f'{REGISTRY}/data_prepare:1.0.0',
        arguments=['--config', config,
                   '--mode', mode]
    ).apply(use_gcp_secret('user-gcp-sa'))


# run_build_pipeline ---------------------------------------------------------------------------------------------------
def run_build_pipeline(args):
    out_pipe_dir = args.out_pipe_dir
    env = args.mode
    pipe_name = f"women_clt_rev_clf_pipe_{env}_{datetime.datetime.now().strftime('%y%m%d-%H%M%S')}.yaml"

    if env == 'cloud':
        @dsl.pipeline(name="Women Clothing Reviews Classification ML Pipeline",
                      description="An example of Machine Learning Pipeline")
        def build_pipeline(config: URI, mode: dsl.PipelineParam):
            # TODO: Check for one to one portability with cloud
            # General setting
            out_vol_op = dsl.VolumeOp(name='pipeline-volume',
                                      resource_name='data',
                                      size="3Gi",
                                      modes=dsl.VOLUME_MODE_RWO)
            step_0 = gcs_download_component(config)
            step_0.add_pvolumes({'/pipe-data': out_vol_op.volume})
            step_1 = data_collection(config=step_0.output, mode=mode)
            step_1.add_pvolumes({'/pipe-data': out_vol_op.volume})
            step_1.after(step_0)
            step_2 = data_preparation(config=step_0.output, mode=mode)
            step_2.after(step_1)

    pipeline_complier = cmp.Compiler()
    pipeline_complier.compile(pipeline_func=build_pipeline,
                              package_path=os.path.join(out_pipe_dir, pipe_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run pipeline builder")
    parser.add_argument('--out-pipe-dir', default='../deliverables/pipeline')
    parser.add_argument('--mode', default='cloud')
    args = parser.parse_args()
    run_build_pipeline(args=args)
