#!/usr/bin/env python3

# HelloKubeflow.py
# HelloKubeflow is a hello world python module for testing Kubeflow
# Python lightweight components
#
# Steps:
# 1 - Create a simple python function
# 2 - (Optional) Create a container image for the component
# 3 - Convert your Python function into a pipeline component
# 4 - Write a pipeline function using the Kubeflow Pipelines DSL
# 5 - Compile the pipeline to generate a compressed YAML definition of the pipeline

import os
from sys import argv

import kfp
import kfp.components as cpt
import kfp.compiler as cmp
import kfp.dsl as dsl


# Functions ------------------------------------------------------------------------------------------------------------

# Create a simple python function
def hello_kubeflow(name: str) -> str:
    msg = f'{name} met Kubeflow at Valentines day! <3'
    return msg


# Main -----------------------------------------------------------------------------------------------------------------
def main():
    OUT_COMPONENTS_DIR = argv[1]
    OUT_PIPELINE_DIR = argv[2]

    # Convert your Python function into a pipeline component
    hello_component = cpt.create_component_from_func(func=hello_kubeflow,
                                                     output_component_file=f'{OUT_COMPONENTS_DIR}/hello_kubeflow_component.yaml')

    # Write a pipeline function using the Kubeflow Pipelines DSL
    @dsl.pipeline(name='Hello Kubeflow Pipeline',
                  description='A Hello Kubeflow pipeline')
    def hello_kubeflow_pipeline(
            name='Ivan'):
        task = hello_kubeflow(name)

    # Compile the pipeline to generate a compressed YAML definition of the pipeline
    cmp.Compiler().compile(pipeline_func=hello_kubeflow_pipeline,
                         package_path=OUT_PIPELINE_DIR)


if __name__ == "__main__":
    main()
