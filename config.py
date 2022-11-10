from os import path
import toml

CONFIG_PATH = 'config.toml'

DEFAULT_CONFIG = {
    'hostname': 'localhost',
    'port': 80,
    'user': 'admin',
    'password': 'admin',
    'secure': True,
}

class MissingConfigError(Exception):
    def __init__(self, name):
        self.name = name

def load_config() -> dict:
    if not path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'x') as config_file:
            toml.dump(DEFAULT_CONFIG, config_file)

    config = {}

    with open(CONFIG_PATH, 'r') as config_file:
        config = toml.load(config_file)

    for required_entry in DEFAULT_CONFIG.keys():
        if required_entry in config: continue
        raise MissingConfigError(required_entry)

    return config
