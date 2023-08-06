import os
from google.cloud import storage
import json
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(None)
logger.setLevel(logging.INFO)

def get_env_vars(regex):
    """Get all environ vars matching contains='<PREFIX>'"""
    filtered_env_vars = []

    regex_pattern = re.compile(regex)

    for key,value in os.environ.items():
        if regex_pattern.match(key):
            # get all keys matching the regex
            filtered_env_vars.append({'key': key, 'value': value})
    return filtered_env_vars

class Environment:

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self._create_training_directories()

    def _create_training_directories(self):
        """Create the directory structure, if not exists
        """
        logger.debug("Creating a new training folder under {} .".format(self.base_dir))

        try:
            self.input_data_dir.mkdir(parents=True, exist_ok=True)
            self.model_dir.mkdir(parents=True, exist_ok=True)
            self.input_config_dir.mkdir(parents=True, exist_ok=True)
            self.output_data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exception:
            print(exception)
            raise


    @property
    def input_dir(self):
        return Path(self.base_dir, 'input')

    @property
    def input_data_dir(self):
        return Path(self.input_dir, 'data')

    @property
    def input_config_dir(self):
        return Path(self.input_dir, 'config')

    @property
    def model_dir(self):
        return Path(self.base_dir, 'model')
    
    @property
    def output_data_dir(self):
        return Path(self.base_dir, 'output')
