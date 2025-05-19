import os

from dotenv import load_dotenv
from config.app_config import AppConfig

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):

    def __init__(self, env_file=None, data_injection=None) -> None:
        init_message = "Initialize Config only once"

        if env_file is not None:
            load_dotenv(env_file)
            init_message += f", env file {env_file}"

        data_config = os.environ.copy()

        if data_injection is not None:
            data_config.update(data_injection)
            init_message += ", data injection length: {}".format(len(data_injection))
        self.app_config = AppConfig(data_config)