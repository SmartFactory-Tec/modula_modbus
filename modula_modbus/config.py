from os import path
import toml

CONFIG_PATH = 'config.toml'

DEFAULT_CONFIG = {
    'hostname': 'localhost',
    'port': 8080,
    'odoo_hostname': 'localhost',
    'odoo_port': 80,
    'odoo_user': 'admin',
    'odoo_password': 'admin',
    'odoo_secure': True,
}

class MissingConfigError(Exception):
    def __init__(self, name, message="Missing configuration key in config file"):
        self.name = name
        self.message = message
        super().__init__(self.message)

def load_config() -> dict:
    if not path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'x') as config_file:
            toml.dump(DEFAULT_CONFIG, config_file)

    with open(CONFIG_PATH, 'r') as config_file:
        config = toml.load(config_file)

    config = DEFAULT_CONFIG | config

    return config
