import os
import sys
import json
import logging
import click
from pathlib import Path
from future.moves import subprocess

from mldock.config.config_manager import \
    ResourceConfigManager, SagifyConfigManager, PackageConfigManager, \
        HyperparameterConfigManager, InputDataConfigManager
from mldock.api.local import \
    _copy_boilerplate_to_dst, _rename_file

from mldock.api.platform import sagemaker_init, generic_init

click.disable_unicode_literals_warning = True
logger=logging.getLogger('mldock')

@click.command()
@click.option('--dir', help='Set the working directory for your sagify container.', required=True)
@click.option('--new', is_flag=True)
@click.option('--testing_framework', default=None, help='(Optional) Pytest framework. This creates a few health-check tests')
@click.option('--service', default=None, help='(Optional) Docker Compose. This seeds a service config.')
@click.pass_obj
def init(obj, dir, new, testing_framework, service):
    """
    Command to initialize container configs required by sagemaker-training.
    """
    helper_library_path=obj['helper_library_path']
    try:
        logger.info("Getting Sagify config")
        sagify_manager = SagifyConfigManager(
            filepath=os.path.join(dir, ".sagify.json")
        )
        if new:
            sagify_manager.setup_config()
            # write .sagify file
            logger.info("\n\nWriting a new .sagify file")
            sagify_manager.write_file()

        sagify_manager.pretty_print()

        logger.info("Getting Requirements")
        package_manager = PackageConfigManager(
            filepath=os.path.join(dir, "requirements.txt")
        )
        package_manager.pretty_print()
        # write to package manager
        package_manager.write_file()


        path_to_payload = Path(os.path.join(dir, "payload.json"))
        if not path_to_payload.exists():
            path_to_payload.write_text(json.dumps({"feature1": 10, "feature2":"groupA"}))

        # get sagify_module_path name
        sagify_config = sagify_manager.get_config()
        platform = sagify_config.get("platform", None)

        if platform == "sagemaker":
            sagemaker_init(
                dir=dir,
                helper_library_path=helper_library_path,
                sagify_config=sagify_config,
                new=new,
                testing_framework=testing_framework
            )
        elif platform == "bare":
            generic_init(
                dir=dir,
                helper_library_path=helper_library_path,
                sagify_config=sagify_config,
                new=new,
                testing_framework=testing_framework,
                service=service
            )
        else:
            raise Exception("Platform not found. Please supply available platform template.")

        logger.info("\nlocal container volume is ready! ヽ(´▽`)/")
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.info("{}".format(e))
        sys.exit(-1)
