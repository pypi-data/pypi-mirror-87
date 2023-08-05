import os
from google.cloud import storage
import json
from pathlib import Path
from future.moves import subprocess
import logging

from mldock.platform_helpers.gcp.storage import _check_if_cloud_scheme, download_input_assets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(None)
logger.setLevel(logging.INFO)

class MLFlowGCSEnvironment: 

    def __init__(self, base_dir, experiment_id, run_id, gcs_artifact_store):
        self.base_dir = base_dir
        self.experiment_id = experiment_id
        self.run_id = run_id
        self.gcs_artifact_store=gcs_artifact_store

        logger.debug("Creating training directories")
        self._create_training_directories()

        logger.debug("=== Local Containter ===\n\nCurrent base_dir: {}".format(self.base_dir))
        logger.debug("Current run_base_dir: {}".format(self.run_base_dir))
        logger.debug("Current GCS Artifact Store: {}".format(self.gcs_artifact_store))
        logger.debug("Current model: {}".format(self.model_local_path))
        logger.debug("Current metrics: {}".format(self.metrics_local_path))
        logger.debug("\n=== \nAll Set up and Ready to Go!\n ===\n")
    
    def _create_training_directories(self):
        """Create the directory structure and files necessary for training under the base path.
        """
        Path(self.run_base_dir).mkdir(parents=True, exist_ok=True)
        Path(self.model_local_path).mkdir(parents=True, exist_ok=True)
        Path(self.metrics_local_path).mkdir(parents=True, exist_ok=True)
        Path(self.params_local_path).mkdir(parents=True, exist_ok=True)
        Path(self.tags_local_path).mkdir(parents=True, exist_ok=True)

    @property
    def run_base_dir(self):
        return os.path.join(self.base_dir, self.experiment_id, self.run_id)

    @property
    def artifact_store_path(self):
        return self.gcs_artifact_store

    @property
    def model_local_path(self):
        return os.path.join(self.run_base_dir,'artifacts/model')

    @property
    def metrics_local_path(self):
        return os.path.join(self.run_base_dir,'metrics')

    @property
    def params_local_path(self):
        return os.path.join(self.run_base_dir,'params')

    @property
    def tags_local_path(self):
        return os.path.join(self.run_base_dir,'tags')

def update_bash_env_vars(key, value):
    """Execute a bash export to set ENV VARS

    Args:
        key (str): ENV var key
        value (str): ENV var value
    """
    _FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    local_train_script_path = os.path.join(_FILE_DIR_PATH, 'update_var.sh')
    output = subprocess.check_output(
        [
            "{}".format(local_train_script_path),
            key,
            value
        ]
    )

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

class AIPlatformEnvironment(Environment):
    @staticmethod
    def get_all_environ_vars(contains):
        """Get all environ vars matching contains='<PREFIX>'"""
        sm_channels = []
        for key,value in os.environ.items():
            if contains in key:
                sm_channels.append({'channel': key, 'path': value})
        return sm_channels 

    def download_input_data_from_cloud_storage(self, path):
        """
            download only cloud storage artifacts
        """
        scheme = 'gs' 
        is_cloud_storage =  _check_if_cloud_scheme(url=path, scheme=scheme)
        if is_cloud_storage:
            download_input_assets(storage_dir_path=path, local_path=self.input_data_dir, scheme=scheme)
        else:
            Exception("No Cloud storage url was found. Must have gs:// schema")
        folder = Path(path).name
        local_path = Path(self.input_data_dir, folder)
        return local_path

    def setup_input_data(self):
        """ Iterates through environment variables and downloads artifacts from storage.
        """
        sm_channels = self.get_all_environ_vars(contains='SM_CHANNEL_')
        for channel in sm_channels:
            _ = self.download_input_data_from_cloud_storage(path=channel['path'])
