import os
import logging
import click
from mldock.api.push import \
    push_to_ecr
from mldock.config.config_manager import \
    SagifyConfigManager

logger=logging.getLogger('mldock')

@click.command()
@click.option('--dir', help='Set the working directory for your sagify container.', required=True)
def push(dir):
    """
    Command to push docker container image to ECR using your default AWS sdk credentials.

    note: Override default AWS credentials by providing AWS_DEFAULT_PROFILE environment variable.
    """
    sagify_manager = SagifyConfigManager(
        filepath=os.path.join(dir, ".sagify.json")
    )
    # get sagify_module_path name
    sagify_config = sagify_manager.get_config()
    image_name = sagify_config.get("image_name", None)
    dockerfile_path = os.path.join(
        dir,
        sagify_config.get("sagify_module_dir", "src"),
        'sagify_base'
    )
    if image_name is None:
        logger.info("\nimage_name cannot be None")
    elif image_name.endswith(":latest"):
        logger.info("\nImage version is not supported at this point. Please remove :latest versioning")
    else:
        push_to_ecr(
            script_path='serum/api/build_and_push.sh',
            base_path=dir,
            image_name=image_name,
            dockerfile_path=dockerfile_path,
            module_path=sagify_config.get("sagify_module_dir", "src"),
            target_dir_name=sagify_config.get("sagify_module_dir", "src"),
            requirements_file_path=sagify_config.get("requirements.txt", "requirements.txt")
        )
