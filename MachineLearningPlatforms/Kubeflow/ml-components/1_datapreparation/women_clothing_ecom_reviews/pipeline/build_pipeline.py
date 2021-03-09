#!/usr/bin/env python3

# build_pipeline.py
# build_pipeline is a module to compile the pipeline

import k

import kfp
import kfp.components as cpt
import kfp.compiler as cmp
import kfp.dsl as dsl
from kfp.gcp import use_gcp_secret
import argparse