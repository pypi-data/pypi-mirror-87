import os
import logging
from pathlib import Path
from future.moves import subprocess

from mldock.config.config_manager import \
    ResourceConfigManager, SagifyConfigManager, PackageConfigManager, \
        HyperparameterConfigManager, InputDataConfigManager
from mldock.api.local import \
    _copy_boilerplate_to_dst, _rename_file

logger=logging.getLogger('mldock')


def generic_init(dir, helper_library_path, sagify_config, new, testing_framework, service):
    src_directory = os.path.join(
        dir,
        sagify_config.get("sagify_module_dir", "src")
    )
    service_directory = os.path.join(
        dir,
        'service'
    )

    template_dir = 'templates'

    template_dir = os.path.join(
        helper_library_path,
        'templates',
        sagify_config['platform']
    )

    sagify_module_path = os.path.join(
        src_directory,
        'container'
    )

    test_path = os.path.join(sagify_module_path, 'local_test', 'test_dir')

    # generic copy
    if new:
        logger.info("Creating new workspace")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'src/'), src_directory)
    if testing_framework == 'pytest':
        logger.info("Adding pytest container tests")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'tests/'), 'tests/')
        logger.info("renaming test file")

        _rename_file(
            base_path='tests/container_health',
            current_filename='_template_test_container.py',
            new_filename='test_{ASSET_DIR}.py'.format(ASSET_DIR=dir)
        )
    if service == 'compose':
        logger.info("Adding service")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'service/'), service_directory)

def sagemaker_init(dir, helper_library_path, sagify_config, new, testing_framework):

    src_directory = os.path.join(
        dir,
        sagify_config.get("sagify_module_dir", "src")
    )

    template_dir = sagify_config.get("template_dir", None)

    if template_dir is None:
        template_dir = os.path.join(
            helper_library_path,
            template_dir,
            sagify_config['platform']
        )

    sagify_module_path = os.path.join(
        src_directory,
        'container'
    )

    test_path = os.path.join(sagify_module_path, 'local_test', 'test_dir')

    # generic copy
    if new:
        logger.info("Creating new workspace")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'src/'), src_directory)
    if testing_framework == 'pytest':
        logger.info("Adding pytest container tests")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'tests/'), 'tests/')
        logger.info("renaming test file")

        _rename_file(
            base_path='tests/container_health',
            current_filename='_template_test_container.py',
            new_filename='test_{ASSET_DIR}.py'.format(ASSET_DIR=dir)
        )

    # sagemaker
    config_path = os.path.join(test_path, 'input/config')
    # set resource config
    logger.info("\n\nGetting Container Resource config")
    resource_config = ResourceConfigManager(
        filepath=os.path.join(config_path, "resourceconfig.json")
    )
    resource_config.ask_for_resourceconfig()
    resource_config.write_file()
    # set input data channels
    logger.info("\n\nGetting Input Data config")
    input_data_channels = InputDataConfigManager(
        filepath=os.path.join(config_path, "inputdataconfig.json")
    )
    input_data_channels.ask_for_input_data_channels()
    input_data_channels.write_file()

    # set hyperparameters
    logger.info("\n\nGetting Hyperparameters config")
    hyperparameters = HyperparameterConfigManager(
        filepath=os.path.join(config_path, "hyperparameters.json")
    )
    hyperparameters.pretty_print()
    hyperparameters.ask_for_hyperparameters()
    hyperparameters.write_file()
    # --end sagemaker


def gcaip_init():
    pass
