import os
import json
import logging
from pathlib import Path
from distutils.dir_util import copy_tree
from future.moves import subprocess

logger=logging.getLogger('mldock')

def train_model(script_path, test_dir, docker_tag, image_name):
    """
    Trains ML model(s) locally
    :param dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """
    local_train_script_path = script_path
    test_path = test_dir

    output = subprocess.check_output(
        [
            "{}".format(local_train_script_path),
            "{}".format(os.path.abspath(test_path)),
            docker_tag,
            image_name
        ]
    )
    logger.debug(output.decode('utf-8'))
    logger.info("\nTraining Complete! ヽ(´▽`)/")

def local_train(dir, docker_tag, image_name):
    """
    Trains ML model(s) locally
    :param dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """
    sagify_module_path = os.path.join(dir, 'container')
    local_train_script_path = os.path.join(sagify_module_path, 'local_test', 'train_local.sh')
    test_path = os.path.join(sagify_module_path, 'local_test', 'test_dir')

    if not os.path.isdir(test_path):
        raise ValueError("This is not a sagify directory: {}".format(dir))

    output = subprocess.check_output(
        [
            "{}".format(local_train_script_path),
            "{}".format(os.path.abspath(test_path)),
            docker_tag,
            image_name
        ]
    )
    logger.debug(output.decode('utf-8'))
    logger.info("\nTraining Complete! ヽ(´▽`)/")


def deploy_model(script_path, test_dir, docker_tag, image_name):
    """
    Deploys ML models(s) locally
    :param dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """
    local_deploy_script_path = script_path
    test_path = test_dir

    output = subprocess.check_output(
        [
            "{}".format(local_deploy_script_path),
            "{}".format(os.path.abspath(test_path)),
            docker_tag,
            image_name
        ]
    )
    logger.debug(output.decode('utf-8'))

def local_deploy(dir, docker_tag, image_name):
    """
    Deploys ML models(s) locally
    :param dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """
    sagify_module_path = os.path.join(dir, 'container')
    local_deploy_script_path = os.path.join(sagify_module_path, 'local_test', 'deploy_local.sh')
    test_path = os.path.join(sagify_module_path, 'local_test', 'test_dir')

    if not os.path.isdir(test_path):
        raise ValueError("This is not a sagify directory: {}".format(dir))

    output = subprocess.check_output(
        [
            "{}".format(local_deploy_script_path),
            "{}".format(os.path.abspath(test_path)),
            docker_tag,
            image_name
        ]
    )
    logger.debug(output.decode('utf-8'))

def get_local_container_ids(dir, docker_tag, image_name):
    """
    Deploys ML models(s) locally
    :param dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """
    sagify_module_path = os.path.join(dir, 'container')
    local_deploy_script_path = os.path.join(sagify_module_path, 'local_test', 'deploy_local.sh')
    test_path = os.path.join(sagify_module_path, 'local_test', 'test_dir')

    if not os.path.isdir(test_path):
        raise ValueError("This is not a sagify directory: {}".format(dir))

    output = subprocess.check_output(
        [
            "{}".format(local_deploy_script_path),
            "{}".format(os.path.abspath(test_path)),
            docker_tag,
            image_name
        ]
    )
    logger.debug(output.decode('utf-8'))

def local_deploy_detached(dir, docker_tag, image_name):
    """
    Deploys ML models(s) locally
    :param dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """
    sagify_module_path = os.path.join(dir, 'container')
    local_deploy_script_path = os.path.join(sagify_module_path, 'local_test', 'deploy_local.sh')
    test_path = os.path.join(sagify_module_path, 'local_test', 'test_dir')

    if not os.path.isdir(test_path):
        raise ValueError("This is not a sagify directory: {}".format(dir))

    output = subprocess.Popen(
        [
            "{}".format(local_deploy_script_path),
            "{}".format(os.path.abspath(test_path)),
            docker_tag,
            image_name
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    logger.debug(output)
    logger.info("\nDeploy Ready! ヽ(´▽`)/")
    logger.info(
        "\nRemember to stop the container once you're done."
        "\n\nRun:\n>> docker ps\n\nfollowed by:\n>> docker stop <container-id>\n"
    )

def docker_build(
    script_path: str,
    image_name: str,
    dockerfile_path: str,
    module_path: str,
    target_dir_name: str,
    requirements_file_path: str,
    no_cache: bool
):
    """Runs the build executable from script path, passing a set of arguments in a command line subprocess.

    Args:
        script_path (str): relative path to script when run on root
        base_path (str):
        image_name (str):
        dockerfile_path (str):
        module_path (str):
        target_dir_name (str):
        requirements_file_path (str):
    """
    logger.info("\nStarting build...\n") 
    _ = subprocess.check_call([
                                script_path,
                                image_name,
                                dockerfile_path,
                                module_path,
                                target_dir_name,
                                requirements_file_path,
                                str(no_cache).lower()
    ])
    logger.info("\nBuild Complete! ヽ(´▽`)/")

def _rename_file(base_path, current_filename, new_filename):
    """renames filename for a given base_path, saving the file in the same base_path

    Args:
        base_path ([type]): directory path containing file to rename
        current_filename ([type]): current name of the file to rename
        new_filename ([type]): new name for the renamed file
    """
    Path(base_path, current_filename).rename(Path(base_path, new_filename))

def _create_empty_file(base_path, filename):
    """renames filename for a given base_path, saving the file in the same base_path

    Args:
        base_path ([type]): directory path containing file to rename
        current_filename ([type]): current name of the file to rename
        new_filename ([type]): new name for the renamed file
    """
    Path(base_path, filename).touch(exist_ok=True)

def _copy_boilerplate_to_dst(src: str, dst: str):
    """[summary]

    Args:
        src (str): [description]
        dst (str): [description]
    """
    source_path = str(Path(src).absolute())
    destination_path = str(Path(dst).absolute())
    copy_tree(source_path, destination_path)


def run_predict(script_path: str, host: str, payload: str, content_type: str):
    """Runs the predict shell script and passes the arguments as expected by the script.

    Args:
        script_path (str): relative path to script when run on root
        host (str): http/https host uri
        payload (str): relative path to payload file when run on root
        content_type (str): content type for request
    """
    logger.info("\nRunning Prediction...\n") 
    result = subprocess.run([
                                     script_path,
                                     host,
                                     payload,
                                     content_type
    ], stdout=subprocess.PIPE)

    if content_type == 'application/json':
        decoded_stdout = json.loads(result.stdout.decode())
        pretty_output = json.dumps(decoded_stdout, indent=4, separators=(',', ': '), sort_keys=True)
    else:
        pretty_output = result.stdout
    logger.info(pretty_output)
    logger.info("\nPrediction Complete! ヽ(´▽`)/")
    return pretty_output
