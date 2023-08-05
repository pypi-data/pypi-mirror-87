"""
    CLEANUP SCRIPT (TRAINING)

    any tasks to run when shutting down the container. Such as uploading data or artifacts.
"""
import logging
import argparse
import sys;sys.path.insert(1, ".")  # Do not remove this
from src.env import TrainingContainer

from src.container.training.startup import logger

if __name__ == '__main__':
    PARSER= argparse.ArgumentParser()
    ## User set params which link to Sagemaker params
    PARSER.add_argument('--env', type=str,
                        default='dev',
                        help='Run setup according to development environment')
    ARGS, _ = PARSER.parse_known_args()
    # Cleaning up Training Container
    TrainingContainer.cleanup(base_dir='/opt/ml', env=ARGS.env, logger=logger)
