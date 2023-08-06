import os
import json
import click
import logging
from pathlib import Path

logger=logging.getLogger('mldock')

class BaseConfigManager:
    """Base config manager with basic read, write and update functionality.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        if not self.file_exists(self.filepath):
            prompt_input = click.prompt("File not found. Create?", default="yes")
        
            if prompt_input:
                self.touch(self.filepath)

        self.config = self.load_config(self.filepath)

    @staticmethod
    def touch(path: str):
        """create a blank json file, seeded with {}

        Args:
            path (str): path to file
        """
        with open(path, 'a') as file_:
            json.dump({}, file_)

    @staticmethod
    def file_exists(filename: str) -> bool:
        """Check if file exists

        Args:
            filename (str): path to file

        Returns:
            bool: whether file exists
        """
        return os.path.exists(filename)

    @staticmethod
    def load_config(filename: str) -> dict:
        """loads config from file

        Args:
            filename (str): path to config to load
        Returns:
            dict: config
        """
        with open(filename, "r") as file_:
            config = json.load(file_)
            return config

    def pretty_print(self):
        """pretty prints a json config to terminal
        """
        pretty_config = json.dumps(self.config, indent=4, separators=(',', ': '), sort_keys=True)
        logger.info("{}\n".format(pretty_config))

    def write_file(self):
        """
        Trains ML model(s) locally
        :param dir: [str], source root directory
        :param docker_tag: [str], the Docker tag for the image
        :param image_name: [str], The name of the Docker image
        """

        with open(self.filepath, 'w') as config_file:
            json.dump(self.config, config_file, indent=4)

class ResourceConfigManager(BaseConfigManager):
    """Resource Config Manager for sagify
    """

    @staticmethod
    def ask_for_current_host_name():
        """prompt user for current host name

        Returns:
            return: current host name
        """
        current_host_name = chosen_python_index = click.prompt(
            text="Set current host name: ",
            default="algo",
        )

        return current_host_name

    @staticmethod
    def ask_for_network_interface_name():
        """prompt user for network interface name

        Returns:
            str: network interface name
        """
        network_interface_name = click.prompt(
            text="Set current host name: ",
            default="eth1",
        )

        return network_interface_name

    def ask_for_resourceconfig(self):
        """prompt user for resource config
        """
        current_host_name = self.ask_for_current_host_name()
        hosts = [current_host_name+"-1"]
        network_interface_name = self.ask_for_network_interface_name()

        self.config = {
            "current_host": hosts[0],
            "hosts": hosts,
            "network_interface_name": network_interface_name
        }

class SagifyConfigManager(BaseConfigManager):
    """Hyperparameter Config Manager for sagify
    """

    def setup_config(self):

        self.ask_for_image_name()
        self.ask_for_platform_name()
        self.ask_for_sagify_module_dir()
        self.ask_for_container_dir_name()
        self.ask_for_requirements_file_name()
        self.ask_for_python_version()
        self.ask_for_path_to_template_dir()

    def ask_for_image_name(self):
        """prompt user for image name

        Returns:
            return: image name
        """
        image_name = click.prompt(
            text="Set your image name: ",
        )

        self.config.update({
            'image_name':image_name
        })
    
    def ask_for_platform_name(self):
        """prompt user for platform name

        Returns:
            return: platform name
        """
        platform_name = click.prompt(
            text="Set your platform name:",
            default='bare'
        )

        self.config.update({
            'platform':platform_name
        })

    def ask_for_container_dir_name(self):
        """prompt user for platform name

        Returns:
            return: platform name
        """
        container_dir_name = click.prompt(
            text="Set your container dir name:",
            default='container'
        )

        self.config.update({
            'container_dir':container_dir_name
        })

    def ask_for_sagify_module_dir(self):
        """prompt user for image name

        Returns:
            return: image name
        """
        
        sagify_module_dir = click.prompt(
            text="Set sagify module dir: ",
            default='src'
        )

        self.config.update({
            'sagify_module_dir': sagify_module_dir
        })

    def ask_for_requirements_file_name(self):
        """prompt user for image name

        Returns:
            return: image name
        """
        requirements_file_name = click.prompt(
            text="Set full path to requirements: ",
            default='requirements.txt'
        )

        self.config.update({
            'requirements_dir':requirements_file_name
        })

    def ask_for_python_version(self):
        logger.info("Select Python interpreter:")
        logger.info('{}'.format('\n'.join(['1 - Python3', '2 - Python2'])))

        def _validate_python_option(input_value):
            if int(input_value) not in {1, 2}:
                raise BadParameter(
                    message="invalid choice: {}. (choose from 1, 2)".format(str(input_value))
                )

            return int(input_value)

        chosen_python_index = click.prompt(
            text="Choose from 1, 2",
            default=1,
            value_proc=lambda x: _validate_python_option(x)
        )

        python_version = '3.6' if chosen_python_index == 1 else '2.7'

        self.config.update({
            'python_version':python_version
        })

    def ask_for_path_to_template_dir(self):
        """prompt user for platform name

        Returns:
            return: platform name
        """
        template_dir = click.prompt(
            text="Set your template directory:",
            default=""
        )

        if template_dir == "":
            template_dir = None

        self.config.update({
            'template_dir':template_dir
        })

    def get_config(self) -> dict:
        """get config object

        Returns:
            dict: config
        """
        return self.config

class PackageConfigManager(BaseConfigManager):
    """Hyperparameter Config Manager for sagify
    """
    @staticmethod
    def touch(filename):
        """creat an empty txt file

        Args:
            filename (str): path to file
        """
        Path(filename).touch()

    @staticmethod
    def load_config(filename: str) -> list:
        """load config

        Args:
            filename (str): path to config file to load

        Returns:
            list: config
        """
        path = Path(filename)
        with path.open() as f: 
            config = f.readlines()
        
        for index, c_package in enumerate(config):
            if c_package.endswith("\n"):
                config[index] = config[index].split("\n")[0]
        return config

    def get_config(self) -> list:
        """get config object

        Returns:
            list: config
        """
        return self.config

    def seed_packages(self, packages: list):
        """seeds config with required package modules

        Args:
            packages (list): packages to add to config
        """
        for new_package in packages:
            for config_package in self.config:
                if new_package not in config_package:
                    self.config.append(new_package)

    def pretty_print(self):
        """pretty prints a list config to terminal
        """
        pretty_config = json.dumps(self.config, indent=4, separators=(',', ': '))
        logger.info("{}\n".format(pretty_config))

    def write_file(self):
        """
        write to file
        """
        config = set(self.config)
        config_txt = "\n".join(config) + "\n"
        print(config_txt)
        Path(self.filepath).write_text(config_txt)
    

class HyperparameterConfigManager(BaseConfigManager):
    """Hyperparameter Config Manager for sagify
    """
    @staticmethod
    def is_float(s):
        """ Returns True is string is a number. """
        try:
            float(s)
            return True
        except ValueError:
            return False
    def ask_for_hyperparameters(self):
        """prompt user for hyperparameters
        """
        while True:
            name_value_pair = click.prompt(
                text="Add a hyperparameter. (Expects name:value). Hit enter to continue.",
                default="end",
                show_default=False,
                type=str
            )
            if name_value_pair == "end":
                logger.info("\nUpdated hyperparameters = {}".format(self.config))
                break
            elif ":" in name_value_pair and not name_value_pair == "name:value":
                name, value = name_value_pair.split(":",1)
                if value.isdigit():
                    value = int(value)
                elif self.is_float(value):
                    value = float(value)
                logger.info("Adding {}={}".format(name, value))
                self.config.update({name: value})
            else:
                logger.info("Expected format as name:value. Skipping")

class InputDataConfigManager(BaseConfigManager):
    """InputData Config Manager for sagify
    """
    attribute_config = { 
            "TrainingInputMode": "File",
            "S3DistributionType": "FullyReplicated",
            "RecordWrapperType": "None"
    }
    def ask_for_input_data_channels(self):
        """prompt users for input data channels
        """
        while True:
            channel = click.prompt(
                text="Add a data channel. (Expects name). Hit enter to continue.",
                default="NULL",
                show_default=False
            )
            if channel == "NULL":
                break
            else:
                logger.info("Adding {} channel".format(channel))
                self.config.update({
                    channel: self.attribute_config
                })
