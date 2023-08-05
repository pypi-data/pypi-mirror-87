import os
from mldock.platform_helpers.gcp import storage
from mldock.platform_helpers.gcp.environment import AIPlatformEnvironment as Environment

class TrainingContainer:
    """A set of tasks for setup and cleanup of container"""
    def startup(base_dir,logger, env='prod'):
        logger.info("\n\n --- Running Startup Script ---\n\nSetting Up Training Container")
        environment = Environment(base_dir=base_dir)
        if env=="prod":
            logger.info("Env == Prod")
            environment.setup_input_data()
        logger.info("\n\n --- Setup Complete --- \n\n")
        

    def cleanup(base_dir, logger, env='prod'):
        """clean up tasks executed on container task complete"""
        logger.info("\n\n --- Running Cleanup Script ---\n\nCleaning Up Training Container")
        if env=="prod":
            logger.info("Env == Prod")
            storage.package_and_upload_model_dir(local_path=os.path.join(base_dir, 'model'), storage_dir_path=os.environ['SM_MODEL_DIR'], scheme='gs')
            storage.package_and_upload_output_data_dir(local_path=os.path.join(base_dir, 'output'), storage_dir_path=os.environ['SM_OUTPUT_DATA_DIR'], scheme='gs')
        logger.info("\n\n --- Cleanup Complete --- \n\n")

class ServingContainer:
    """
        A set of tasks for setup and cleanup of container
    
        note:
            - Only supports a startup script. Cleanup is a  bit fuzzy for serving.
    """
    def startup(base_dir, logger, env='prod'):
        logger.info("\n\n --- Running Startup Script ---\n\nSetting Up Training Container")
        environment = Environment(base_dir=base_dir)
        if env=="prod":
            logger.info("Env == Prod")
            environment.setup_input_data()
        logger.info("\n\n --- Setup Complete --- \n\n")
