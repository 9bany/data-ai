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
        self.open_ai_key = data_config.get('OPENAI_API_KEY', None)
        self.google_api_key = data_config.get('GOOGLE_API_KEY', None)
        self.anthropic_api_key = data_config.get('ANTHROPIC_API_KEY', None)
        self.groq_api_key = data_config.get('GROQ_API_KEY', None)