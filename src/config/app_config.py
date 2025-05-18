import os

class AppConfig(object):
    def __init__(self, data_config):
        self.log_level = data_config.get('LOG_LEVEL', 'INFO')
