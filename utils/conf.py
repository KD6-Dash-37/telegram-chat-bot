# conf.py
import os
import yaml

from data_model import BotConfig


def load_config_file(bot_name: str):

    file_name = ".".join([bot_name, "yaml"])

    config_dir = os.path.join("/", *os.getcwd().split("/")[:-1], "bot_configs")

    config_file_path = os.path.join(config_dir, file_name)

    if os.path.exists(config_file_path):

        with open(config_file_path, encoding="utf-8") as yaml_file:

            config = yaml.safe_load(yaml_file)

            return config

    raise FileNotFoundError(config_file_path)


def load_config(bot_name: str):

    config_dict = load_config_file(bot_name=bot_name)

    config = BotConfig.model_validate(config_dict)

    return config
