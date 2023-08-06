"""
    STARTUP SCRIPT (TRAINING)

    Any tasks to run when starting up the container. Such as downloading data or artifacts.
"""
import logging
import argparse
import sys;sys.path.insert(1, ".")  # Do not remove this
from src.env import TrainingContainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(None)
logger.setLevel(logging.INFO)

if __name__ == '__main__':

    PARSER= argparse.ArgumentParser()
    ## User set params which link to Sagemaker params
    PARSER.add_argument('--env', type=str,
                        default='dev',
                        help='Run setup according to development environment')
    ARGS, _ = PARSER.parse_known_args()

    # Setting up training container
    TrainingContainer.startup(base_dir='/opt/ml', env=ARGS.env, logger=logger)

