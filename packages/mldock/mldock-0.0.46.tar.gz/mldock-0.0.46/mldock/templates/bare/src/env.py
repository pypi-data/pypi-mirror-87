import os
from pathlib import Path

from mldock.platform_helpers.gcp import storage
from mldock.platform_helpers.gcp.storage import _check_if_cloud_scheme, download_input_assets
from mldock.platform_helpers.environment import Environment, get_env_vars

class AIPlatformEnvironment(Environment):
    """
        Extends the Environment class to give us
        more specific environment setup functionality
    """
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
        sm_channels = get_env_vars(regex='INPUT_CHANNEL_.*')
        for channel in sm_channels:
            _ = self.download_input_data_from_cloud_storage(path=channel['value'])

class TrainingContainer:
    """
        A set of tasks for setup and cleanup of container
    """
    def startup(base_dir,logger, env='prod'):
        logger.info("\n\n --- Running Startup Script ---\n\nSetting Up Training Container")
        environment = AIPlatformEnvironment(base_dir=base_dir)
        if env=="prod":
            logger.info("Env == Prod")
            environment.setup_input_data()
        logger.info("\n\n --- Setup Complete --- \n\n")
        

    def cleanup(base_dir, logger, env='prod'):
        """clean up tasks executed on container task complete"""
        logger.info("\n\n --- Running Cleanup Script ---\n\nCleaning Up Training Container")
        if env=="prod":
            logger.info("Env == Prod")
            storage.package_and_upload_model_dir(local_path=os.path.join(base_dir, 'model'), storage_dir_path=os.environ['OUTPUT_CHANNEL_MODEL'], scheme='gs')
            storage.package_and_upload_output_data_dir(local_path=os.path.join(base_dir, 'output'), storage_dir_path=os.environ['OUTPUT_CHANNEL_DATA'], scheme='gs')
        logger.info("\n\n --- Cleanup Complete --- \n\n")

class ServingContainer:
    """
        A set of tasks for setup and cleanup of container
    
        note:
            - Only supports a startup script. Cleanup is a bit fuzzy for serving.
    """
    def startup(base_dir, logger, env='prod'):
        logger.info("\n\n --- Running Startup Script ---\n\nSetting Up Training Container")
        environment = AIPlatformEnvironment(base_dir=base_dir)
        if env=="prod":
            logger.info("Env == Prod")
            environment.setup_input_data()
        logger.info("\n\n --- Setup Complete --- \n\n")
