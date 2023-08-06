import os
from pathlib import Path
import toml

# DEFAULT SETTING
CONFIG_PATH = str(Path.home())+'/.jijcloud/'
HOST_URL = 'https://jijcloud.azure-api.net/'
DEFAULT_CONFIG_FILE = 'config.toml'

def create_config(token: str, host_url=HOST_URL, config_path=CONFIG_PATH):
    Path(config_path).mkdir(parents=True, exist_ok=True)

    config_dict = {
        'default': {
            'url': host_url,
            'token': token
        }
    }
    # save config file's
    config_path = config_path if config_path[-1] == '/' else config_path + '/'
    config_file_name = config_path + DEFAULT_CONFIG_FILE
    with open(config_file_name, mode='w') as f:
        toml.dump(config_dict, f)

    return config_file_name

    



