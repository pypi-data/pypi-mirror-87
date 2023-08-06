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
    run_predict, _copy_boilerplate_to_dst, docker_build, \
        local_train, local_deploy, _rename_file

from mldock.api.local import \
    train_model, deploy_model

click.disable_unicode_literals_warning = True
logger=logging.getLogger('mldock')

@click.group()
def local():
    """
    Commands for local operations: train and deploy
    """
    pass

@click.command()
@click.option('--dir', help='Set the working directory for your sagify container.', required=True)
@click.option('--no-cache', help='builds container from scratch', is_flag=True)
@click.pass_obj
def build(obj, dir, no_cache):
    """build image using docker

    Args:
        dir (str): directory containing model assets
    """
    helper_library_path = obj['helper_library_path']
    try:
        sagify_manager = SagifyConfigManager(
            filepath=os.path.join(dir, ".sagify.json")
        )
        # get sagify_module_path name
        sagify_config = sagify_manager.get_config()
        image_name = sagify_config.get("image_name", None)
        container_dir = sagify_config.get("container_dir", None)
        module_path = os.path.join(
                    dir,
            sagify_config.get("sagify_module_dir", "src"),
        )
        dockerfile_path = os.path.join(
            dir,
            sagify_config.get("sagify_module_dir", "src"),
            container_dir
        )
        requirements_file_path = os.path.join(
            dir,
            sagify_config.get("requirements.txt", "requirements.txt")
        )
        if image_name is None:
            logger.info("\nimage_name cannot be None")
        elif image_name.endswith(":latest"):
            logger.info("\nImage version is not supported at this point. Please remove :latest versioning")
        else:
            docker_build(
                script_path=os.path.join(helper_library_path,'api/build.sh'),
                image_name=image_name,
                dockerfile_path=dockerfile_path,
                module_path=module_path,
                target_dir_name=sagify_config.get("sagify_module_dir", "src"),
                requirements_file_path=requirements_file_path,
                no_cache=no_cache
            )
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.info("{}".format(e))
        sys.exit(-1)

@click.command()
@click.option('--payload', default=None, help='path to payload file', required=True)
@click.option('--content-type', help='format of payload', type=click.Choice(['json', 'csv'], case_sensitive=False))
@click.option('--host', help='host url at which model is served', type=str, default='http://127.0.0.1:8080')
@click.pass_obj
def predict(obj, payload, content_type, host):
    """
    Command to run curl predict against an host served on localhost:8080
    """
    helper_library_path = obj['helper_library_path']
    try:
        script_path=os.path.join(helper_library_path,'api/predict.sh')
        if payload is None:
            logger.info("\nPayload cannot be None")
        else:
            if content_type == "csv":
                content_type = 'text/csv'
                _ = run_predict(
                    script_path=script_path,
                    host=host,
                    payload=payload,
                    content_type=content_type
                )
            elif content_type == 'json':
                content_type = 'application/json'
                _ = run_predict(
                    script_path=script_path,
                    host=host,
                    payload=payload,
                    content_type=content_type
                )
            else:
                raise TypeError("content-type of payload no supported. Only csv and json are supported at the moment")
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.info("{}".format(e))
        sys.exit(-1)

@click.command()
@click.option('--dir', help='Set the working directory for your sagify container.', required=True)
@click.option('--tag', help='docker tag', type=str, default='latest')
@click.pass_obj
def train(obj, dir, tag):
    """
    Command to train ML model(s) locally
    """
    sagify_manager = SagifyConfigManager(
        filepath=os.path.join(dir, ".sagify.json")
    )
    # get sagify_module_path name
    sagify_config = sagify_manager.get_config()
    module_path = os.path.join(
                dir,
        sagify_config.get("sagify_module_dir", "src"),
    )
    image_name = sagify_config.get("image_name", None)
    platform = sagify_config.get("platform", None)
    container_dir = sagify_config.get("container_dir", None)
    helper_library_path = obj['helper_library_path']
    try:
        if platform == "sagemaker":

            local_train(
                dir=module_path,
                docker_tag=tag,
                image_name=image_name
            )
        else:
            train_model(
                script_path=os.path.join(helper_library_path, "api", "train_model.sh"),
                test_dir=os.path.join(module_path, container_dir, "local_test/test_dir"),
                docker_tag=tag,
                image_name=image_name
            )

        logger.info("Local training completed successfully!")
    except ValueError:
        logger.info("This is not a sagify directory: {}".format(dir))
        sys.exit(-1)
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.info("{}".format(e))
        sys.exit(-1)


@click.command()
@click.option('--dir', help='Set the working directory for your sagify container.', required=True)
@click.option('--tag', help='docker tag', type=str, default='latest')
@click.option('--host', help='host url at which model is served', type=str, default='http://127.0.0.1:8080')
@click.pass_obj
def deploy(obj, dir, tag, host):
    """
    Command to deploy ML model(s) locally
    """
    helper_library_path=obj['helper_library_path']
    sagify_manager = SagifyConfigManager(
        filepath=os.path.join(dir, ".sagify.json")
    )
    # get sagify_module_path name
    sagify_config = sagify_manager.get_config()
    module_path = os.path.join(
                dir,
        sagify_config.get("sagify_module_dir", "src"),
    )
    image_name = sagify_config.get("image_name", None)
    platform = sagify_config.get("platform", None)
    container_dir = sagify_config.get("container_dir", None)
    helper_library_path = obj['helper_library_path']
    try:
        logger.info("Started local deployment at {}...\n".format(host))
        if platform == "sagemaker":
        
            local_deploy(
                dir=module_path,
                docker_tag=tag,
                image_name=image_name
            )
        else:
            deploy_model(
                script_path=os.path.join(helper_library_path, "api", "deploy_model.sh"),
                test_dir=os.path.join(module_path, container_dir, "local_test/test_dir"),
                docker_tag=tag,
                image_name=image_name
            )

    except ValueError:
        logger.info("This is not a sagify directory: {}".format(dir))
        sys.exit(-1)
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.info("{}".format(e))
        sys.exit(-1)

local.add_command(build)
local.add_command(predict)
local.add_command(train)
local.add_command(deploy)
