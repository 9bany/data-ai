# Configuration loader for Data-AI application

class AppConfig(object):
    """
    AppConfig manages application-level configuration flags such as log level.
    """

    def __init__(self, data_config):
        # Set log level from config, default to 'ERROR' if not provided
        self.log_level = data_config.get('DATA_AI_LOG_LEVEL', 'ERROR')

    def is_debug(self) -> bool:
        # Returns True if log level is set to DEBUG
        return self.log_level == "DEBUG"
