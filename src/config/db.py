class PostgresConfig(object):
    def __init__(self, data_config):
        self.pg_host = data_config.get('PG_HOST')
        self.pg_port = data_config.get('PG_PORT')
        self.pg_database = data_config.get('PG_DATABASE')
        self.pg_user = data_config.get('PG_USER')
        self.pg_password = data_config.get('PG_PASSWORD')
        self.pg_uri = f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}"