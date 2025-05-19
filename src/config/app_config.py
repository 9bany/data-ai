import os

class AppConfig(object):
    def __init__(self, data_config):
        self.log_level = data_config.get('DATA_AI_LOG_LEVEL', 'ERROR')
    def is_debug(self) -> bool:
        return self.log_level == "DEBUG"
