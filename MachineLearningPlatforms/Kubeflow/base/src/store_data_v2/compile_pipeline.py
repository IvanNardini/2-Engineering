#!/usr/bin/env python3

# pipeline.py
# pipeline is an example of how creating components from existing application code
# Improvements:
# - Wrapper python and annotations to simplify the pipeline
# - file_outputs option to avoid .add_pvolume repetitions
# Steps:
# Assuming that the Docker container image of the existing app is uploaded to a registry:
# 1 - Write a component function using the Kubeflow Pipelines DSL
# 2 - Write a pipeline function using the Kubeflow Pipelines DSL
# 3 - Compile the pipeline to generate a compressed YAML definition of the pipeline

import kfp
import kfp.components as cpt
import kfp.compiler as cmp
import kfp.dsl as dsl
import argparse

# Variables ------------------------------------------------------------------------------------------------------------
REGISTRY = "docker.io/in92"

# Components -----------------------------------------------------------------------------------------------------------



@kfp.dsl.component
def prepare_component(text_path: dsl.PipelineParam, out_path_pkl: dsl.PipelineParam):
    return kfp.dsl.ContainerOp(
        name='Prepare data component',
        image=f'{REGISTRY}/kf_prepare:1.0.0',
        arguments=['--text-path', text_path,
                   '--path-pkl', out_path_pkl]
    )


@kfp.dsl.component
def count_component(input_path_pkl: dsl.PipelineParam, word: str):
    return kfp.dsl.ContainerOp(
        name='Count word component',
        image=f'{REGISTRY}/kf_count_word:1.0.0',
        arguments=['--path-pkl', input_path_pkl,
                   '--word', word]
    )


# Main
def main(args):
    output_pipeline_dir = args.output_pipeline_dir

    @dsl.pipeline(name="Store data pipeline",
                  description="A pipeline to test volume mounting")
    def build_pipeline(text_bucket_path: dsl.PipelineParam, pkl_volume_path: dsl.PipelineParam, word="Kubeflow"):
        step_1 = prepare_component(text_path=text_bucket_path, out_path_pkl=pkl_volume_path)
        step_2 = count_component(input_path_pkl=pkl_volume_path, word=word)
        step_2.after(step_1)

    pipeline_compiler = cmp.Compiler()
    pipeline_compiler.compile(pipeline_func=build_pipeline,
                              package_path=f'{output_pipeline_dir}/store_data_pipeline_v2.zip')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run pipeline builder")
    parser.add_argument('--output-pipeline-dir', default='../../out/pipelines')
    args = parser.parse_args()
    main(args=args)
