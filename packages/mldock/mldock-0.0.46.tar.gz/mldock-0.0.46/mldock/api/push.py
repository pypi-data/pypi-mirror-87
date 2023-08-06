import logging
from pathlib import Path
from distutils.dir_util import copy_tree
from future.moves import subprocess

logger=logging.getLogger('mldock')


def push_to_ecr(script_path: str, base_path:str, image_name: str, dockerfile_path: str, module_path: str, target_dir_name: str, requirements_file_path: str):
    """Runs the predict shell script and passes the arguments as expected by the script.

    Args:
        script_path (str): relative path to script when run on root
        host (str): http/https host uri
        payload (str): relative path to payload file when run on root
        content_type (str): content type for request
    """
    logger.info("\nStarting Upload to ECR...\n") 
    _ = subprocess.check_call([
                                script_path,
                                image_name,
                                base_path,
                                dockerfile_path,
                                module_path,
                                target_dir_name,
                                requirements_file_path
    ])
    logger.info("\nUpload to ECR complete! ヽ(´▽`)/")
