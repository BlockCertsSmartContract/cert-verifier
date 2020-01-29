import os
import configargparse

cwd = os.getcwd()
CONFIG = None


def add_arguments(p):
    p.add('-c', '--my-config', required=False, env_var='CONFIG_FILE',
          is_config_file=True, help='config file path')
    p.add_argument('--infura_ropsten', help='infura ropsten', env_var='INFURA_ROPSTEN')
    p.add_argument('--infura_mainnet', help='infura mainnet', env_var='INFURA_MAINNET')


def get_config():
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(cwd, 'conf.ini')])
    add_arguments(p)
    parsed_config, _ = p.parse_known_args()

    global CONFIG
    CONFIG = parsed_config
    return parsed_config

